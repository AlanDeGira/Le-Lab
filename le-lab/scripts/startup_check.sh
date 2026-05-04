#!/usr/bin/env bash
# startup_check.sh — Exécuté au démarrage de session
# Résumé des agents, outils et infrastructure

echo "═══════════════════════════════════════════"
echo "  🔍 STARTUP CHECK — $(date '+%d/%m/%Y %H:%M')"
echo "═══════════════════════════════════════════"

echo ""
echo "─── 🐳 Docker ───"
docker ps -a --format 'table {{.Names}}\t{{.Status}}'

echo ""
echo "─── 🔌 Ports actifs ───"
ss -tlnp | grep -E ':25|:80|:143|:443|:993|:587|:465|:5678|:11434|:13306'

echo ""
echo "─── 🗄️  BDD ───"
mysql -e "SHOW DATABASES;" 2>/dev/null

echo ""
echo "─── 📂 Agents disponibles ───"
ls -1 /root/.openclaw/workspace/le-lab/agents/*/*.md 2>/dev/null
ls -1 /root/.openclaw/workspace/le-lab/agents/*/*.py 2>/dev/null

echo ""
echo "─── 📋 Git ───"
git -C /root/.openclaw/workspace status --short 2>/dev/null

echo ""
echo "─── 📖 Documentation ───"
echo "  AGENT_MAP.md → /root/.openclaw/workspace/AGENT_MAP.md"
echo "  SOUL.md      → /root/.openclaw/workspace/SOUL.md"
echo "  TOOLS.md     → /root/.openclaw/workspace/TOOLS.md"

echo ""
echo "═══════════════════════════════════════════"
echo "  ✅ Startup check terminé"
echo "═══════════════════════════════════════════"
