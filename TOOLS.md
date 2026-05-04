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

## Related

- [Agent workspace](/concepts/agent-workspace)
