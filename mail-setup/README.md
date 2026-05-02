# Mail OTP — automatisations.org

## 1. DNS déjà configurés (Cloudflare)
- ✅ MX → mail.automatisations.org
- ✅ SPF (v=spf1 mx ~all)
- ✅ DKIM (mail._domainkey)
- ✅ DMARC (_dmarc)

## 2. Installation sur le serveur

```bash
# Copier les fichiers sur le serveur
# Puis :
cd /home/n8nuser/n8n
# Ajouter le contenu du docker-compose mail au docker-compose existant,
# OU créer un docker-compose séparé :
cp /root/mail-setup/docker-compose.yml ./
docker compose up -d
```

## 3. Créer des boîtes mail

```bash
# Créer un utilisateur mail pour OTP
docker exec mail-postfix adduser otp@automatisations.org
docker exec mail-postfix passwd otp@automatisations.org
# Mot de passe par défaut : changer immédiatement
```

## 4. Tester
- Envoyer un mail à otp@automatisations.org
- Vérifier la réception : IMAP mail.automatisations.org port 143
- Vérifier DKIM : https://www.appmail.dev/dkim-check/
