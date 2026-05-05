#!/usr/bin/env python3
"""
Module de création de boîtes mail via Mailcow API MySQL.
Utilisé par l'agent création de comptes.
"""

import subprocess
import os
import sys

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'le-lab.db')
DB_USER = 'mailcow'
DB_PASS = 'JKTKg6HzlIwN5ihTMhc8bO5i8LxX'
DB_NAME = 'mailcow'
DOMAIN = 'automatisations.org'
QUOTA = 5000000000  # 5 Go par boîte

# ─── GÉNÉRATION MDP ─────────────────────────────────────────────────────────

def generer_hash_mdp(password):
    """Génère un hash SHA512-CRYPT pour Mailcow via Dovecot."""
    cmd = [
        'docker', 'exec',
        subprocess.check_output(
            ['docker', 'ps', '-qf', 'name=dovecot-mailcow']
        ).decode().strip(),
        'doveadm', 'pw', '-s', 'SHA512-CRYPT', '-p', password
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().replace('\r', '')

def exec_mysql(query):
    """Exécute une requête MySQL dans le conteneur Mailcow."""
    container = subprocess.check_output(
        ['docker', 'ps', '-qf', 'name=mysql-mailcow']
    ).decode().strip()
    
    cmd = [
        'docker', 'exec', container,
        'mariadb', '-u', DB_USER, f'-p{DB_PASS}', DB_NAME,
        '-e', query
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ⚠️ Erreur MySQL: {result.stderr.strip()}")
        return False
    return True

# ─── CRÉATION ────────────────────────────────────────────────────────────────

def creer_boite(email, nom, mot_de_passe):
    """Crée une boîte mail sur mail.automatisations.org."""
    local_part = email.split('@')[0]
    
    # Vérifier si la boîte existe déjà
    verif = subprocess.run(
        ['docker', 'exec',
         subprocess.check_output(['docker', 'ps', '-qf', 'name=mysql-mailcow']).decode().strip(),
         'mariadb', '-u', DB_USER, f'-p{DB_PASS}', DB_NAME,
         '-e', f"SELECT username FROM mailbox WHERE username='{email}';"],
        capture_output=True, text=True
    )
    if email in verif.stdout:
        print(f"  ⚠️ {email} existe déjà (ignoré)")
        return True
    
    hash_mdp = generer_hash_mdp(mot_de_passe)
    
    query = f"""
        INSERT INTO mailbox 
        (username, domain, local_part, name, quota, active, password)
        VALUES ('{email}', '{DOMAIN}', '{local_part}', '{nom}', {QUOTA}, 1, '{hash_mdp}');
    """
    
    success = exec_mysql(query)
    if success:
        # Ajouter l'entrée sender_acl pour permettre l'envoi depuis cette adresse
        exec_mysql(f"""
            INSERT IGNORE INTO sender_acl (logged_in_as, send_as)
            VALUES ('{email}', '{email}');
        """)
        print(f"  ✅ {email} créée")
    else:
        print(f"  ❌ {email} échec")
    
    return success

def creer_boites_portfolio(prenom, suffixe, mdp):
    """Crée les 10 boîtes + 1 admin pour un prénom donné."""
    email = f"{prenom.lower()}.{suffixe}@{DOMAIN}"
    nom = f"{prenom} {suffixe.capitalize()}"
    return creer_boite(email, nom, mdp)

if __name__ == "__main__":
    # Test: créer une boîte de test
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "test":
            creer_boite("test@automatisations.org", "Test", "Turing1!Alan")
        elif action == "liste":
            exec_mysql("SELECT username, name, quota FROM mailbox ORDER BY username;")
        else:
            print(f"Actions: test, liste")
    else:
        print(f"Module Mailcow — Agent de création de boîtes")
