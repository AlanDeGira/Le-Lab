# 🔧 Procédure — Création des comptes

---

## RÉSUMÉ (10 lignes)

1. Chaque compte a besoin : 1 email unique + 1 proxy mobile + 1 SMS + 1 résolution captcha
2. Pour Instagram : on utilise **SaeidB/insta_create** (API mobile IG)
3. Pour les pages Facebook : on utilise **greikgk/FB-Pages-Creator** (GraphQL + Bloks)
4. Pour les comptes Facebook : rien d'OS fiable → on fait du Selenium maison
5. Pour TikTok : rien de prêt → mis en attente
6. Chaque compte est créé → marqué "creation" dans BDD → vérifié → marqué "actif"
7. Le strateur (admin) intègre chaque nouveau compte dans le Business Portfolio Meta
8. Branded Content activé sur chaque compte Instagram
9. Un seul portfolio testé d'abord (Adam × 10 comptes)
10. Si test OK → scale à 26 portfolios

---

## 1. INSTAGRAM — SaeidB/insta_create

### Pourquoi lui
- API mobile Instagram (version 370.0.0.42.96) — ressemble à une vraie app
- Proxies supportés
- Génération de username automatique
- Choix du format de cookie
- Testé et fonctionnel en 2025

### Installation
```bash
git clone https://github.com/SaeidB/insta_create.git
cd insta_create
pip install -r requirements.txt
```

### Configuration
```python
# config.py
PROXY = "http://user:pass@ip:port"  # Proxy mobile obligatoire
INSTA_API = "370.0.0.42.96"
SMS_API_KEY = "..."  # 5sim ou SMSActivate
CAPTCHA_API_KEY = "..."  # 2Captcha
```

### Exécution
```bash
python insta_create.py \
  --email adam.reel@automatisations.org \
  --password Adam1! \
  --proxy http://user:pass@ip:port \
  --birthday 1990-01-01 \
  --username adam_reel
```

### Résultat attendu
- Compte Instagram créé ✅
- Cookie stocké pour session ultérieure
- Compte marqué "creation" dans BDD

### Vérification
- Se connecter avec le cookie
- Vérifier que le compte n'est pas shadowban
- Si OK → marqué "actif"

---

## 2. PAGES FACEBOOK — greikgk/FB-Pages-Creator

### Pourquoi lui
- Utilise l'API GraphQL + Bloks (les vraies API internes Meta)
- Interface GUI
- Licence MIT
- MAJ le 3 mai 2026 (hyper récent → encore fonctionnel)

### Installation
```bash
git clone https://github.com/greikgk/FB-Pages-Creator.git
cd FB-Pages-Creator
pip install -r requirements.txt
```

### Configuration
```python
# Config : token Facebook, proxy, etc.
FB_TOKEN = "..."  # Récupéré depuis le compte Facebook associé
PROXY = "http://user:pass@ip:port"
PAGE_NAME = "Adam Reel"  # Nom de la page
PAGE_CATEGORY = "Shopping & Retail"
```

### Exécution
```bash
python main.py
```
→ Interface graphique : entrer le token, le nom de page, la catégorie
→ Le bot crée la page via GraphQL

### Résultat attendu
- Page Facebook créée ✅
- Marqué dans BDD
- Liée au compte Instagram (même suffixe)

---

## 3. COMPTES FACEBOOK — DIY Selenium

### Pourquoi pas d'OS
- Les bots FB Creator existants sont soit morts, soit des scams, soit des versions freemium qui limitent tout
- Facebook change son flow d'inscription toutes les 2 semaines
- Seule solution fiable : Selenium/Puppeteur maison avec les bons fingerprints

### Stack
- **Python** + Selenium + undetected-chromedriver
- **Fingerprints** : Fake agent, WebGL, canvas, fonts, screen resolution
- **Proxy** : Mobile 4G (obligatoire, datacenter = ban immédiat)
- **SMS** : 5sim pour le numéro de vérification
- **Captcha** : 2Captcha API (reCAPTCHA)

### Flow d'inscription FB (à automatiser)
1. Ouvrir facebook.com avec undetected-chromedriver + proxy
2. Remplir : prénom, nom, email, mot de passe, date naissance
3. Sélectionner genre
4. Résoudre le reCAPTCHA via 2Captcha
5. Soumettre le formulaire
6. Coder le code SMS reçu sur 5sim
7. Ajouter photo de profil
8. Ajouter bio randomisée
9. Ne pas follow, ne pas liker, ne rien faire les premières 24h
10. Marquer "creation" dans BDD

### Code minimal
```python
import undetected_chromedriver as uc
options = uc.ChromeOptions()
options.add_argument('--proxy-server=http://user:pass@ip:port')
driver = uc.Chrome(options=options)
driver.get('https://facebook.com')
# ... remplir le formulaire ...
```

---

## 4. TIKTOK — En attente

**Décision prise** : On ne touche pas à TikTok pour l'instant. Priorité à Meta.

Quand on y viendra :
- **hendrikbgr/TikTok-Account-Creator** : le seul OS trouvé, mais vérification manuelle requise
- **l-portet/tiktok-warmup-bot** : pour le warmup (iOS Voice Control)

---

## 5. LE FLUX COMPLET (portfolio par portfolio)

Pour chaque portfolio (ex: Adam) :

### J0 — Préparation
- [ ] 10 boîtes mail créées sur le serveur
- [ ] 1 proxy mobile attribué
- [ ] 10 photos de profil générées (IA)
- [ ] 10 bios randomisées préparées

### J1 — Comptes Facebook
- [ ] 10 comptes FB créés (Selenium DIY)
- [ ] Marquer "creation" dans BDD
- [ ] Attendre 24h avant toute action

### J2 — Comptes Instagram
- [ ] 10 comptes IG créés (insta_create)
- [ ] Marquer "creation" dans BDD

### J3 — Pages Facebook
- [ ] 10 pages FB créées (FB-Pages-Creator)
- [ ] Lier chaque page au compte FB correspondant

### J4 — Liaisons
- [ ] Chaque IG lié à sa page FB (même suffixe)
- [ ] Branded Content activé sur chaque IG

### J5 — Business Portfolio
- [ ] Le strateur (adam.strateur) crée le BP Meta
- [ ] Le strateur invite les 10 pages FB dans le BP
- [ ] Les 10 comptes acceptent l'invitation
- [ ] Marqués "actif" dans BDD

### J6 à J30 — Warmup
- [ ] Connexion quotidienne à chaque compte
- [ ] Likes, follows, scroll (comportement humain)
- [ ] Instagram : 15 min/jour minimum
- [ ] Facebook : 5 min/jour minimum
- [ ] Aucune publication avant J30

### J31+ — Publication
- [ ] Premier post organique
- [ ] Si pas de flag → planning automatisé activé

---

## 6. SERVICES PAYANTS

### Proxies
| Fournisseur | Prix | Type | Notes |
|-------------|:----:|------|-------|
| **BrightData** | ~5€/mois | Mobile 4G | Cher mais fiable |
| **IPRoyal** | ~3€/mois | Résidentiel | Pas cher, ok pour test |
| **Proxysale** | ~3-5€/mois | Mobile | Bon rapport qualité |
| **Hydrox** | ~3€/mois | Résidentiel | Pas cher, rotation auto |

**Règle** : 1 proxy = 1 compte. Pas de proxy tournant sur plusieurs comptes.

### SMS
| Fournisseur | Prix/numéro | Notes |
|-------------|:-----------:|-------|
| **5sim** | ~0.10-0.50€ | Large choix pays |
| **SMSActivate** | ~0.15-0.50€ | API fiable |
| **SMSPVA** | ~0.10-0.30€ | Bon marché |

**Règle** : 1 numéro = 1 compte. Pas de réutilisation.

### Captcha
| Fournisseur | Prix | Notes |
|-------------|:----:|-------|
| **2Captcha** | ~0.50€/1000 | Standard, fiable |
| **AntiCaptcha** | ~1-2€/1000 | Plus cher, plus rapide |

---

## 7. BUDGET CUMULÉ (création uniquement)

### Test — Portfolio A (Adam)
| Item | Qté | € |
|------|:---:|:-:|
| Proxy mobile 1 mois | 1 | 3-5 |
| SMS (x10 comptes) | 10 | 1-5 |
| Captcha (x10 comptes) | ~200 | ~0.10 |
| Photos IA | 10 | 0 |
| **Total** | | **~5-10€** |

### Scale — 26 portfolios
| Item | Qté | €/mois | € une fois |
|------|:---:|:-------:|:----------:|
| Proxies | 26 | 80-130 | - |
| SMS | 260 | - | 26-130 |
| Captcha | ~5200 | - | ~3-10 |
| Photos IA | 260 | - | 0 |
| **Total** | | **80-130€/mois** | **29-140€** |

---

## 8. SERVICES À CHOISIR (décision Kevyn)

- [ ] Quel fournisseur de proxies ?
- [ ] Quel fournisseur SMS ?
- [ ] Quel fournisseur captcha ?
- [ ] Budget mensuel alloué ?
- [ ] Feu vert pour lancer le test sur Adam ?

---

## 9. BONNES PRATIQUES (les apprendre, ne pas les oublier)

- Ne JAMAIS créer un compte depuis un datacenter
- Ne JAMAIS utiliser le même proxy pour 2 comptes
- Ne JAMAIS publier le jour de la création du compte
- Attendre 24h MINIMUM avant toute action après création
- Randomiser les timings (pas 10 comptes créés à la seconde près)
- Randomiser les fingerprints (user-agent, résolution, polices)
- Utiliser des vrais noms + vraies photos pour les profils (générées IA)
- Warmup progressif : J1→J5 juste connexion, J6→J15 likes/follows, J16+ posts
- Un compte shadowban = 7 jours de pause, pas de suppression
- Un compte bloqué = on abandonne, pas de réclamation
