# Agent Superviseur

## Rôle
Centraliser, filtrer et qualifier les anomalies remontées par tous les autres agents.
Prendre des décisions automatiques pour limiter les dégâts.
Transmettre les alertes critiques à Kevyn.

## Fonctionnement

1. **Analyse** : scanne les logs de la BDD toutes les heures
2. **Détection** : repère les comptes bloqués, shadowban, à vérifier
3. **Décision** : applique des actions automatiques (suspension de portfolio, etc.)
4. **Alerte** : transmet les anomalies critiques à Kevyn

## Règles de remontée

| Niveau | Critère | Action |
|--------|---------|--------|
| 🔴 Critique | Compte bloqué, proxy mort, échec publication | Alerte immédiate |
| 🟡 Important | Shadowban, ralentissement, vérification en cours | Résumé quotidien |
| 🔵 Info | Compte créé, publication réussie, portfolio actif | Log BDD uniquement |

## Décisions automatiques

| Seuil | Action |
|-------|--------|
| ≥3 comptes bloqués dans un portfolio | Portfolio suspendu |
| ≥3 shadowban dans un portfolio | Alerte Kevyn |
| >3 échecs consécutifs publication | Alerte immédiate |

## Anti-doublon
Une alerte identique ne peut pas être envoyée plus d'une fois par heure.

## Communication
- Écrit un fichier `alerte_sortie.json` quand une alerte doit être transmise
- Un listener (via le cron OpenClaw) peut surveiller ce fichier et envoyer le message Telegram

## Commandes
- `python3 agent-superviseur.py` — Lance une supervision
