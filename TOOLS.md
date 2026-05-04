# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Exemple

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Règles de diagnostic — Infrastructure

**Règle n°1 — Toujours vérifier Docker d'abord.**

Beaucoup de services sur ce VPS tournent en containers : Mailcow (Postfix, Dovecot, SOGo, Rspamd), Ollama, etc. Ne jamais conclure qu'un service est absent parce que le binaire système n'existe pas ou que systemctl ne le voit pas. Commencer par :
```
docker ps -a --format 'table {{.Names}}\t{{.Status}}'
```

**Règle n°2 — Vérifier les ports ouverts**
```
ss -tlnp | grep -E ':25|:143|:993|:587|:465'
```
Si un port SMTP/IMAP répond, le service est là — peu importe comment.

**Règle n°3 — Connaître les chemins Docker de ce serveur**
- Mailcow : `/opt/mailcow-dockerized/`
- MySQL Mailcow : `mailcowdockerized-mysql-mailcow-1` (port 13306 sur l'hôte)
- Volumes de données : sous `/opt/mailcow-dockerized/data/`

## Services conteneurisés sur ce VPS

| Service | Container(s) | Infos |
|---------|-------------|-------|
| Mailcow | postfix, dovecot, sogo, rspamd, mysql, redis, ... | 18 containers, `/opt/mailcow-dockerized/` |
| Ollama | ollama | Port 11434 |
| Watcher mail | mail_watch.py (PID variable) | `le-lab/agents/mail/mail_watch.py` |

### Watcher mail
- **Script :** le-lab/agents/mail/mail_watch.py
- **Commande status :** `python3 mail_watch.py --status`
- **Commande check :** `python3 mail_watch.py --check-last 5`
- **Commande lecture :** `python3 mail_watch.py --read-mail <id>`
- **Rapport :** data/mail_watch_report.json
- **Corps mails :** data/mails/

## 💰 Coût API quotidien

Suivi du coût DeepSeek (modèle deepseek-v4-flash) :

| Date | Coût | Requêtes | Output tokens | Cache hit | Cache miss |
|------|------|----------|---------------|-----------|------------|
| 2026-05-01 | $0.39 | 136 | 45 025 | 4 676 352 | 2 580 800 |
| 2026-05-02 | $1.97 | 773 | 166 175 | 31 094 912 | 13 081 886 |
| 2026-05-03 | $0.88 | 377 | 160 244 | 17 455 488 | 5 639 352 |
| 2026-05-04 | $0.77 | 528 | 158 761 | 23 749 504 | 4 698 990 |
| **Total mai** | **$4.00** | **1 814** | **530 205** | **77M** | **26M** |

### Stratégies pour réduire le coût

1. **Compacter plus souvent** — les sessions longues accumulent du contexte (input), coûtent cher en cache miss
2. **Éviter les sessions inutiles** — une requête = coût même minimal
3. **Utiliser le sub-agent pour les tâches isolées** — ses tokens ne s'ajoutent pas au contexte parent
4. **HEARTBEAT :** ne pas répondre quand rien à dire (NO_REPLY évite un tour de contexte)
5. **Privilégier les fichiers .md pour la mémoire** plutôt que de tout recharger à chaque session

### Actions concrètes
- [ ] Regrouper les questions en un seul message plutôt que plusieurs petits
- [ ] Utiliser `--check-last` ponctuellement, pas `--check-now` systématique
- [ ] Mettre à jour ce tableau quotidiennement

## Related

- [Agent workspace](/concepts/agent-workspace)
