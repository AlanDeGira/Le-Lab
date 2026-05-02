#!/usr/bin/env python3
"""
le-lab Database Manager
Gère la base de données SQLite du projet Le Lab.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'le-lab.db')

def get_db():
    """Retourne une connexion à la base"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ajouter_portfolio(numero, nom=None, proxy=None):
    """Crée un nouveau portfolio (groupe de 10 comptes)"""
    if not nom:
        nom = f"Portfolio {numero}"
    conn = get_db()
    conn.execute("INSERT INTO portfolios (nom, numero, proxy) VALUES (?, ?, ?)",
                 (nom, numero, proxy))
    conn.commit()
    conn.close()

def ajouter_compte(portfolio_id, email, mot_de_passe, reseau, pseudo=None):
    """Ajoute un compte social à un portfolio"""
    conn = get_db()
    conn.execute("""INSERT INTO comptes 
        (portfolio_id, email, mot_de_passe, reseau, pseudo) 
        VALUES (?, ?, ?, ?, ?)""",
        (portfolio_id, email, mot_de_passe, reseau, pseudo))
    conn.commit()
    conn.close()

def ajouter_video(fichier, chemin, duree=None, theme=None, portfolio_id=None):
    """Ajoute une vidéo à la bibliothèque"""
    conn = get_db()
    conn.execute("""INSERT INTO videos 
        (fichier, chemin, duree_secondes, theme, portfolio_id) 
        VALUES (?, ?, ?, ?, ?)""",
        (fichier, chemin, duree, theme, portfolio_id))
    conn.commit()
    conn.close()

def log(niveau, source, message, details=None):
    """Ajoute une entrée de log"""
    conn = get_db()
    conn.execute("INSERT INTO logs (niveau, source, message, details) VALUES (?, ?, ?, ?)",
                 (niveau, source, message, details))
    conn.commit()
    conn.close()

def enregistrer_publication(compte_id, video_id, date_prevue, statut='planifie'):
    """Planifie ou enregistre une publication"""
    conn = get_db()
    conn.execute("""INSERT INTO publications 
        (compte_id, video_id, date_prevue, statut) 
        VALUES (?, ?, ?, ?)""",
        (compte_id, video_id, date_prevue, statut))
    conn.commit()
    conn.close()

def dashboard():
    """Affiche un résumé de l'état du système"""
    conn = get_db()
    cur = conn.cursor()
    
    print("=" * 50)
    print("📊 DASHBOARD LE LAB")
    print("=" * 50)
    
    cur.execute("SELECT * FROM vue_etat_global")
    row = cur.fetchone()
    if row:
        print(f"Comptes totaux:      {row['total_comptes']}")
        print(f"Comptes actifs:      {row['comptes_actifs']}")
        print(f"Comptes bloqués:     {row['comptes_bloques']}")
        print(f"Portfolios:          {row['total_portfolios']}")
        print(f"Publications réussies: {row['pubs_reussies']}")
        print(f"Publications échouées: {row['pubs_echouees']}")
    
    print("\n--- Portfolios ---")
    cur.execute("SELECT id, nom, numero, statut FROM portfolios")
    for p in cur.fetchall():
        cur.execute("SELECT COUNT(*) as c FROM comptes WHERE portfolio_id=?", (p['id'],))
        nb = cur.fetchone()['c']
        print(f"  #{p['numero']} {p['nom']} [{p['statut']}] - {nb} comptes")
    
    conn.close()

if __name__ == "__main__":
    dashboard()
