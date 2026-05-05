"""
Utilitaire de signalement pour les agents.
Permet à n'importe quel agent de logger une anomalie
qui sera détectée par le Superviseur.
"""

import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'le-lab.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def signaler(niveau, source, message, details=None):
    """
    Signale une anomalie. Le Superviseur la détectera à son prochain passage.
    
    Args:
        niveau: 'info', 'warning', 'error', 'critical'
        source: Nom de l'agent ou du module
        message: Description courte
        details: Infos supplémentaires (optionnel, dict ou str)
    """
    if niveau not in ('info', 'warning', 'error', 'critical'):
        niveau = 'info'
    
    if details and isinstance(details, dict):
        details = str(details)
    
    conn = get_db()
    conn.execute(
        "INSERT INTO logs (niveau, source, message, details) VALUES (?, ?, ?, ?)",
        (niveau, source, message, details)
    )
    conn.commit()
    conn.close()
    
    # Affiche un résumé pour le terminal
    icones = {'info': 'ℹ️', 'warning': '⚠️', 'error': '❌', 'critical': '🚨'}
    print(f"{icones.get(niveau, 'ℹ️')} [{source}] {message}")

def erreur_critique(source, message, details=None):
    """Raccourci pour une erreur critique."""
    signaler('critical', source, message, details)

def avertissement(source, message, details=None):
    """Raccourci pour un avertissement."""
    signaler('warning', source, message, details)

def information(source, message, details=None):
    """Raccourci pour une information."""
    signaler('info', source, message, details)
