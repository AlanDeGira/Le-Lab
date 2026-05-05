# Heartbeat — Tâches périodiques

Routines exécutées lors des heartbeats (2-4 fois par jour).

## Routines

### 1. Watcher mail
```json
{
  "check": "pgrep -f mail_watch.py && echo '🟢 OK' || echo '🔴 MORT'",
  "period": "chaque heartbeat (~30min)",
  "action_if_dead": "relancer : cd ~/le-lab/agents/mail && python3 mail_watch.py &"
}
```

### 2. Docker santé
```json
{
  "check": "docker ps --format '{{.Names}} {{.Status}}' | grep -c 'Up'",
  "period": "quotidien (1x)",
  "alert": "si < 20 containers Up → alerte Kevyn"
}
```

### 3. Coûts API (DeepSeek)
```json
{
  "check": "lire les stats DeepSeek | mettre à jour TOOLS.md",
  "period": "quotidien (1x), en fin de journée",
  "note": "manuel pour l'instant — à automatiser"
}
```

### 4. Maintenance mémoire
```json
{
  "check": "lire memory/YYYY-MM-DD.md du jour (si existe) et distiller dans MEMORY.md",
  "period": "hebdomadaire (dimanche soir idéalement)",
  "note": "éviter les daily files obsolètes"
}
```

### 5. Git status
```json
{
  "check": "cd /root/.openclaw/workspace && git status --short",
  "period": "fin de session ou heartbeat lente",
  "action": "git add -A && git commit -m '[date] heartbeat maintenance' && git push origin main"
}
```

## Principe général

- **Batch** les vérifications plutôt que de faire des appels séparés
- **NO_REPLY** si rien d'urgent — ne pas déranger Kevyn pour des stats
- **Alerte** seulement si un service est DOWN (watcher, Docker, disque)
- **Horaires calmes :** 23:00-08:00 → NO_REPLY sauf urgence absolue

---

*Mis à jour le 5 mai 2026 — Routines définies par sub-agent projet-core-worker*
