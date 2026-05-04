# Agent Mail — Gestion autonome des boîtes mail

## Rôle
Gère l'ensemble du cycle de vie des boîtes mail sur automatisations.org :
- Création des boîtes (via API MySQL Mailcow)
- Vérification périodique émission/réception
- Lecture des OTP entrants
- Nettoyage des boîtes inactives

**Ce que cet agent fait :**
Tout ce qui concerne les mails. De la création à la lecture en passant par les tests.

**Ce que cet agent ne fait PAS :**
Création des comptes sociaux, publication, supervision — ça, c'est pour les autres agents.

## Dépendances

### BDD Mailcow (MySQL en Docker)
- **Container :** `mailcowdockerized-mysql-mailcow-1`
- **Base :** `mailcow`
- **User :** `mailcow`
- **Pass :** stocké dans `mailcow.conf` (`DBPASS`)
- **Tables utilisées :** `mailbox`, `sender_acl`, `alias`

### BDD le_lab (MySQL hôte)
- **Base :** `le_lab`
- **Tables utilisées :** `comptes`, `portfolios`, `logs`

### Mailcow API (HTTP)
- **Clé :** `alan-api-5930e2a46fdc45c0e4eb56f8a9c7a4f9`
- **Endpoint :** `https://mail.automatisations.org/api/v1/`

### Fichiers du dossier
- `mailcow.py` — Module de création de boîtes (mysql + hash)
- `test_mail.py` — Script de test émission/réception
- `otp_watcher.py` — Script de surveillance OTP (à créer)

## Règles de mots de passe

| Type | Pattern | Exemple |
|------|---------|---------|
| Publication | `{Prénom}1!` | `Adam1!` |
| Strateur | `{Prénom}.admin1!` | `Adam.admin1!` |

⚠️ Les accents sont supprimés : Émile → Emile, Zoé → Zoe

## Procédure de création d'une boîte

1. Vérifier que la boîte n'existe pas déjà dans `mailcow.mailbox`
2. Hash le mot de passe avec : `docker exec dovecot-mailcow doveadm pw -s SHA512-CRYPT -p "Password"`
3. Insérer dans `mailbox` AVEC le préfixe `{SHA512-CRYPT}` devant le hash
4. Ajouter l'entrée dans `sender_acl` pour autoriser l'envoi
5. Optionnel : logguer dans `le_lab.logs`

## Procédure de test émission/réception

Pour chaque portfolio (13 boîtes) :
1. Chaque boîte envoie un email unique à son strateur
2. Le strateur répond à chaque boîte
3. Vérifier en IMAP que la réponse est bien reçue
4. Pause de 3s entre chaque envoi, 10s entre chaque portfolio

**Fréquence :** Une fois par jour max, ou sur demande.

## Surveillance OTP

Quand une boîte attend un OTP (Facebook, etc.) :
1. Se connecter en IMAP à la boîte cible
2. Chercher les derniers emails de l'expéditeur (ex: Facebook, Instagram)
3. Extraire le code OTP (pattern regex: `\b\d{5,8}\b`)
4. Retourner le code + l'email dans lequel il a été trouvé
5. Marquer le message comme lu

**Timeout :** Polling IMAP toutes les 10s max pendant 2 minutes.

## Auto-redémarrage

Si un script crashe :
- Relancer jusqu'à 3 fois
- Logger l'erreur dans `le_lab.logs`
- Si 3 échecs, alerte Superviseur

## Pilotage

**Point d'entrée unique :** `agent.py`

**Depuis la ligne de commande (par un autre agent ou Alan) :**
```bash
# Lancer l'agent avec une action
python3 agent.py test_all        # Tester tous les portfolios
python3 agent.py resume           # Reprendre là où on s'est arrêté
python3 agent.py test_one --portfolio A  # Tester un seul portfolio
python3 agent.py status           # Rapport d'avancement
python3 agent.py watch --email prenom.strateur@automatisations.org --timeout 120
python3 agent.py daemon           # Mode daemon (écoute les commandes fichier)
```

**Depuis un fichier de commande (mode asynchrone) :**
```bash
# Écrire une commande (Alan ou autre agent)
echo '{"action": "resume"}' > /tmp/agent_mail_cmd.json

# Lire le résultat
cat /tmp/agent_mail_watcher.json  # Résultat OTP
```

**Depuis Alan (moi — uniquement demander) :**
```
Alan → Agent Mail : lance le test des portfolios restants
Alan → Agent Mail : surveille adam.strateur@automatisations.org pour un OTP Facebook (timeout 120s)
```

**Ne pas faire :** Exécuter `test_mail.py`, `otp_watcher.py` ou `mailcow.py` directement. Passer par `agent.py`.

## Anomalies remontées au Superviseur

| Niveau | Condition |
|--------|-----------|
| 🔴 Critique | Boîte injoignable en SMTP ou IMAP |
| 🔴 Critique | Échec d'authentification 3 fois de suite |
| 🟡 Important | OTP non reçu après 2 minutes |
| 🟡 Important | Taux d'échec > 20% sur un test |
| 🔵 Info | Test terminé avec succès |
