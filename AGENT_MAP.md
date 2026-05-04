# AGENT_MAP.md — Cartographie des agents et outils

Fichier de référence, mis à jour à chaque création/modification d'agent.
Consulté au démarrage pour avoir une vue d'ensemble de l'infrastructure.

---

## Agents Python (scripts autonomes)

### Agent Création de Comptes
- **Fichier :** `le-lab/agents/communication/agent-creation-comptes.py`
- **Rôle :** Génère les 26 portfolios (Adam → Zoé) avec leurs comptes dans la BDD SQLite
- **Mot de passe pattern :** `{Prénom}1!` (publication), `{Prénom}.admin1!` (strateur)
- **BDD :** `le-lab/data/le-lab.db` (SQLite)
- **Tables :** `comptes`, `portfolios`, `logs`, `vue_etat_global`
- **Actions :** `dashboard`, `generer`, `portfolio <num>`

### Module Mailcow (création boîtes mail)
- **Fichier :** `le-lab/agents/communication/mailcow.py`
- **Rôle :** Interface avec Mailcow pour créer les boîtes mail sur `automatisations.org`
- **Méthodes :** `creer_boite(email, nom, password)`, `creer_boites_portfolio(prenom, suffixe, mdp)`, `generer_hash_mdp(password)`
- **Connexion :** MySQL via Docker (DB mailcow)
- **⚠️ Mots de passe :** Hashés en BLF-CRYPT avant insertion, pas de stockage en clair
- **À corriger :** Stocker les mots de passe en clair dans `comptes.mot_de_passe`

### Agent Superviseur
- **Fichier :** `le-lab/agents/superviseur/agent-superviseur.py`
- **Rôle :** Centralise les anomalies, filtre les doublons, prend des décisions automatiques
- **BDD :** `le-lab/data/le-lab.db` (SQLite)
- **Décisions :** Suspension portfolio (≥3 bloqués), alerte (≥3 shadowban)
- **Sortie :** Écrit `data/alerte_sortie.json` pour transmission Telegram

---

## Agents OpenClaw

### Main (moi, Alan de Gira)
- **ID :** `main`
- **Rôle :** Interface Telegram directe avec Kevyn, accès shell/serveur
- **Accès :** Docker, MySQL, Mailcow API, base `le_lab`, GitHub
- **Documentation :** SOUL.md (personnalité), TOOLS.md (règles de diagnostic), AGENT_MAP.md (ce fichier)

*À créer / enregistrer dans la config OpenClaw :*
- [ ] Agent Mail OTP — vérification et lecture des boîtes mail

---

## Infrastructure serveur

### VPS Contabo
- **OS :** Ubuntu 22.04
- **Domaine :** automatisations.org (Cloudflare)
- **IP :** 158.220.111.110

### Docker
| Service | Détail |
|---------|--------|
| **Mailcow** | 18 containers, `/opt/mailcow-dockerized/` |
| Postfix | SMTP (ports 25, 465, 587) |
| Dovecot | IMAP (ports 143, 993) |
| SOGo | Webmail (https://mail.automatisations.org/SOGo) |
| Rspamd | Antispam + DKIM |
| MySQL Mailcow | `mailcowdockerized-mysql-mailcow-1`, port 13306 hôte |
| Redis Mailcow | Cache sessions |
| **n8n** | Automatisations, port 5678 |
| **Ollama** | LLM local, port 11434 |

### BDD
| Base | Type | Usage |
|------|------|-------|
| `le_lab` (MySQL hôte) | MySQL | Portfolios, comptes, publications |
| `mailcow` (MySQL Docker) | MySQL | Boîtes mail Mailcow |
| `n8n` (PostgreSQL Docker) | PostgreSQL | Workflows n8n |

### DNS Cloudflare
- NS : clint.ns.cloudflare.com / nina.ns.cloudflare.com
- MX : mail.automatisations.org (prio 10)
- SPF : v=spf1 mx ~all
- DKIM : mail._domainkey (Rspamd)
- DMARC : p=none

### Corrections Postfix appliquées
- `smtputf8_enable = no` (conflit Dovecot)
- `smtp_bind_address = 0.0.0.0` (IPv4 forcé, Gmail rejette IPv6 sans PTR)

---

## Comptes mail (318 boîtes)

### 312 boîtes publication
26 prénoms × 12 suffixes :
- **Web/App :** app, web, fr
- **Projets :** hub, labs, studio
- **Média :** media, news, ideaz, idies
- **Business :** biz
- **Admin :** strateur

### 6 boîtes système
- `admin@automatisations.org` — Admin Mailcow
- `contact@automatisations.org` — Contact
- `otp@automatisations.org` — Bot OTP
- `test@automatisations.org` — Test
- `validation@automatisations.org` — Validation
- `alan.degira@automatisations.org` — Alan personnelle

### Portfolios (26)
| # | Lettre | Prénom |
|---|--------|--------|
| 1 | A | Adam |
| 2 | B | Baptiste |
| 3 | C | Camille |
| 4 | D | Diane |
| 5 | E | Émile |
| 6 | F | Flora |
| 7 | G | Gabriel |
| 8 | H | Hugo |
| 9 | I | Iris |
| 10 | J | Jules |
| 11 | K | Karine |
| 12 | L | Léo |
| 13 | M | Manon |
| 14 | N | Nathan |
| 15 | O | Oscar |
| 16 | P | Paul |
| 17 | Q | Quentin |
| 18 | R | Romane |
| 19 | S | Sacha |
| 20 | T | Théo |
| 21 | U | Ulysse |
| 22 | V | Valentin |
| 23 | W | William |
| 24 | X | Xander |
| 25 | Y | Yasmine |
| 26 | Z | Zoé |

---

## ## 🔄 Checklist démarrage de session

Avant de répondre à Kevyn, exécuter :

```bash
# 1. Vérifier Docker
docker ps -a --format 'table {{.Names}}\t{{.Status}}'

# 2. Vérifier les ports actifs
ss -tlnp | grep -E ':25|:80|:143|:443|:993|:587|:465|:5678|:11434|:13306'

# 3. Vérifier les bases actives
mysql -e "SHOW DATABASES;" 2>/dev/null

# 4. Vérifier GitHub
git status --short

# 5. Consulter AGENT_MAP.md (ce fichier)
# 6. Consulter TOOLS.md
```

---

## 📋 À faire (checklist persistante)
- [ ] Stocker mots de passe mail en clair dans `comptes` (mailcow.py)
- [ ] Tester émission/réception 318 boîtes (par strateur)
- [ ] Créer agent Mail OTP OpenClaw
- [ ] Créer comptes Facebook à la main
