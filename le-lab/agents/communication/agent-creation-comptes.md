# Agent Création de Comptes — Mise à jour mail

## Rôle
Créer les boîtes mail pour les 26 portfolios sur le domaine automatisations.org.

## Infrastructure mail
- **Serveur :** Mailcow Docker (mailcowdockerized)
- **Base :** MySQL (table `mailbox`)
- **SMTP :** Postfix (envoi forcé en IPv4)
- **IMAP :** Dovecot
- **Interface web :** SOGo sur https://mail.automatisations.org

## Boîtes créées (318 au total)

### 312 boîtes publication
26 prénoms (Adam → Zoé) × 12 suffixes :

| Groupe | Suffixes |
|--------|----------|
| Web/App | app, web, fr |
| Projets | hub, labs, studio |
| Média | media, news, ideaz, idies |
| Business | biz |
| Admin | strateur |

Format : `prenom.suffixe@automatisations.org`

### 6 boîtes système
- `admin@automatisations.org` — Admin Mailcow
- `contact@automatisations.org` — Contact général
- `otp@automatisations.org` — Bot OTP
- `test@automatisations.org` — Test
- `validation@automatisations.org` — Validation email
- `alan.degira@automatisations.org` — Alan (personnelle)

## DNS (Cloudflare)
- NS : clint.ns.cloudflare.com / nina.ns.cloudflare.com
- MX : mail.automatisations.org (priorité 10)
- SPF : v=spf1 mx ~all
- DKIM : mail._domainkey (généré par Rspamd)
- DMARC : _dmarc (p=none)

## Méthodes de création

### Interface SOGo (manuel)
- Connexion admin sur https://mail.automatisations.org/SOGo
- Mailboxes → Add mailbox

### SQL direct
```sql
UPDATE mailbox SET attributes = '{"mailbox_format": "maildir:"}';
-- Requis pour que Postfix trouve les boîtes
```

### Script Python (mailcow.py)
- Automatisation par lots (hash Dovecot + INSERT MySQL)

## Config Postfix (corrections appliquées)
- `smtputf8_enable = no` — évite le conflit SMTPUTF8/Dovecot
- `smtp_bind_address = 0.0.0.0` — force IPv4 (Gmail rejette IPv6 sans PTR)
- `attributes = {"mailbox_format": "maildir:"}` sur TOUTES les boîtes

## Mémo technique
- Mot de passe générique pour les boîtes publication (stocké dans la base, jamais transmis)
- Admin mailcow : utilisateur `mailcow` / base `mailcow`
- Quota par défaut : 100 Mo (publication) / 5 Go (système)
