# Le Lab — Projet Commerce & Automatisation

**Commercialiser des produits e-commerce en ligne via un système automatisé de publication massive sur les réseaux sociaux (Meta, TikTok).**

---

## 🧭 Vue d'ensemble

Le projet repose sur **26 portfolios** (A → Z), chacun composé d'une identité unique. Chaque portfolio contient 10 comptes publication (Facebook + Instagram + TikTok) et 1 compte admin (strateur) qui gère le Business Portfolio Meta.

Architecture : [Voir le README Le Lab](./README.md)

---

## 📊 État d'avancement

### ✅ Terminé

| Élément | Statut | Détail |
|---------|--------|--------|
| Architecture des portfolios | ✅ | 26 portfolios, 1 prénom/portfolio, 10 suffixes |
| Schéma BDD v2 | ✅ | Tables : portfolios, comptes, videos, publications, logs |
| 1er agent (création de comptes) | ✅ | Génère les 806 comptes dans la BDD |
| Spécifications des comptes | ✅ | Emails, mots de passe, dates, rôles définis |
| Conditions obligatoires (agent publication) | ✅ | Instagram ↔ FB, Business Portfolio, Branded Content |
| Planning de création | ✅ | Pipeline J0→J5 validé |
| Documentation complète | ✅ | README, MD des agents, mémoire de session |

### 🔄 En cours

| Élément | Statut | Détail |
|---------|--------|--------|
| Phase de test — Portfolio A (Adam) | ⏳ | Test sur un seul portfolio avant scale |
| Génération des emails | ⏳ | À faire : création des boîtes sur automatisations.org |
| Outil de création automatisée | ⏳ | À faire : automate navigateur |
| Proxies | ⏳ | À faire : choisir fournisseur, tester 1 proxy |
| Numéros de téléphone | ⏳ | À faire : choisir fournisseur SMS |

### ❌ Bloqué / À faire

| Élément | Statut | Blocage | Solution envisagée |
|---------|--------|---------|-------------------|
| Création comptes Facebook | ❌ | Nécessite SMS + email + proxy | Test sur un seul portfolio d'abord |
| Création comptes TikTok | ❌ | Processus inconnu pour création en masse | Mis en attente, priorités Meta d'abord |
| YouTube | ❌ | Écosystème Google trop contraignant | Abandonné |

---

## 📐 Architecture

### 26 portfolios (A → Z)

| Portfolio | Prénom | Comptes publication | Compte admin | Total |
|-----------|--------|:-------------------:|:------------:|:-----:|
| A | Adam | 10 × (FB + IG + TK) | adam.strateur | 31 |
| B | Baptiste | 10 × (FB + IG + TK) | baptiste.strateur | 31 |
| ... | ... | ... | ... | ... |
| Z | Zoé | 10 × (FB + IG + TK) | zoe.strateur | 31 |
| **Total** | | **780** | **26** | **806** |

### Suffixes email (10 par portfolio)

`.reel`, `.story`, `.content`, `.media`, `.feed`, `.post`, `.daily`, `.vibe`, `.style`, `.life`

Format : `prenom.suffixe@automatisations.org`

### Mots de passe

- Comptes publication : `Prénom1!` (ex: `Adam1!`)
- Compte admin : `Prénom.admin1!` (ex: `Adam.admin1!`)
- Date de naissance unique : `1990-01-01`

---

## 📅 Planning de création (test)

Test sur le **Portfolio A (Adam)** avant de scaler :

| Jour | Action |
|------|--------|
| **J0** | Génération des 10 emails |
| **J1** | Création des 10 comptes Facebook |
| **J2** | Création des 10 comptes Instagram |
| **J3** | Création des 10 pages Facebook |
| **J4** | Liaison Instagram ↔ Page FB + Branded Content |
| **J5** | Strateur → BP Meta → Tous les comptes intégrés → marqués "actif" |

### Conditions obligatoires pour chaque compte

1. **Compte Instagram lié à sa page Facebook** — Vérifié via Meta Business Suite
2. **Compte intégré au Business Portfolio Meta** — Géré par le strateur
3. **Branded Content activé** — Permet le tracking via pixel Meta

---

## 🛠️ Agents

### Agent 1 — Création de Comptes
- **Fichier :** `agents/communication/agent-creation-comptes.py`
- **Rôle :** Génère les portfolios et leurs comptes dans la BDD
- **Commandes :** `dashboard`, `generer`, `portfolio <num>`

---

## 💾 Base de données

- **SQLite** → `data/le-lab.db`
- **Schéma :** `data/schema.sql`
- 6 tables : `portfolios`, `comptes`, `videos`, `publications`, `logs`
- 2 vues : `vue_etat_global`, `vue_portfolio_detail`

---

## 📝 Ressources nécessaires (estimation)

### Test (Portfolio A uniquement)

| Ressource | Quantité | Coût estimé |
|-----------|----------|-------------|
| Proxy résidentiel | 1 | ~3-5 €/mois |
| Numéros SMS | 10 | ~1-5 € |
| Photos de profil | 10 | ~0 € (IA) |

### Scale (26 portfolios)

| Ressource | Quantité | Coût estimé |
|-----------|----------|-------------|
| Proxies résidentiels | 26+ | ~80-130 €/mois |
| Numéros SMS | 260+ | ~26-130 € |
| Photos de profil | 260+ | ~0 € (IA) |

---

## 🔗 Contact

Projet piloté par Alan de Gira pour Kevyn.
