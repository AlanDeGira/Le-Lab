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
- 10 comptes Facebook
- 10 pages Facebook
- 10 comptes Instagram
- 10 comptes TikTok (en option, en attente)
- 1 compte admin Facebook (le "strateur") qui supervise via Meta Business Portfolio

**Totaux :** 260 comptes FB + 260 pages FB + 260 comptes IG + 26 admins = ~806

---

## 3. CE QUI EST FAIT

### Mail — ✅ Terminé (318 boîtes)

| Élément | Statut |
|---------|--------|
| Mailcow Docker installé | ✅ |
| 318 boîtes mail créées | ✅ (312 + 6 système) |
| DNS Cloudflare configurés | ✅ (MX, SPF, DKIM, DMARC) |
| Corrections Postfix | ✅ (SMTPUTF8, IPv4, attributes) |
| Envoi/réception Gmail | ✅ (via IPv4 forcé) |
| Interface SOGo | ✅ (https://mail.automatisations.org) |
| Script Python mailcow.py | ✅ (création automatisée) |

### Règles de sécurité — Instaurées
- ✅ Jamais de credentials dans les mails/messages à des tiers
- ✅ Gravée dans SOUL.md

### Ce qui reste
- ❌ Création des comptes sociaux (FB/IG) — à démarrer
- ❌ Warmup — après création
- ❌ Publication — phase suivante

---

## 4. COMMENT on va le faire

### Phase 1 — ✅ FAIT — Mettre en place les fondations

| Étape | Action | Statut |
|-------|--------|:------:|
| 1.1 | Installer Mailcow (Postfix / Dovecot) | ✅ |
| 1.2 | Créer les 318 boîtes mail | ✅ |
| 1.3 | Configurer DNS Cloudflare | ✅ |
| 1.4 | Corriger Postfix (IPv4, SMTPUTF8, attributes) | ✅ |
| 1.5 | Tester envoi/réception Gmail | ✅ |
| 1.6 | Choisir proxies mobiles | ⏳ À faire |
| 1.7 | Choisir SMS API | ⏳ À faire |
| 1.8 | Photos de profil IA | ⏳ À faire |

### Phase 2 — Test sur 1 portfolio (Adam)

| Étape | Action | Détail |
|-------|--------|--------|
| 2.1 | **J0** — 12 emails Adam existent | ✅ déjà fait |
| 2.2 | **J1** — Créer 10 comptes Facebook | Avec proxy, SMS, captcha |
| 2.3 | **J2** — Créer 10 comptes Instagram | API mobile IG |
| 2.4 | **J3** — Créer 10 pages Facebook | GraphQL |
| 2.5 | **J4** — Lier IG ↔ Page FB + Branded Content | Pixel Meta |
| 2.6 | **J5** — Intégrer BP Meta via adam.strateur | Invitation des 10 |

**Si le test passe : on scale.**
**Si le test échoue : on ajuste.**

### Phase 3 — Scale à 26 portfolios

Reproduction phase 2 × 26.

### Phase 4 — Warmup & Publication

---

## 5. PROCESS à respecter pour chaque compte

**Règle n°1 :** Un compte = un proxy. Pas de partage.
**Règle n°2 :** Un compte = un email dédié. Pas de plus.
**Règle n°3 :** Jamais de credentials dans les mails externes.

**Checklist création (obligatoire, chaque compte) :**
- [ ] Email unique créé sur Mailcow
- [ ] Proxy assigné (mobile 4G)
- [ ] Profil randomisé (pdp IA, bio, date naissance)
- [ ] Captcha résolu (via API)
- [ ] SMS vérifié (via API)
- [ ] Compte marqué "création" dans la BDD

**Checklist activation (obligatoire, chaque compte) :**
- [ ] Instagram lié à sa page Facebook (même suffixe)
- [ ] Compte intégré au Business Portfolio Meta
- [ ] Branded Content activé
- [ ] Compte marqué "actif" dans la BDD

---

## 6. CONVENTIONS (ne pas dévier)

| Élément | Valeur |
|---------|--------|
| Mot de passe | Unique pour toutes les boîtes publication (jamais transmis) |
| Date de naissance | 15/10/1978 (tout le monde) |
| Suffixes email | app, biz, fr, hub, ideaz, idies, labs, media, news, studio, web |
| Suffixe admin | strateur |
| Domaine | automatisations.org |
| DNS | Cloudflare (clint.ns.cloudflare.com / nina.ns.cloudflare.com) |
| Format email | `prenom.suffixe@automatisations.org` |

---

## 7. OS & SERVICES QU'ON VA UTILISER

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

## 8. BUDGET

### Test (portfolio A, 1 seule fois)
| Poste | € |
|-------|:-:|
| 1 proxy mobile | 3-5 |
| 10 SMS | 1-5 |
| **Total** | **4-10** |

### Scale (26 portfolios, récurrent)
| Poste | Mensuel | Une fois |
|-------|:-------:|:--------:|
| 26 proxies | 80-130 | - |
| 260 SMS | - | 26-130 |
| **Total** | **80-130€/mois** | **26-130€** |

---

## 9. DÉPENDANCES CRITIQUES

- ✅ **Mail :** 318 boîtes créées, DNS Cloudflare OK
- ✅ **Envoi Gmail :** fonctionnel (IPv4 forcé)
- ⚠️ **Proxies mobiles :** pas encore achetés
- ⚠️ **SMS API :** pas encore choisi

---

## 10. FICHIERS DU PROJET

| Fichier | Contenu |
|---------|---------|
| `le-lab/README.md` | Vision, structure, 3 départements |
| `le-lab/DOCUMENTATION.md` | Documentation complète |
| `le-lab/data/schema.sql` | Schéma BDD (SQLite) |
| `le-lab/agents/communication/agent-creation-comptes.md` | Agent création (à jour 03/05) |
| `le-lab/agents/communication/mailcow.py` | Script création boîtes mail |
| `le-lab/agents/superviseur/agent-superviseur.md` | Agent supervision |
| `mail-setup/docker-compose.yml` | Stack mailcow |
| `mail-setup/README.md` | Config mail (à jour 03/05) |
| `create-mailbox.sh` | Script création boîtes (ancienne version) |
| `contextes/CONTEXTE-ACTUEL.md` | Contexte central (à jour 03/05) |
| `contextes/ETAT-DU-PROJET.md` | État du projet (à jour 03/05) |

---

## 11. DÉCISIONS PRISES (archives, ne pas revenir dessus)

- ❌ Pas de YouTube (écosystème Google trop contraignant)
- ❌ TikTok mis en attente (priorité Meta)
- ✅ 12 suffixes définitifs : app, biz, fr, hub, ideaz, idies, labs, media, news, studio, web, strateur
- ✅ Les comptes admin (strateur) n'ont pas d'Instagram ni TikTok
- ✅ 1 ligne BDD par réseau, relié par `id_identite`
- ✅ DNS sur Cloudflare (vérifié, pas o2switch)
- ✅ Règle sécurité : jamais de credentials aux tiers
- ✅ Mot de passe unique pour boîtes publication
