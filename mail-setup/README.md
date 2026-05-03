# Mail OTP — automatisations.org

## 1. DNS (Cloudflare) — vérifiés
- ✅ NS : clint.ns.cloudflare.com / nina.ns.cloudflare.com
- ✅ MX → mail.automatisations.org (priorité 10)
- ✅ SPF (v=spf1 mx ~all)
- ✅ DKIM (mail._domainkey — généré par Rspamd)
- ✅ DMARC (_dmarc)

## 2. Infrastructure déployée
- **Serveur :** Mailcow Docker (mailcowdockerized)
- **Stack complète :** nginx → Postfix (SMTP) → Dovecot (IMAP/POP3) → MySQL
- **Antispam :** Rspamd (signature DKIM active)
- **SSL :** Let's Encrypt (auto via acme-mailcow)
- **Interface web :** SOGo sur https://mail.automatisations.org
- **Boîtes créées :** 318 (312 publication + 6 système)
- **MVP gestion :** Script Python mailcow.py (hash Dovecot + INSERT MySQL)

## 3. Corrections appliquées
- `smtputf8_enable = no` (conflit Dovecot)
- `smtp_bind_address = 0.0.0.0` (force IPv4 — Gmail rejette IPv6 sans PTR)
- `attributes = {"mailbox_format": "maildir:"}` sur toutes les boîtes (fix "User unknown")
- Reload Postfix après chaque modif

## 4. Créer une boîte mail

### Méthode SQL directe
```bash
HASH=$(docker exec mailcowdockerized-dovecot-mailcow-1 doveadm pw -s SHA512-CRYPT -p "MotDePasse")
docker exec mailcowdockerized-mysql-mailcow-1 mariadb -u mailcow -p<PASS> mailcow -e \
  "INSERT INTO mailbox (username, password, name, local_part, domain, kind, quota, active)
   VALUES ('user@automatisations.org', '$HASH', 'Display Name', 'user', 'automatisations.org', 'mailbox', 1073741824, 1);"
```

### Méthode SOGo (interface web)
- https://mail.automatisations.org/SOGo → connexion admin → Mailboxes → Add mailbox

## 5. Tester
- Envoyer depuis Gmail vers n'importe quelle adresse du domaine
- Vérifier la réception : IMAP mail.automatisations.org port 143
- Vérifier DKIM : https://www.appmail.dev/dkim-check/

## 6. État
- ✅ DNS OK (Cloudflare)
- ✅ Mailcow opérationnel
- ✅ 318 boîtes créées
- ✅ Corrections Postfix appliquées
- ⚠️ PTR IPv6 non configurable (hébergeur VPS) → contourné par envoi IPv4
