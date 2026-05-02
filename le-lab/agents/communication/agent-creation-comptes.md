# Agent Création de Comptes v2

## Rôle
Générer les 26 portfolios (A → Z) avec leurs comptes Facebook, Instagram et TikTok.

## Architecture
- **26 portfolios**, 1 par lettre de l'alphabet
- **1 prénom** par portfolio (ex: Portfolio A = Adam)
- **10 comptes publication** + **1 compte admin** par portfolio
- Chaque publication a : 1 page Facebook + 1 Instagram + 1 TikTok
- Chaque email = 3 lignes dans la BDD (1 par réseau)

## Portfolios
| # | Lettre | Prénom | Admin |
|---|--------|--------|-------|
| 1 | A | Adam | adam.strateur |
| 2 | B | Baptiste | baptiste.strateur |
| ... | ... | ... | ... |
| 26 | Z | Zoé | zoe.strateur |

## Suffixes email (10)
- `.reel`, `.story`, `.content`, `.media`, `.feed`
- `.post`, `.daily`, `.vibe`, `.style`, `.life`

Format : `prenom.suffixe@automatisations.org`

## Mots de passe
- Comptes publication : `Prénom1!` (ex: `Adam1!`)
- Compte admin : `Prénom.admin1!` (ex: `Adam.admin1!`)
- Date de naissance : `1990-01-01` pour tous

## Par portfolio
- 30 comptes publication (10 FB + 10 IG + 10 TK)
- 1 compte admin FB (strateur)
- **31 comptes au total par portfolio**
- **806 comptes pour les 26 portfolios** (admin compris)

## Conditions obligatoires de création (transmises par l'Agent Publication)

Chaque compte créé **doit impérativement** respecter ces 3 conditions :

### 1. Compte Instagram lié à sa page Facebook
- Le compte Instagram (Pro) doit être connecté à la page Facebook correspondante (même suffixe)
- Vérifiable dans Meta Business Suite → Instagram → Linked Accounts

### 2. Compte intégré au Business Portfolio Meta
- Tous les comptes FB/IG d'un même portfolio doivent être membres du Business Portfolio
- Géré par le compte strateur (admin) qui invite chaque page FB

### 3. Branded Content activé
- Chaque compte Instagram doit autoriser le contenu de marque (Branded Content / Partnerships)
- Permet de taguer la marque partenaire dans chaque publication
- Requis pour le tracking via pixel Meta

Ces conditions sont **vérifiées** après création. Tout compte ne les respectant pas est marqué `a_verifier`.

## Admin (strateur)
- Ne publie pas
- Gère le Business Portfolio Meta
- Lie les pages Facebook entre elles
- Invite les 10 comptes publication dans le BP Meta
- Active Branded Content pour chaque compte
- Pas d'Instagram, pas de TikTok

## Commandes
- `dashboard` — Vue d'ensemble
- `generer` — Génère les 26 portfolios
- `portfolio <num>` — Génère un seul portfolio

## BDD
- Table `comptes` : 1 ligne par réseau (FB/IG/TK)
- Champ `role` : 'publication' ou 'admin'
- Champ `suffixe` : le suffixe de l'email (pour regroupement)
- Vue `vue_portfolio_detail` : stats par portfolio
- Vue `vue_etat_global` : stats globales
