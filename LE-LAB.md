# 🧪 Le Lab — Plan de bataille

---

## 1. POURQUOI on fait ça

On veut commercialiser des produits e-commerce en ligne.

Pour vendre, il faut du trafic. Pour du trafic organique, il faut publier sur les réseaux sociaux. Beaucoup. Chaque jour.

Un seul compte = portée limitée. 300 comptes qui postent les mêmes réels = portée démultipliée.

**But final :** Un système automatisé où 300 comptes Facebook/Instagram/TikTok publient du contenu e-commerce 24/7 sans intervention humaine. Landing pages dynamiques. Pixel Meta. Tracking. Optimisation continue.

---

## 2. CE QU'ON VEUT FAIRE

Créer **806 comptes sociaux** répartis sur **26 portfolios** (A → Z).

Chaque portfolio = 1 identité fictive qui gère :
- 10 pages Facebook
- 10 comptes Instagram
- 10 comptes TikTok (en option)
- 1 compte admin Facebook (le "strateur") qui supervise via Meta Business Portfolio

**Totaux :** 260 comptes FB + 260 pages FB + 260 comptes IG + 26 admins = ~806

---

## 3. COMMENT on va le faire

### Phase 1 — Mettre en place les fondations

| Étape | Action | Pourquoi |
|-------|--------|----------|
| 1.1 | Serveur mail OTP (Postfix/Dovecot) | Chaque compte a besoin d'un email unique |
| 1.2 | Créer les 260 boîtes mail sur le serveur | Base de tout le reste |
| 1.3 | Choisir et acheter des proxies mobiles 4G | Sans proxy, Meta bloque en 5 secondes |
| 1.4 | Choisir et acheter un service SMS API | Obligatoire pour vérifier les comptes |
| 1.5 | Préparer photos de profil IA (260+ visages) | Comptes crédibles = comptes qui durent |

### Phase 2 — Test sur 1 portfolio (Adam)

| Étape | Action | Détail |
|-------|--------|--------|
| 2.1 | **J0** — Générer les 10 emails Adam | adam.reel@... → adam.life@... |
| 2.2 | **J1** — Créer 10 comptes Facebook | Avec proxy, SMS, captcha solver |
| 2.3 | **J2** — Créer 10 comptes Instagram | API mobile IG via SaeidB/insta_create |
| 2.4 | **J3** — Créer 10 pages Facebook | Via greikgk/FB-Pages-Creator (GraphQL) |
| 2.5 | **J4** — Lier IG ↔ Page FB + Branded Content | Obligatoire pour le pixel Meta |
| 2.6 | **J5** — Intégrer tout dans BP Meta via strateur | adam.strateur invite les 10 comptes |

**Si le test passe :** on scale.
**Si le test échoue :** on ajuste la méthode.

### Phase 3 — Scale à 26 portfolios

On reproduit la phase 2 × 26.

2 stratégies possibles :
- **Linéaire** : 1 portfolio après l'autre → ~5 mois
- **Parallèle** : plusieurs portfolios simultanément → ~1 mois

### Phase 4 — Warmup & Publication

| Étape | Action |
|-------|--------|
| 4.1 | Warmup manuel 15-30 min/compte (like, follow, scroll) |
| 4.2 | Déploiement bot TikTok warmup (iOS Voice Control) |
| 4.3 | Mise en place du planning de publication automatisé |
| 4.4 | Activation pixel Meta + tracking |

---

## 4. PROCESS à respecter pour chaque compte

**Règle n°1 :** Un compte = un proxy. Pas de partage.
**Règle n°2 :** Un compte = un email dédié. Pas de plus.

**Checklist création (obligatoire, chaque compte) :**
- [ ] Email unique créé sur le serveur mail
- [ ] Proxy assigné (mobile 4G)
- [ ] Profil randomisé (pdp IA, bio, date naissance 1990-01-01)
- [ ] Captcha résolu (via API)
- [ ] SMS vérifié (via API)
- [ ] Compte marqué "création" dans la BDD

**Checklist activation (obligatoire, chaque compte) :**
- [ ] Instagram lié à sa page Facebook (même suffixe)
- [ ] Compte intégré au Business Portfolio Meta
- [ ] Branded Content activé
- [ ] Compte marqué "actif" dans la BDD

---

## 5. CONVENTIONS (ne pas dévier)

| Élément | Valeur |
|---------|--------|
| Mot de passe publication | `Prénom1!` (ex: `Adam1!`) |
| Mot de passe admin | `Prénom.admin1!` (ex: `Adam.admin1!`) |
| Date de naissance | 1990-01-01 (tout le monde) |
| Suffixes email publication | `.reel`, `.story`, `.content`, `.media`, `.feed`, `.post`, `.daily`, `.vibe`, `.style`, `.life` |
| Suffixe email admin | `.strateur` |
| Domaine | automatisations.org |
| Format email | `prenom.suffixe@automatisations.org` |

---

## 6. OS & SERVICES QU'ON VA UTILISER

### Création
- **Instagram** : SaeidB/insta_create (Python, API mobile IG, testé 2025)
- **Pages Facebook** : greikgk/FB-Pages-Creator (Python, GraphQL, MAJ 03/05/2026)
- **Comptes Facebook** : DIY (Selenium/Puppeteer — rien d'OS fiable)
- **TikTok** : En attente (priorité Meta d'abord)

### Warmup
- **TikTok** : l-portet/tiktok-warmup-bot (iOS Voice Control)
- **IG/FB** : Manuel (15-30 min/jour/compte les 1res semaines)

### Services payants (incontournables)
- **Proxies** : Mobile 4G/5G (~3-5€/mois/unité)
- **SMS** : 5sim, SMSActivate, SMSPVA (~0.10-0.50€/numéro)
- **Captcha** : 2Captcha, AntiCaptcha (~0.50-2€/1000)

---

## 7. BUDGET

### Test (portfolio A, 1 seule fois)
| Poste | € |
|-------|:-:|
| 1 proxy mobile | 3-5 |
| 10 SMS | 1-5 |
| 0 photos IA | 0 |
| **Total** | **4-10** |

### Scale (26 portfolios, récurrent)
| Poste | Mensuel | Une fois |
|-------|:-------:|:--------:|
| 26 proxies | 80-130 | - |
| 260 SMS | - | 26-130 |
| 260 photos IA | - | 0 |
| **Total** | **80-130€/mois** | **26-130€** |

---

## 8. DÉPENDANCES CRITIQUES

**Sans serveur mail OTP → RIEN n'est possible.**
Les DNS du domaine `automatisations.org` pointent encore vers o2switch. Tant que Cloudflare n'est pas en place, on ne peut pas héberger le serveur mail sur le VPS.

**Blocage actuel :**
DNS automatisations.org → o2switch (à basculer vers Cloudflare)

---

## 9. FICHIERS DU PROJET

| Fichier | Contenu |
|---------|---------|
| `le-lab/README.md` | Vision, structure, 3 départements |
| `le-lab/DOCUMENTATION.md` | Documentation complète |
| `le-lab/data/schema.sql` | Schéma BDD (SQLite) |
| `le-lab/agents/communication/agent-creation-comptes.md` | Agent Python création |
| `le-lab/agents/superviseur/agent-superviseur.md` | Agent supervision |
| `mail-setup/docker-compose.yml` | Stack mail Postfix + Dovecot |
| `mail-setup/README.md` | Config mail OTP |
| `check-otp.sh` | Script récupération OTP |
| `create-mailbox.sh` | Script création boîtes mail |

---

## 10. DÉCISIONS PRISES (archives, ne pas revenir dessus)

- ❌ Pas de YouTube (écosystème Google trop contraignant)
- ❌ TikTok mis en attente (priorité Meta)
- ✅ Les comptes admin (strateur) n'ont pas d'Instagram ni TikTok
- ✅ 1 ligne BDD par réseau, relié par `id_identite`
