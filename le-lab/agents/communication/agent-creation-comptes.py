#!/usr/bin/env python3
"""
Agent Création de Comptes
Gère la génération et le suivi des comptes pour les portfolios.
"""

import mysql.connector
import os
import sys
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'alan',
    'password': 'Turing1!Alan',
    'database': 'le_lab'
}

def get_db():
    """Connexion MySQL"""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def dashboard():
    """Affiche le tableau de bord"""
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    
    print("=" * 55)
    print("📊 AGENT CRÉATION DE COMPTES - DASHBOARD")
    print("=" * 55)
    
    cur.execute("SELECT * FROM vue_etat_global")
    row = cur.fetchone()
    if row:
        print(f"  Comptes totaux:         {row['total_comptes']}")
        print(f"  Comptes actifs:         {row['comptes_actifs']}")
        print(f"  Comptes bloqués:        {row['comptes_bloques']}")
        print(f"  Portfolios:             {row['total_portfolios']}")
        print(f"  Publications réussies:  {row['pubs_reussies']}")
        print(f"  Publications échouées:  {row['pubs_echouees']}")
    
    print("\n📋 Portfolios :")
    cur.execute("SELECT id, nom, numero, statut FROM portfolios ORDER BY numero")
    for p in cur.fetchall():
        cur.execute("SELECT COUNT(*) as c FROM comptes WHERE portfolio_id=%s", (p['id'],))
        nb = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) as c FROM comptes WHERE portfolio_id=%s AND statut='actif'", (p['id'],))
        actifs = cur.fetchone()['c']
        print(f"  #{p['numero']} {p['nom']} [{p['statut']}] - {actifs}/{nb} actifs")
    
    print("\n⚠️  Comptes problématiques :")
    cur.execute("""
        SELECT c.id, c.email, c.reseau, c.statut, c.date_creation, p.nom as portfolio
        FROM comptes c JOIN portfolios p ON c.portfolio_id = p.id
        WHERE c.statut IN ('bloque', 'shadowban', 'a_verifier')
        ORDER BY c.date_creation DESC
    """)
    problemes = cur.fetchall()
    if problemes:
        for c in problemes:
            print(f"  🔴 {c['email']} - {c['reseau']} - {c['statut']} ({c['portfolio']})")
    else:
        print("  ✅ Aucun compte problématique")
    
    conn.close()

def creer_portfolio(numero, proxy=None):
    """Crée un nouveau portfolio"""
    conn = get_db()
    cur = conn.cursor()
    nom = f"Portfolio {numero}"
    try:
        cur.execute("INSERT INTO portfolios (nom, numero, proxy, statut) VALUES (%s, %s, %s, 'en_creation')",
                   (nom, numero, proxy))
        conn.commit()
        print(f"✅ Portfolio #{numero} '{nom}' créé")
        return cur.lastrowid
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return None
    finally:
        conn.close()

def ajouter_email(portfolio_id):
    """Génère un email automatisations.org pour le portfolio"""
    # Noms alphabétiques par portfolio (1=A, 2=B, 3=C...)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT numero FROM portfolios WHERE id=%s", (portfolio_id,))
    p = cur.fetchone()
    
    if not p:
        print(f"❌ Portfolio #{portfolio_id} introuvable")
        conn.close()
        return None
    
    lettre = alphabet[p['numero'] - 1]
    
    # Liste de prénoms par lettre
    prenoms = {
        'A': ['Antoine', 'Alexandre', 'Anaïs', 'Arthur', 'Amélie', 'Adam', 'Axel', 'Alice', 'Alban', 'Aurélie'],
        'B': ['Benjamin', 'Bastien', 'Bérénice', 'Bruno', 'Baptiste', 'Blandine', 'Bertrand', 'Béatrice', 'Boris', 'Brigitte'],
        'C': ['Camille', 'Clément', 'Coralie', 'Cédric', 'Charlotte', 'Christophe', 'Céline', 'Corentin', 'Coline', 'Cyril'],
        'D': ['David', 'Delphine', 'Damien', 'Diane', 'Dylan', 'Dorian', 'Daphné', 'Denis', 'Dominique', 'Danièle'],
        'E': ['Emma', 'Étienne', 'Élodie', 'Émile', 'Estelle', 'Éric', 'Eva', 'Edouard', 'Élise', 'Ethan'],
        'F': ['Florent', 'Fanny', 'Fabien', 'Flora', 'Franck', 'Fiona', 'Frédéric', 'Flavie', 'Florian', 'Félicie'],
        'G': ['Gabriel', 'Gaëlle', 'Guillaume', 'Géraldine', 'Gaspard', 'Gwen', 'Grégoire', 'Gaëtan', 'Gisèle', 'Gilles'],
        'H': ['Hugo', 'Hélène', 'Henri', 'Hermine', 'Hadrien', 'Hortense', 'Hervé', 'Honorine', 'Hippolyte', 'Huguette'],
        'I': ['Inès', 'Ismaël', 'Iris', 'Ivan', 'Imane', 'Isabelle', 'Isaac', 'Irène', 'Idriss', 'Iphigénie'],
        'J': ['Jules', 'Jeanne', 'Jérôme', 'Julie', 'Jérémy', 'Jessica', 'Jordan', 'Justine', 'Jonathan', 'Juliette'],
        'K': ['Kévin', 'Karine', 'Kenzo', 'Khadija', 'Kylian', 'Kim', 'Killian', 'Kelly', 'Kurt', 'Kenza'],
        'L': ['Lucas', 'Léa', 'Louis', 'Laura', 'Léo', 'Lise', 'Lucien', 'Léonie', 'Lorenzo', 'Lucie'],
        'M': ['Mathis', 'Manon', 'Maxime', 'Marie', 'Mattéo', 'Mélanie', 'Marcel', 'Mylène', 'Morgan', 'Margot'],
        'N': ['Nathan', 'Nina', 'Noé', 'Nadia', 'Nicolas', 'Noémie', 'Nolan', 'Nathalie', 'Nelson', 'Nora'],
        'O': ['Oscar', 'Océane', 'Olivier', 'Odile', 'Owen', 'Orlane', 'Octave', 'Oriane', 'Othman', 'Ophélie'],
        'P': ['Paul', 'Pauline', 'Pierre', 'Pénélope', 'Philippe', 'Priscille', 'Patrick', 'Pascale', 'Pablo', 'Paloma'],
        'Q': ['Quentin', 'Quitterie', 'Quoc', 'Quentin', 'Quiana', 'Quillan', 'Qamar', 'Queen', 'Quirinus', 'Quintina'],
        'R': ['Romain', 'Romane', 'Raphaël', 'Rachel', 'Robin', 'Roxane', 'Rémi', 'Rebecca', 'Roger', 'Rosalie'],
        'S': ['Sarah', 'Simon', 'Sacha', 'Sandra', 'Samuel', 'Sophie', 'Sébastien', 'Sylvie', 'Steven', 'Sabrina'],
        'T': ['Thomas', 'Tatiana', 'Théo', 'Tamara', 'Tristan', 'Tiphaine', 'Timothée', 'Thérèse', 'Tom', 'Tania'],
        'U': ['Ulysse', 'Ursule', 'Uriel', 'Uma', 'Ulrich', 'Ursula', 'Ugo', 'Umberto', 'Uranie', 'Ulysse'],
        'V': ['Valentin', 'Valérie', 'Victor', 'Vanessa', 'Vincent', 'Victoire', 'Vianney', 'Violette', 'Vladimir', 'Véronique'],
        'W': ['William', 'Wendy', 'Wesley', 'Wilhelmine', 'Walter', 'Wanda', 'Warren', 'Wilma', 'Walid', 'Wivine'],
        'X': ['Xavier', 'Xavière', 'Xander', 'Xana', 'Xénophon', 'Xylia', 'Xerxès', 'Ximena', 'Xavier', 'Xynthia'],
        'Y': ['Yannick', 'Yasmine', 'Yves', 'Yseult', 'Yanis', 'Yolande', 'Yohan', 'Ysée', 'Yuri', 'Yvonne'],
        'Z': ['Zoé', 'Zacharie', 'Zélie', 'Zakaria', 'Zéphyr', 'Zia', 'Zachary', 'Zita', 'Zoran', 'Zulma'],
    }
    
    prenoms_lettre = prenoms.get(lettre, [])
    if not prenoms_lettre:
        # Fallback
        prenoms_lettre = [f"User{lettre}{i+1}" for i in range(10)]
    
    # Voir combien d'emails existent déjà pour ce portfolio
    cur.execute("SELECT COUNT(*) as c FROM comptes WHERE portfolio_id=%s", (portfolio_id,))
    count = cur.fetchone()['c']
    
    if count >= 10:
        print(f"⚠️ Portfolio #{portfolio_id} a déjà {count} comptes (max 10)")
        conn.close()
        return []
    
    emails = []
    start = count
    for i in range(start, min(start + (10 - count), 10)):
        prenom = prenoms_lettre[i]
        nom = prenom[0]
        email = f"{prenom.lower()}.{lettre.lower()}{i+1}@automatisations.org"
        mdp = "Automatisation1!"
        
        try:
            cur.execute("""INSERT INTO comptes 
                (portfolio_id, email, mot_de_passe, reseau, pseudo, statut)
                VALUES (%s, %s, %s, 'facebook', %s, 'en_attente')""",
                (portfolio_id, email, mdp, f"@{prenom}.{lettre.lower()}{i+1}"))
            emails.append({'email': email, 'prenom': prenom, 'mdp': mdp})
        except Exception as e:
            print(f"  ⚠️ {email} déjà existant")
    
    conn.commit()
    conn.close()
    
    print(f"✅ {len(emails)} emails générés pour le Portfolio #{portfolio_id}")
    for e in emails:
        print(f"  {e['email']} - {e['prenom']}")
    
    return emails

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "dashboard":
            dashboard()
        elif cmd == "creer_portfolio":
            num = int(sys.argv[2]) if len(sys.argv) > 2 else 2
            proxy = sys.argv[3] if len(sys.argv) > 3 else None
            pid = creer_portfolio(num, proxy)
            if pid:
                ajouter_email(pid)
        elif cmd == "generer_emails":
            pid = int(sys.argv[2])
            ajouter_email(pid)
        else:
            print("Commandes: dashboard, creer_portfolio <num>, generer_emails <portfolio_id>")
    else:
        dashboard()
