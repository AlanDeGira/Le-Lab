# PROJET 1 — Le Lab : Publication massive e-commerce

> Document de référence — Dernière mise à jour : 03/05/2026 — 16 sections

---

## TABLE DES MATIÈRES

1. [Pourquoi ce projet existe](#1-pourquoi-ce-projet-existe)
2. [Ce qu'on veut construire](#2-ce-quon-veut-construire)
3. [Architecture des portfolios](#3-architecture-des-portfolios)
4. [Conventions de nommage](#4-conventions-de-nommage)
5. [Règles métier & décisions](#5-regles-metier--decisions)
6. [Base de données](#6-base-de-donnees)
7. [Agents](#7-agents)
8. [Planning de création](#8-planning-de-creation)
9. [Stack technique & outils](#9-stack-technique--outils)
10. [Services tiers payants](#10-services-tiers-payants)
11. [Dépendances & blocages](#11-dependances--blocages)
12. [Checklists obligatoires](#12-checklists-obligatoires)
13. [Budget détaillé](#13-budget-detaille)
14. [Fichiers du projet](#14-fichiers-du-projet)
15. [Structure organisationnelle](#15-structure-organisationnelle)
16. [État d'avancement](#16-etat-davancement)

---

# 1. POURQUOI CE PROJET EXISTE

## 1.1 Le problème

Pour vendre des produits en e-commerce, il faut du trafic. Le trafic payant (Facebook Ads, Google Ads) coûte cher et devient de moins en moins rentable. Le trafic organique (publications sur les réseaux sociaux) est gratuit, mais limité par la portée d'un seul compte.

Un compte Facebook/Instagram standard touche naturellement environ 5 à 10% de ses abonnés sur une publication organique. Avec 300 comptes qui postent le même contenu, la portée est démultipliée sans dépenser un euro en publicité.

## 1.2 La stratégie

Le principe est simple : créer un grand nombre de comptes sociaux qui agissent comme un réseau de distribution. Chaque compte publie du contenu e-commerce (reels, stories, posts) qui redirige vers des landing pages. Les landing pages vendent les produits. Le tout est automatisé.

Ce n'est pas du spam. C'est un réseau de distribution organique. Chaque compte a sa propre identité, son propre contenu, son propre rythme de publication. L'ensemble forme un écosystème crédible.

## 1.3 L'objectif final

**À terme, le système doit :**
- Publier automatiquement sur 300+ comptes (FB, IG, TK)
- Générer du trafic vers des landing pages e-commerce
- Optimiser les publications en fonction des performances
- Se maintenir tout seul (remplacement des comptes bloqués)
- Coûter moins cher qu'une campagne publicitaire équivalente

## 1.4 Les 3 phases du projet

| Phase | Nom | Objectif | Statut |
|:-----:|-----|----------|:------:|
| 1 | Infrastructure de publication | Créer les comptes, les warmuper, les faire publier | En cours |
| 2 | Boutique & Marketing | Landing pages, A/B testing, pixels, tracking | Future |
| 3 | Optimisation continue | Cost-killing, scaling, fiscal, maintenance | Future |

---

# 2. CE QU'ON VEUT CONSTRUIRE

## 2.1 Les comptes

On va créer **806 comptes sociaux** répartis sur **26 portfolios** (un par lettre de l'alphabet, de A à Z). Chaque portfolio représente une identité fictive complète.

**Par portfolio :**

| Type de compte | Qté | Réseau | Rôle |
|----------------|:---:|--------|------|
| Comptes publication | 10 | Facebook (compte personnel) | Publier du contenu |
| Pages Facebook | 10 | Facebook (page) | Recevoir les publications |
| Comptes Instagram | 10 | Instagram | Publier des reels |
| Comptes TikTok | 10 | TikTok | Publier des vidéos (optionnel) |
| Compte admin (strateur) | 1 | Facebook (BP Meta) | Gérer, intégrer, superviser |
| **Total par portfolio** | **31** | | |

**Pour les 26 portfolios :**

| Type | Total |
|------|:-----:|
| Comptes Facebook (personnels) | 260 |
| Pages Facebook | 260 |
| Comptes Instagram | 260 |
| Comptes TikTok (optionnel) | 260 |
| Admins / Strateurs | 26 |
| **Total général** | **~806** |

## 2.2 Ce qu'on ne fait PAS (décisions fermes)

| Décision | Raison |
|----------|--------|
| **YouTube** - EXCLU | Ecosystème Google trop contraignant (verif SMS + tel + ID) |
| **TikTok** - EN ATTENTE | Priorité Meta. On y reviendra si FB/IG tourne bien |
| **Rotation de proxies** - INTERDIT | 1 proxy = 1 compte. Pas de partage, pas de rotation |
| **Contestation comptes bloqués** - INTERDIT | Abandon. Pas de réclamation, pas de risque |
| **Admin avec Instagram/TikTok** - INTERDIT | Le strateur est purement Facebook / Business Portfolio |

---

# 3. ARCHITECTURE DES PORTFOLIOS

## 3.1 La liste complète

| # | Lettre | Prénom | Comptes pub. | Admin (strateur) | Total |
|:-:|:------:|--------|:------------:|:----------------:|:-----:|
| 1 | A | Adam | 10 | adam.strateur | 31 |
| 2 | B | Baptiste | 10 | baptiste.strateur | 31 |
| 3 | C | Camille | 10 | camille.strateur | 31 |
| 4 | D | Diane | 10 | diane.strateur | 31 |
| 5 | E | Emile | 10 | emile.strateur | 31 |
| 6 | F | Flora | 10 | flora.strateur | 31 |
| 7 | G | Gabriel | 10 | gabriel.strateur | 31 |
| 8 | H | Hugo | 10 | hugo.strateur | 31 |
| 9 | I | Iris | 10 | iris.strateur | 31 |
| 10 | J | Jules | 10 | jules.strateur | 31 |
| 11 | K | Karine | 10 | karine.strateur | 31 |
| 12 | L | Leo | 10 | leo.strateur | 31 |
| 13 | M | Manon | 10 | manon.strateur | 31 |
| 14 | N | Nathan | 10 | nathan.strateur | 31 |
| 15 | O | Oscar | 10 | oscar.strateur | 31 |
| 16 | P | Paul | 10 | paul.strateur | 31 |
| 17 | Q | Quentin | 10 | quentin.strateur | 31 |
| 18 | R | Romane | 10 | romane.strateur | 31 |
| 19 | S | Sacha | 10 | sacha.strateur | 31 |
| 20 | T | Theo | 10 | theo.strateur | 31 |
| 21 | U | Ulysse | 10 | ulysse.strateur | 31 |
| 22 | V | Valentin | 10 | valentin.strateur | 31 |
| 23 | W | William | 10 | william.strateur | 31 |
| 24 | X | Xander | 10 | xander.strateur | 31 |
| 25 | Y | Yasmine | 10 | yasmine.strateur | 31 |
| 26 | Z | Zoe | 10 | zoe.strateur | 31 |

## 3.2 Comment les comptes sont groupés

Chaque compte est lié à :
- Son **portfolio** (table portfolios) - l'identité parente
- Son **réseau** (facebook_page, instagram, tiktok) - la plateforme
- Son **suffixe** (reel, story, content...) - le rôle spécifique

Un portfolio "Adam" = 31 lignes en BDD :
- 10 x Facebook (adam.reel, adam.story... adam.life)
- 10 x Instagram (idem)
- 10 x TikTok (idem, en option)
- 1 x admin Facebook (adam.strateur)

## 3.3 Le rôle du strateur (admin)

Le strateur est le compte central du portfolio. Il :
- Crée et gère le **Business Portfolio Meta**
- Invite les 10 comptes publication dans le BP Meta
- Active le Branded Content sur chaque compte Instagram
- Supervise l'état de santé du portfolio
- **Ne publie pas de contenu**
- **N'a pas d'Instagram ni TikTok**

---

# 4. CONVENTIONS DE NOMMAGE

## 4.1 Emails des comptes publication

Format : `prenom.suffixe@automatisations.org`

| Suffixe | Rôle | Type de contenu |
|---------|------|-----------------|
| .reel | Compte principal | Reels, videos courtes |
| .story | Compte stories | Stories quotidiennes |
| .content | Compte contenu long | Posts, articles, descriptions |
| .media | Compte medias | Photos, visuels, produits |
| .feed | Compte feed | Posts standards, grille |
| .post | Compte posts programmés | Publications planifiées |
| .daily | Compte quotidien | Contenu journalier |
| .vibe | Compte lifestyle | Ambiance, style de vie |
| .style | Compte mode/style | Mode, tendances |
| .life | Compte lifestyle general | Vie quotidienne, blog |

## 4.2 Mots de passe

| Rôle | Format | Exemple |
|------|--------|---------|
| Publication | `Prenom1!` | `Adam1!` |
| Admin / Strateur | `Prenom.admin1!` | `Adam.admin1!` |

## 4.3 Date de naissance

**1990-01-01** pour tous, sans exception.

---

# 5. REGLES METIER & DECISIONS

## 5.1 Règles absolues (ne pas enfreindre)

| Règle | Raison | Sanction |
|-------|--------|----------|
| 1 proxy = 1 compte | Meta détecte les IP partagées | Ban immédiat |
| Pas de création depuis datacenter | IP blacklistées | Ban avant création |
| 24h minimum avant action apres création | Meta analyse comportement initial | Shadowban |
| Ne pas publier le jour de la création | Comportement non-humain | Ban |
| Compte bloqué = abandon | Contester = risquer tout le portfolio | Perte totale |
| Jamais le même MDP que le strateur | Séparation des responsabilités | Compromission totale |

## 5.2 Règles de warmup

| Période | Actions autorisées | Durée/jour |
|---------|-------------------|:----------:|
| J1-J5 | Connexion uniquement, lecture du fil | ~1 min |
| J6-J15 | Connexion + likes + follows aléatoires | ~5 min |
| J16-J30 | Connexion + likes + follows + scroll + commentaires | ~10-15 min |
| J31+ | Premier post organique | Normal |

## 5.3 Règles de supervision

| Seuil | Action |
|-------|--------|
| 1 compte bloqué dans 1 portfolio | Alerte Kevyn + marquer "bloque" |
| 3 comptes bloqués dans 1 portfolio | Portfolio suspendu automatiquement |
| 3 shadowban dans 1 portfolio | Alerte Kevyn + investigation |
| 3 échecs consécutifs publication | Alerte immédiate |

## 5.4 Décisions historiques (archives)

| Décision | Date | Raison |
|----------|:----:|--------|
| Abandon YouTube | 02/05/2026 | Vérification trop stricte |
| TikTok en attente | 02/05/2026 | Priorité Meta |
| Pas d'IG/TK pour les strateurs | 02/05/2026 | Rôle purement admin FB |
| 1 ligne BDD par réseau | 02/05/2026 | Traçabilité par plateforme |
| Date naissance unique 1990-01-01 | 02/05/2026 | Simplicité, pas de détection cross-compte |
| Pas de rotation proxies | 02/05/2026 | Risque de ban |
| Abandon contestation comptes bloqués | 02/05/2026 | Rapport risque/bénéfice défavorable |

---

# 6. BASE DE DONNEES

## 6.1 Informations générales

| Propriété | Valeur |
|-----------|--------|
| Type | SQLite |
| Fichier | le-lab/data/le-lab.db |
| Schéma | le-lab/data/schema.sql |
| Version | v2 |

## 6.2 Table portfolios

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PK | Auto |
| nom | TEXT | "Portfolio A" |
| numero | INTEGER UNIQUE | 1 à 26 |
| lettre | TEXT | A à Z |
| prenom | TEXT | Adam à Zoé |
| business_manager_id | TEXT | ID BP Meta (rempli après création) |
| proxy | TEXT | Adresse du proxy assigné |
| statut | TEXT | en_creation, actif, suspendu |
| date_creation | DATETIME | Auto |

## 6.3 Table comptes

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PK | Auto |
| portfolio_id | INTEGER FK | Portfolio parent |
| email | TEXT | Email complet |
| suffixe | TEXT | reel, story, content... |
| mot_de_passe | TEXT | Mot de passe |
| nom_page | TEXT | Nom de la page Facebook |
| reseau | TEXT | facebook_page, instagram, tiktok |
| pseudo_instagram | TEXT | Pseudo Instagram |
| statut | TEXT | en_attente, creation, actif, bloque, shadowban, a_verifier |
| role | TEXT | publication, admin |
| date_de_naissance | TEXT | 1990-01-01 |
| derniere_verification | DATETIME | Derniere vérification |
| date_creation | DATETIME | Auto |

Contraintes :
- UNIQUE(email, reseau) - 1 email peut avoir FB+IG+TK, pas 2 FB
- reseau IN ('facebook_page', 'instagram', 'tiktok')
- statut IN ('en_attente', 'creation', 'actif', 'bloque', 'shadowban', 'a_verifier')
- role IN ('publication', 'admin')

## 6.4 Table videos

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PK | Auto |
| fichier | TEXT | Nom du fichier |
| chemin | TEXT | Chemin complet |
| duree_secondes | INTEGER | Durée vidéo |
| theme | TEXT | Thème |
| description | TEXT | Description |
| portfolio_id | INTEGER FK | Portfolio assigné |
| nombre_publications | INTEGER | Compteur |
| date_ajout | DATETIME | Auto |

## 6.5 Table publications

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PK | Auto |
| compte_id | INTEGER FK | Compte qui publie |
| video_id | INTEGER FK | Vidéo publiée |
| date_prevue | DATETIME | Date planifiée |
| date_reelle | DATETIME | Date réelle |
| statut | TEXT | planifie, succes, echec, annule |
| message_erreur | TEXT | Si échec |

## 6.6 Table logs

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PK | Auto |
| niveau | TEXT | info, warning, error, critical |
| source | TEXT | Composant |
| message | TEXT | Message |
| details | TEXT | Détails (JSON) |
| date | DATETIME | Auto |

## 6.7 Index

| Index | Colonne | Utilité |
|-------|---------|---------|
| idx_comptes_portfolio | portfolio_id | Recherche par portfolio |
| idx_comptes_statut | statut | Filtrage actifs/bloqués |
| idx_comptes_reseau | reseau | Filtrage par plateforme |
| idx_comptes_role | role | Publication vs admin |
| idx_publications_date | date_prevue | Planning |
| idx_publications_compte | compte_id | Historique par compte |
| idx_logs_date | date | Recherche chronologique |
| idx_logs_niveau | niveau | Filtrage erreurs critiques |

## 6.8 Vues

**vue_etat_global :** total_comptes, comptes_actifs, bloques, shadowban, a_verifier, portfolios_actifs, pubs_reussies, pubs_echouees.

**vue_portfolio_detail :** par portfolio : numero, lettre, prenom, statut, total_comptes, admins, actifs, bloques, facebook, instagram, tiktok.

---

# 7. AGENTS

## 7.1 Agent 1 - Création de Comptes

**Fichier :** le-lab/agents/communication/agent-creation-comptes.py
**Doc :** le-lab/agents/communication/agent-creation-comptes.md
**Langage :** Python 3

**Rôle :** Générer les 26 portfolios et leurs 806 comptes dans la base de données. L'agent ne crée PAS les comptes sur Facebook/Instagram. Il remplit la structure BDD avec les métadonnées.

**Commandes :**
- dashboard - Résumé : nb portfolios, nb comptes, répartition par statut
- generer - Crée les 26 portfolios + 806 comptes (vérifie doublons)
- portfolio <num> - Crée un seul portfolio (ex: portfolio 1 = Adam)

**Logique d'insertion :**
1. Vérifier si le portfolio existe déjà
2. Si non : créer le portfolio (statut "en_creation")
3. Pour chaque suffixe (reel... life) : créer 3 lignes (FB+IG+TK, statut "en_attente")
4. Créer le compte admin (role "admin", reseau "facebook_page")
5. Mettre à jour le compteur du portfolio

## 7.2 Agent 2 - Superviseur

**Fichier :** le-lab/agents/superviseur/agent-superviseur.py
**Doc :** le-lab/agents/superviseur/agent-superviseur.md
**Cron :** le-lab/agents/superviseur/cron-superviseur.yaml
**Langage :** Python 3
**Fréquence :** Toutes les heures

**Rôle :** Centraliser et filtrer les anomalies de tous les agents. Décisions automatiques. Alertes.

**Etapes :**
1. Analyse - lecture des logs de la dernière heure
2. Détection - comptes bloqués, shadowban, échecs publication
3. Décision - suspension de portfolio, alerte
4. Transmission - écriture de alerte_sortie.json

**Règles :**
| Niveau | Critère | Action |
|--------|---------|--------|
| Critique | Compte bloqué, proxy mort, échec pub | Alerte immédiate Kevyn |
| Important | Shadowban, ralentissement | Résumé quotidien |
| Info | Compte créé, pub réussie | Log BDD uniquement |

**Décisions automatiques :**
| Condition | Action |
|-----------|--------|
| 3+ bloqués dans 1 portfolio | Portfolio suspendu |
| 3+ shadowban dans 1 portfolio | Alerte Kevyn |
| >3 échecs consécutifs pub | Alerte immédiate |

**Anti-doublon :** Une alerte identique max 1x par heure.

**Communication :** Ecrit alerte_sortie.json. Un listener cron lit le fichier, envoie sur Telegram, supprime.

---

# 8. PLANNING DE CREATION

## 8.1 Stratégie

Test sur **1 seul portfolio** (Adam) d'abord. Si ça marche, on scale. Si ça plante, on ajuste sans perte.

## 8.2 Phase test - Portfolio A (Adam) : J0 à J31

### J0 - Préparation

| Tâche | Détail |
|-------|--------|
| Créer 10 boîtes mail Adam | Mailcow : adam.reel à adam.life |
| Préparer 1 proxy mobile | Choisir et acheter un fournisseur |
| Préparer 10 numéros SMS | Via 5sim ou équivalent |
| Générer 10 photos de profil IA | ThisPersonDoesNotExist ou Stable Diffusion |
| Générer 10 bios randomisées | Descriptions crédibles |

### J1 - Création des 10 comptes Facebook

| Tâche | Outil |
|-------|-------|
| Créer 10 comptes FB | Selenium maison + undetected-chromedriver |
| Résoudre reCAPTCHA | 2Captcha API |
| Vérifier SMS | 5sim API |
| Marquer "creation" en BDD | Agent création |
| Attendre 24h avant toute action | |

### J2 - Création des 10 comptes Instagram

| Tâche | Outil |
|-------|-------|
| Créer 10 comptes IG | SaeidB/insta_create |
| Marquer "creation" en BDD | Agent création |

### J3 - Création des 10 pages Facebook

| Tâche | Outil |
|-------|-------|
| Créer 10 pages FB | greikgk/FB-Pages-Creator |
| Lier page au compte FB | Meta interface |

### J4 - Liaisons

| Tâche | Où |
|-------|-----|
| Lier chaque IG à sa page FB (même suffixe) | Meta Business Suite |
| Activer Branded Content sur chaque IG | Paramètres Instagram |
| Vérifier les liaisons | Test publication |

### J5 - Intégration Business Portfolio Meta

| Tâche | Acteur |
|-------|--------|
| Strateur crée le BP Meta | Meta Business Suite |
| Strateur invite les 10 pages FB | BP Meta > Ajouter comptes |
| Les 10 comptes acceptent l'invitation | Chaque compte FB |
| Vérifier l'intégration | BP Meta > Comptes |
| Marquer "actif" en BDD | Agent |

### J6 à J30 - Warmup

| Période | Actions | Durée/jour |
|---------|---------|:----------:|
| J6-J10 | Connexion uniquement | ~1 min |
| J11-J15 | Likes + follows aléatoires | ~5 min |
| J16-J20 | Likes + follows + scroll | ~10 min |
| J21-J30 | Likes + follows + scroll + commentaires | ~15 min |

### J31+ - Publication

| Etape | Action |
|-------|--------|
| Premier post organique | Tester réaction |
| Pas de flag > planning automatisé | Activation |
| Flag > retour warmup, ajuster | Correction |

## 8.3 Scale - 26 portfolios

| Stratégie | Durée | Risque | Avantage |
|-----------|:-----:|:------:|----------|
| Linéaire (recommandée) | ~5 mois | Faible | Ajustable à chaque itération |
| Parallélisée | ~1 mois | Elevé | Rapidité |

---

# 9. STACK TECHNIQUE & OUTILS

## 9.1 Instagram - SaeidB/insta_create

**Pourquoi :** API mobile IG (370.0.0.42.96), proxies, usernames auto, cookie format choice, testé 2025.

**Installation :**
```
git clone https://github.com/SaeidB/insta_create.git
cd insta_create
pip install -r requirements.txt
```

**Exécution :**
```
python insta_create.py --email adam.reel@automatisations.org --password Adam1! --proxy http://user:pass@ip:port --birthday 1990-01-01
```

**Résultat :** Compte IG créé + cookie stocké + marqué "creation" en BDD.

## 9.2 Pages Facebook - greikgk/FB-Pages-Creator

**Pourquoi :** GraphQL + Bloks API, GUI, MIT, MAJ 03/05/2026.

**Installation :**
```
git clone https://github.com/greikgk/FB-Pages-Creator.git
cd FB-Pages-Creator
pip install -r requirements.txt
```

**Exécution :** python main.py > interface GUI > token, nom, catégorie.

**Résultat :** Page FB créée + marquée BDD + liée à IG (même suffixe).

## 9.3 Comptes Facebook - DIY Selenium

**Pourquoi du sur-mesure :** Aucun projet OS fiable pour les comptes FB. Les bots existants sont morts, scams, ou freemium. Facebook change son flow d'inscription toutes les 2 semaines.

**Stack technique :**
| Technologie | Rôle |
|-------------|------|
| Python | Langage |
| undetected-chromedriver | Anti-détection |
| Proxy mobile 4G | IP résidentielle |
| 2Captcha API | reCAPTCHA |
| 5sim API | SMS |
| Randomisation | Fingerprints (WebGL, canvas, fonts, resolution) |

**Flow à automatiser :**
1. Ouvrir facebook.com via undetected-chromedriver + proxy
2. Remplir formulaire : prénom, nom, email, MDP, date naissance, genre
3. Résoudre reCAPTCHA via 2Captcha
4. Soumettre
5. Attendre code SMS via 5sim
6. Saisir le code
7. Ajouter photo de profil (IA)
8. Ajouter bio randomisée
9. Ne rien faire pendant 24h
10. Marquer "creation" en BDD

**IMPORTANT : Ce code n'est pas encore écrit. C'est le prochain bloc à développer.**

## 9.4 TikTok - En attente

- hendrikbgr/TikTok-Account-Creator : seul outil OS trouvé, vérif manuelle
- l-portet/tiktok-warmup-bot : warmup iOS Voice Control
- Priorité Meta d'abord

## 9.5 Projets OS explorés (non retenus)

Voir PROJET-COMPTES-MASSE.md pour l'analyse des 12 repos GitHub (angel-automation, mohamed-ladjal-AI, danir-pye, zile42O, makiisthenes, CruelDev69, etc.)

---

# 10. SERVICES TIERS PAYANTS

## 10.1 Proxies

**Pourquoi mobiles :** Meta bloque immédiatement les IP datacenter. Seules les IP mobiles 4G/5G passent.

| Fournisseur | Prix/mois | Type | Fiabilité |
|-------------|:---------:|------|:---------:|
| BrightData | ~5€ | Mobile 4G | Excellente |
| IPRoyal | ~3€ | Residentiel | Bonne |
| Proxysale | ~3-5€ | Mobile | Bonne |
| Hydrox | ~3€ | Residentiel | Correcte |

**Règle :** 1 proxy = 1 compte. Pas de partage. Pas de rotation.

## 10.2 SMS (vérification téléphone)

| Fournisseur | Prix/numéro | Notes |
|-------------|:-----------:|-------|
| 5sim | ~0.10-0.50€ | Large choix pays, API fiable |
| SMSActivate | ~0.15-0.50€ | Fiable, API solide |
| SMSPVA | ~0.10-0.30€ | Bon marché |

**Règle :** 1 numéro = 1 compte. Pas de réutilisation.

## 10.3 Captcha

| Fournisseur | Prix | Notes |
|-------------|:----:|-------|
| 2Captcha | ~0.50€/1000 | Standard, fiable |
| AntiCaptcha | ~1-2€/1000 | Plus rapide |

---

# 11. DEPENDANCES & BLOCAGES

## 11.1 Critique - Serveur mail OTP

**Problème :** Chaque compte a besoin d'un email unique. Sans serveur mail, impossible de créer les comptes.

**Solution :** Mailcow est déjà installé en Docker sur le VPS.
- Container : mailcowdockerized-mysql-mailcow-1
- Boîtes existantes : burgerparis0-9, otp, compte10/11/20/21
- MDP commun existant : Automatisation1!
- Script de création prêt : create-mailbox.sh

**Ce qui bloque :** Les DNS du domaine automatisations.org pointent vers o2switch. Il faut les basculer vers Cloudflare pour que le serveur mail soit joignable.

**Sans cette migration DNS :**
- On ne peut pas créer les 260 boîtes mail
- On ne peut pas créer les comptes sociaux
- **Le projet est à l'arrêt**

## 11.2 En attente de décision Kevyn

- [ ] Choix fournisseur proxies
- [ ] Choix fournisseur SMS
- [ ] Choix fournisseur captcha
- [ ] Budget mensuel alloué pour les services payants
- [ ] Feu vert pour lancer le test sur Adam

---

# 12. CHECKLISTS OBLIGATOIRES

## 12.1 Checklist création (chaque compte)

- [ ] Email unique créé sur Mailcow
- [ ] Proxy mobile assigné
- [ ] Profil randomisé (photo IA + bio + date naissance)
- [ ] Captcha résolu via API
- [ ] SMS vérifié via API
- [ ] Compte marqué "creation" en BDD

## 12.2 Checklist activation (chaque compte)

- [ ] Instagram lié à sa page Facebook (même suffixe)
- [ ] Compte intégré au Business Portfolio Meta (via strateur)
- [ ] Branded Content activé (pour tracking pixel Meta)
- [ ] Compte marqué "actif" en BDD

---

# 13. BUDGET DETAILLE

## 13.1 Test - Portfolio A (Adam)

| Poste | Qté | Prix unitaire | Total |
|-------|:---:|:-------------:|:-----:|
| Proxy mobile 1 mois | 1 | ~3-5€ | ~3-5€ |
| SMS vérification | 10 | ~0.10-0.50€ | ~1-5€ |
| Captcha | ~200 résolutions | ~0.50€/1000 | ~0.10€ |
| Photos de profil IA | 10 | Gratuit | 0€ |
| **Total test** | | | **~4-10€** |

## 13.2 Scale - 26 portfolios

| Poste | Qté | Mensuel | Une fois |
|-------|:---:|:-------:|:--------:|
| Proxies mobiles | 26 | ~80-130€ | - |
| SMS vérification | 260 | - | ~26-130€ |
| Captcha | ~5200 résolutions | - | ~3-10€ |
| Photos de profil IA | 260 | - | 0€ |
| **Total** | | **80-130€/mois** | **29-140€** |

## 13.3 Economies vs pub classique

A titre de comparaison, une campagne Facebook Ads à 10€/jour = 300€/mois. Le scale complet du projet coûte ~80-130€/mois, soit 2 à 3 fois moins cher qu'une seule campagne pub, et le trafic généré est durable (pas d'arrêt si on coupe le budget pub).

---

# 14. FICHIERS DU PROJET

| Fichier | Contenu |
|---------|---------|
| le-lab/README.md | Vision, structure, 3 départements |
| le-lab/DOCUMENTATION.md | Documentation complète du projet |
| le-lab/data/schema.sql | Schéma BDD (SQLite) |
| le-lab/data/le-lab.db | Base de données SQLite |
| le-lab/agents/communication/agent-creation-comptes.py | Code agent création de comptes |
| le-lab/agents/communication/agent-creation-comptes.md | Documentation agent création |
| le-lab/agents/superviseur/agent-superviseur.py | Code agent superviseur |
| le-lab/agents/superviseur/agent-superviseur.md | Documentation agent superviseur |
| le-lab/agents/superviseur/cron-superviseur.yaml | Cron toutes les heures |
| mail-setup/README.md | Configuration mail OTP |
| mail-setup/docker-compose.yml | Stack Postfix + Dovecot |
| mail-setup/mail.txt | DNS DKIM public |
| check-otp.sh | Script récupération OTP |
| create-mailbox.sh | Script création boîtes Mailcow |
| PROJET-COMPTES-MASSE.md | Recherche outils open source |
| CREATION-COMPTES.md | Procédure détaillée création |
| projects/PROJET1-LELAB.md | **CE FICHIER** |

---

# 15. STRUCTURE ORGANISATIONNELLE

```
Kevyn (Chef)
  └── Alan de Gira (Pilotage)
        ├── Département Communication (Publication massive)
        │     └── Agents : création comptes, publication, warmup
        ├── Département Vente (Landing pages, boutique)
        │     └── A construire (phase 2)
        └── Département Continu/Interne (Optimisation, coûts, infra)
              └── Agents : superviseur, monitoring
```

### Les 3 phases
| Phase | Nom | Statut |
|:-----:|-----|:------:|
| 1 | Infrastructure de publication | EN COURS |
| 2 | Boutique & Marketing | Future |
| 3 | Optimisation continue | Future |

---

# 16. ETAT D'AVANCEMENT

| Element | Statut | Depuis |
|---------|:------:|:------:|
| Vision & objectif définis | FAIT | 01/05 |
| Architecture 26 portfolios | FAIT | 01/05 |
| Conventions (MDP, emails) | FAIT | 01/05 |
| Schéma BDD v2 | FAIT | 01/05 |
| Agent création comptes | FAIT | 01/05 |
| Agent superviseur | FAIT | 01/05 |
| Documentation complète | FAIT | 01/05 |
| Recherche outils open source | FAIT | 03/05 |
| Procédure création détaillée | FAIT | 03/05 |
| Selenium FB (code à écrire) | A FAIRE | - |
| Phase test Portfolio A | EN ATTENTE | - |
| Serveur mail OTP (Mailcow) | BLOQUE DNS | - |
| Choix fournisseur proxies | A FAIRE | - |
| Choix fournisseur SMS | A FAIRE | - |
| Choix fournisseur captcha | A FAIRE | - |
| Création comptes FB | A FAIRE | - |
| Création comptes IG | A FAIRE | - |
| Création pages FB | A FAIRE | - |
| TikTok | EN ATTENTE | - |
