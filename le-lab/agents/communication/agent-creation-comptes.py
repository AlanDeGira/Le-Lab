#!/usr/bin/env python3
"""
Agent Création de Comptes v2
Génère les 26 portfolios et leurs comptes dans la BDD.
Signale les anomalies au Superviseur.
"""

import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'le-lab.db')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from signalement import signaler, erreur_critique, avertissement

# ─── CONFIGURATION GLOBALE ───────────────────────────────────────────────────

SUFFIXES = ['reel', 'story', 'content', 'media', 'feed', 'post', 'daily', 'vibe', 'style', 'life']
SUFFIXE_ADMIN = 'strateur'
MDP_SUFFIXE = '1!'
MDP_ADMIN_SUFFIXE = '.admin1!'
DATE_NAISSANCE = '1990-01-01'

PRENOMS = {
    1:  ('A', 'Adam'),
    2:  ('B', 'Baptiste'),
    3:  ('C', 'Camille'),
    4:  ('D', 'Diane'),
    5:  ('E', 'Émile'),
    6:  ('F', 'Flora'),
    7:  ('G', 'Gabriel'),
    8:  ('H', 'Hugo'),
    9:  ('I', 'Iris'),
    10: ('J', 'Jules'),
    11: ('K', 'Karine'),
    12: ('L', 'Léo'),
    13: ('M', 'Manon'),
    14: ('N', 'Nathan'),
    15: ('O', 'Oscar'),
    16: ('P', 'Paul'),
    17: ('Q', 'Quentin'),
    18: ('R', 'Romane'),
    19: ('S', 'Sacha'),
    20: ('T', 'Théo'),
    21: ('U', 'Ulysse'),
    22: ('V', 'Valentin'),
    23: ('W', 'William'),
    24: ('X', 'Xander'),
    25: ('Y', 'Yasmine'),
    26: ('Z', 'Zoé'),
}

SOURCE = 'creation_comptes'

# ─── BDD ────────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ─── PORTFOLIOS ─────────────────────────────────────────────────────────────

def creer_portfolio(numero, proxy=None):
    """Crée un portfolio avec son prénom et lettre."""
    if numero not in PRENOMS:
        erreur_critique(SOURCE, f"Tentative création portfolio #{numero} invalide (1-26)")
        return None

    lettre, prenom = PRENOMS[numero]
    nom = f"Portfolio {lettre} — {prenom}"

    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO portfolios (nom, numero, lettre, prenom, proxy, statut) VALUES (?, ?, ?, ?, ?, 'en_creation')",
            (nom, numero, lettre, prenom, proxy)
        )
        portfolio_id = cur.lastrowid
        conn.commit()
        signaler('info', SOURCE, f"Portfolio #{numero} '{nom}' créé",
                 {'portfolio_id': portfolio_id, 'numero': numero, 'prenom': prenom})
        return portfolio_id
    except Exception as e:
        erreur_critique(SOURCE, f"Échec création portfolio #{numero}", str(e))
        return None
    finally:
        conn.close()

def generer_comptes(portfolio_id):
    """Génère les 10 comptes publication + 1 admin pour un portfolio."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT numero, prenom FROM portfolios WHERE id=?", (portfolio_id,))
    p = cur.fetchone()
    if not p:
        erreur_critique(SOURCE, f"Portfolio #{portfolio_id} introuvable")
        conn.close()
        return

    numero = p['numero']
    prenom = p['prenom']
    mdp = f"{prenom}{MDP_SUFFIXE}"
    mdp_admin = f"{prenom}{MDP_ADMIN_SUFFIXE}"

    comptes_crees = 0
    erreurs = 0

    for suffixe in SUFFIXES:
        email = f"{prenom.lower()}.{suffixe}@automatisations.org"
        nom_page = f"{prenom} {suffixe.capitalize()}"

        try:
            cur.execute("""
                INSERT INTO comptes 
                (portfolio_id, email, suffixe, mot_de_passe, nom_page, reseau, statut, role, date_de_naissance)
                VALUES (?, ?, ?, ?, ?, 'facebook_page', 'en_attente', 'publication', ?)
            """, (portfolio_id, email, suffixe, mdp, nom_page, DATE_NAISSANCE))

            pseudo_ig = f"{prenom.lower()}_{suffixe}"
            cur.execute("""
                INSERT INTO comptes 
                (portfolio_id, email, suffixe, mot_de_passe, reseau, pseudo_instagram, statut, role, date_de_naissance)
                VALUES (?, ?, ?, ?, 'instagram', ?, 'en_attente', 'publication', ?)
            """, (portfolio_id, email, suffixe, mdp, pseudo_ig, DATE_NAISSANCE))

            cur.execute("""
                INSERT INTO comptes 
                (portfolio_id, email, suffixe, mot_de_passe, reseau, statut, role, date_de_naissance)
                VALUES (?, ?, ?, ?, 'tiktok', 'en_attente', 'publication', ?)
            """, (portfolio_id, email, suffixe, mdp, DATE_NAISSANCE))

            comptes_crees += 3
        except Exception as e:
            erreurs += 1
            avertissement(SOURCE, f"Échec insertion {email}", str(e))

    email_admin = f"{prenom.lower()}.{SUFFIXE_ADMIN}@automatisations.org"
    nom_page_admin = f"{prenom} Administration"
    try:
        cur.execute("""
            INSERT INTO comptes 
            (portfolio_id, email, suffixe, mot_de_passe, nom_page, reseau, statut, role, date_de_naissance)
            VALUES (?, ?, ?, ?, ?, 'facebook_page', 'en_attente', 'admin', ?)
        """, (portfolio_id, email_admin, SUFFIXE_ADMIN, mdp_admin, nom_page_admin, DATE_NAISSANCE))
        comptes_crees += 1
    except Exception as e:
        erreurs += 1
        erreur_critique(SOURCE, f"Échec insertion admin {email_admin}", str(e))

    cur.execute("UPDATE portfolios SET statut='actif' WHERE id=?", (portfolio_id,))
    conn.commit()
    conn.close()

    signaler('info' if erreurs == 0 else 'warning', SOURCE,
             f"Portfolio {prenom} — {comptes_crees} comptes créés, {erreurs} erreurs",
             {'portfolio_id': portfolio_id, 'prenom': prenom, 'total': comptes_crees, 'erreurs': erreurs})

# ─── DASHBOARD ──────────────────────────────────────────────────────────────

def dashboard():
    conn = get_db()
    cur = conn.cursor()

    print("=" * 60)
    print("📊 AGENT CRÉATION DE COMPTES — DASHBOARD")
    print("=" * 60)

    cur.execute("SELECT * FROM vue_etat_global")
    row = cur.fetchone()
    if row:
        for k in row.keys():
            print(f"  {k}: {row[k]}")

    print("\n📋 Portfolios :")
    cur.execute("SELECT * FROM vue_portfolio_detail ORDER BY numero")
    for p in cur.fetchall():
        print(f"  #{p['numero']} [{p['lettre']}] {p['prenom']:10s} — "
              f"{p['total_comptes']:2d} comptes ({p['actifs']} actifs, {p['bloques']} bloqués) "
              f"FB:{p['facebook']} IG:{p['instagram']} TK:{p['tiktok']}")

    print("\n⚠️  Comptes problématiques :")
    cur.execute("""
        SELECT c.email, c.reseau, c.statut, c.suffixe, p.prenom
        FROM comptes c JOIN portfolios p ON c.portfolio_id = p.id
        WHERE c.statut IN ('bloque', 'shadowban', 'a_verifier')
        ORDER BY c.date_creation DESC
    """)
    problemes = cur.fetchall()
    if problemes:
        for c in problemes:
            print(f"  🔴 {c['prenom']}.{c['suffixe']} ({c['reseau']}) — {c['statut']}")
    else:
        print("  ✅ Rien à signaler")

    conn.close()

# ─── CLI ────────────────────────────────────────────────────────────────────

def generer_tout(proxy_par_portfolio=None):
    print("🚀 GÉNÉRATION COMPLÈTE — 26 PORTFOLIOS")
    proxies = proxy_par_portfolio or [None] * 26

    for numero in range(1, 27):
        proxy = proxies[numero - 1] if isinstance(proxies, list) else proxy_par_portfolio
        pid = creer_portfolio(numero, proxy)
        if pid:
            generer_comptes(pid)
        if numero < 26:
            print()

    signaler('info', SOURCE, f"Génération terminée — {26 * 31} comptes dans 26 portfolios")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        dashboard()
    else:
        cmd = sys.argv[1]
        if cmd == "dashboard":
            dashboard()
        elif cmd == "generer":
            generer_tout()
        elif cmd == "portfolio":
            num = int(sys.argv[2])
            pid = creer_portfolio(num)
            if pid:
                generer_comptes(pid)
        else:
            print("Commandes: dashboard, generer, portfolio <num>")
