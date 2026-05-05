#!/usr/bin/env python3
"""
Agent Superviseur — Centralise les anomalies, les filtre, et alerte.
Appelé par les autres agents via des signaux simples.
"""

import sqlite3
import os
import sys
import json
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'le-lab.db')
ALERTES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'alertes.json')

# Seuils de tolérance
SEUIL_ERREURS_PORTFOLIO = 3   # Au-delà, le portfolio est suspendu
SEUIL_SHADOWBAN_PORTFOLIO = 3 # Au-delà, alerte
FENETRE_ALERTE_HEURES = 1     # Pas de doublon dans cette fenêtre

NIVEAUX = {
    'critical': '🔴',
    'warning': '🟡',
    'info': '🔵',
}

# ─── BDD ────────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ─── FILTRE ANTI-DOUBLON ────────────────────────────────────────────────────

def _charger_alertes():
    """Charge l'historique des alertes envoyées."""
    if not os.path.exists(ALERTES_PATH):
        return []
    with open(ALERTES_PATH, 'r') as f:
        return json.load(f)

def _sauver_alertes(alertes):
    with open(ALERTES_PATH, 'w') as f:
        json.dump(alertes, f, indent=2)

def _est_deja_envoye(type_alerte, reference):
    """Vérifie si une alerte similaire a été envoyée dans la fenêtre."""
    alertes = _charger_alertes()
    maintenant = datetime.now()
    for a in alertes:
        if a['type'] == type_alerte and a['reference'] == reference:
            date_alerte = datetime.fromisoformat(a['date'])
            if maintenant - date_alerte < timedelta(hours=FENETRE_ALERTE_HEURES):
                return True
    return False

def _enregistrer_alerte(type_alerte, reference):
    alertes = _charger_alertes()
    alertes.append({
        'type': type_alerte,
        'reference': reference,
        'date': datetime.now().isoformat(),
    })
    # Garder seulement les 100 dernières
    _sauver_alertes(alertes[-100:])

# ─── DÉTECTION DES ANOMALIES ────────────────────────────────────────────────

def analyser_logs():
    """Analyse les logs récents et retourne les anomalies détectées."""
    anomalies = []
    conn = get_db()
    cur = conn.cursor()
    
    # 1. Logs d'erreur dans les dernières 24h
    cur.execute("""
        SELECT niveau, source, message, details, date
        FROM logs
        WHERE date >= datetime('now', '-24 hours')
        ORDER BY date DESC
    """)
    
    for log in cur.fetchall():
        if log['niveau'] in ('error', 'critical'):
            anomalies.append({
                'type': 'log',
                'niveau': log['niveau'],
                'source': log['source'],
                'message': log['message'],
                'details': log['details'],
                'date': log['date'],
            })
    
    # 2. Comptes problématiques
    cur.execute("""
        SELECT c.id, c.email, c.reseau, c.statut, c.suffixe, p.prenom, p.numero
        FROM comptes c
        JOIN portfolios p ON c.portfolio_id = p.id
        WHERE c.statut IN ('bloque', 'shadowban', 'a_verifier')
    """)
    
    comptes_problemes = cur.fetchall()
    if comptes_problemes:
        # Grouper par portfolio
        portfolios = {}
        for c in comptes_problemes:
            key = c['numero']
            if key not in portfolios:
                portfolios[key] = {'prenom': c['prenom'], 'comptes': []}
            portfolios[key]['comptes'].append(c)
        
        for num, data in portfolios.items():
            total = len(data['comptes'])
            nb_bloque = sum(1 for c in data['comptes'] if c['statut'] == 'bloque')
            nb_shadow = sum(1 for c in data['comptes'] if c['statut'] == 'shadowban')
            nb_verif = sum(1 for c in data['comptes'] if c['statut'] == 'a_verifier')
            
            niveau = 'critical' if nb_bloque > 0 else 'warning'
            
            anomalies.append({
                'type': 'comptes_problemes',
                'niveau': niveau,
                'source': f"portfolio_{num}",
                'message': f"Portfolio #{num} {data['prenom']}: {total} comptes problématiques "
                          f"({nb_bloque} bloqués, {nb_shadow} shadowban, {nb_verif} à vérifier)",
                'details': [{'email': c['email'], 'reseau': c['reseau'], 'statut': c['statut']} for c in data['comptes']],
            })
    
    conn.close()
    return anomalies

# ─── DÉCISIONS AUTOMATIQUES ────────────────────────────────────────────────

def appliquer_actions(anomalies):
    """Prend des décisions automatiques selon les anomalies."""
    actions = []
    conn = get_db()
    cur = conn.cursor()
    
    for anom in anomalies:
        if anom['type'] == 'comptes_problemes':
            # Extraire le numéro du portfolio
            source = anom['source']
            if source.startswith('portfolio_'):
                num = int(source.split('_')[1])
                
                # Si trop d'erreurs, suspendre le portfolio
                cur.execute("""
                    SELECT COUNT(*) as c FROM comptes c
                    JOIN portfolios p ON c.portfolio_id = p.id
                    WHERE p.numero = ? AND c.statut = 'bloque'
                """, (num,))
                nb_bloque = cur.fetchone()['c']
                
                if nb_bloque >= SEUIL_ERREURS_PORTFOLIO:
                    cur.execute("UPDATE portfolios SET statut='suspendu' WHERE numero=?", (num,))
                    conn.commit()
                    actions.append(f"🔴 Portfolio #{num} suspendu ({nb_bloque} comptes bloqués)")
                
                # Si trop de shadowban, alerte warning
                cur.execute("""
                    SELECT COUNT(*) as c FROM comptes c
                    JOIN portfolios p ON c.portfolio_id = p.id
                    WHERE p.numero = ? AND c.statut = 'shadowban'
                """, (num,))
                nb_shadow = cur.fetchone()['c']
                
                if nb_shadow >= SEUIL_SHADOWBAN_PORTFOLIO:
                    actions.append(f"🟡 Portfolio #{num} : {nb_shadow} shadowban")
    
    conn.close()
    return actions

# ─── FORMAT POUR TELEGRAM ──────────────────────────────────────────────────

def formater_message(anomalies, actions):
    """Formate un message prêt à envoyer."""
    if not anomalies and not actions:
        return None
    
    lignes = ["🔍 **Rapport Superviseur**"]
    lignes.append(f"_{datetime.now().strftime('%d/%m/%Y %H:%M')}_\n")
    
    if actions:
        lignes.append("**⚡ Actions automatiques :**")
        for a in actions:
            lignes.append(f"  {a}")
        lignes.append("")
    
    # Filtrer les anomalies critiques (les autres sont juste loggées)
    alertes = [a for a in anomalies if a['niveau'] in ('critical', 'warning')]
    
    if alertes:
        lignes.append(f"**⚠️ Alertes ({len(alertes)}) :**")
        for a in alertes:
            icone = NIVEAUX.get(a['niveau'], '🔵')
            lignes.append(f"  {icone} **{a['source']}** : {a['message']}")
    
    if len(anomalies) > len(alertes):
        lignes.append(f"\n_+ {len(anomalies) - len(alertes)} anomalies mineures (loggées)_")
    
    return "\n".join(lignes)

# ─── ENVOI ─────────────────────────────────────────────────────────────────

def envoyer_alerte(message):
    """Écrit l'alerte dans un fichier JSON que le session listener peut lire."""
    payload = {
        'type': 'alerte_superviseur',
        'message': message,
        'date': datetime.now().isoformat(),
    }
    
    alertes = _charger_alertes()
    # On ne stocke que les messages dans un fichier dédié
    sortie = os.path.join(os.path.dirname(DB_PATH), 'alerte_sortie.json')
    with open(sortie, 'w') as f:
        json.dump(payload, f, indent=2)
    
    print(f"[SUPERVISEUR] Alerte écrite dans {sortie}")
    print(message)

# ─── POINT D'ENTRÉE ────────────────────────────────────────────────────────

def superviser():
    """Tour principal de supervision."""
    anomalies = analyser_logs()
    actions = appliquer_actions(anomalies)
    
    message = formater_message(anomalies, actions)
    if message:
        # Vérifier qu'on n'a pas déjà envoyé ce message récemment
        if not _est_deja_envoye('supervision', datetime.now().strftime('%Y%m%d')):
            envoyer_alerte(message)
            _enregistrer_alerte('supervision', datetime.now().strftime('%Y%m%d'))
    
    return len(anomalies), len(actions)

if __name__ == "__main__":
    nb_anomalies, nb_actions = superviser()
    print(f"[SUPERVISEUR] {nb_anomalies} anomalies détectées, {nb_actions} actions appliquées")
