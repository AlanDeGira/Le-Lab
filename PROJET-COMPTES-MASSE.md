# PROJET — Création massive de comptes sociaux (FB, IG, TK)

## Objectif
Trouver / assembler une solution open source pour créer en masse :
- Comptes Facebook
- Pages Facebook
- Comptes Instagram
- Comptes TikTok

## Contexte Kevyn
- Projet plus large : système e-commerce automatisé, 300 comptes sociaux, landing pages dynamiques
- 3 départements : Communication, Vente, Continu/Interne
- Serveur : Contabo VPS Cloud 10, Ubuntu 22.04, domaine automatisations.org
- Stack : n8n + PostgreSQL + Metabase
- Canal principal : Telegram

## Projets open source identifiés

### Facebook — Création de comptes

| Projet | Langage | Description | MAJ |
|--------|---------|-------------|:---:|
| **angel-automation/FB-Creator-Bot** | Python | Crée comptes FB. Free: Web API, infos aléatoires. Paid: proxies, Mobile API, email confirm. Contact Telegram @ANGLE_DEV | 2024 |
| **mohamed-ladjal-AI/auto_facebook_creator** | Python | Crée comptes FB avec profils randomisés via Tor + Selenium. Licence MIT. | 2024 |
| **danir-pye/FB-Creator-Bot** | Node.js | Framework Danir AI. Générateur content AI, planning auto. Contact @danirueaq | 2025 |
| **yashu1wwww/Facebook-auto-account-create** | Python | Création auto FB avec Selenium | ? |
| **Ra1d7 Facebook Mass Account Maker** | Gist | Gist GitHub FB mass creator | ? |

### Facebook — Pages

| Projet | Langage | Description | MAJ |
|--------|---------|-------------|:---:|
| **greikgk/FB-Pages-Creator** | Python | Crée pages FB via GraphQL + Bloks API. Interface GUI. Licence MIT. | **03/05/2026** ⚡ |

### Instagram — Création de comptes

| Projet | Langage | Description | MAJ |
|--------|---------|-------------|:---:|
| **SaeidB/insta_create** ⭐ | Python | API mobile IG (370.0.0.42.96). Proxies, génération usernames, choix format cookie. Testé 2025. | **2025** |
| **zile42O/instagram-generator** | Python | Proxy + sms-activate.org API. Threading multi-country. | 2023 |
| **makiisthenes/Insta-mass-account-creator** | Python | 2 modes: Selenium ou Requests. Proxies, pays, domaine email. | ? |
| **angel-automation/Instagram-account-creator** | Python | Requests, Mobile/Web/iOS API, auto-email confirm, proxies. | 2024 |
| **CruelDev69/InstaGen** | JavaScript | Générateur comptes IG non vérifiés. | 2024 |

### TikTok — Création

| Projet | Langage | Description | MAJ |
|--------|---------|-------------|:---:|
| **hendrikbgr/TikTok-Account-Creator** | Python | Crée comptes TK en masse. CSV export. ChromeDriver. Vérif manuelle requise. | ? |

### TikTok — Warmup (indispensable après création)

| Projet | Langage | Description | MAJ |
|--------|---------|-------------|:---:|
| **l-portet/tiktok-warmup-bot** ⭐ | Node.js | Bot iOS Voice Control pour warmup TK. Swipe, like, save auto. Licence Beerware. | ? |

### Outils open source complémentaires

| Outil | Utilité |
|-------|---------|
| **Selenium / Puppeteer / Playwright** | Frameworks browser automation DIY |
| **InstaPy** | Automation Instagram (engagement organique) |
| **TikTokApi** | API TikTok scraping + upload |
| **instagrapi** | API privée Instagram |
| **2Captcha / AntiCaptcha** | Résolution captchas (API payante) |
| **5sim / SMSActivate / SMSPVA** | SMS virtuels vérification (API payante) |

## Stack technique recommandée
- Proxies mobiles 4G/5G (obligatoire, pas de datacenter)
- Anti-detect browsers (optionnel si création API)
- SMS API pour vérification téléphone
- Captcha solving service
- Randomisation complète (fingerprints, timings, user-agents)

## Liens utiles
- PVACreator guide technique : https://github.com/PVACreator/Automating-Bulk-Account-Creation-Tools-and-Methods
- Julian Ivaldy — TikTok/IG Farm : https://julianivaldy.medium.com/building-tiktok-instagram-farm-083e5e3bab62
- SocialAppFarm Mother-Child : https://socialappfarm.com/blog/building-and-automating-your-tiktok-and-instagram-account-with-ai-support-running-on-device-farm/
- Account Farming 2025 : https://blog.browserscan.net/docs/account-farming-2025-browserscan-zinyproxy
