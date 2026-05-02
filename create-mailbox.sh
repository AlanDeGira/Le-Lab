#!/bin/bash
# Script de création de boîte mail — utilisé par l'agent Création de Comptes
# Usage: ./create-mailbox.sh <local_part> <display_name> <linked_account>

if [ $# -lt 2 ]; then
  echo "Usage: $0 <local_part> <display_name> [linked_account]"
  echo "Ex: $0 burgerparis22 'Compte VingtDeux' burgerparis22"
  exit 1
fi

LOCAL_PART="$1"
DISPLAY_NAME="$2"
LINKED_ACCOUNT="${3:-$LOCAL_PART}"
EMAIL="${LOCAL_PART}@automatisations.org"
PASSWORD="Automatisation1!"

MYSQL_CMD="mysql -u mailcow -pJKTKg6HzlIwN5ihTMhc8bO5i8LxX mailcow"
PGSQL_CMD="psql -U n8n -d instagram_farming"
PASSWORD_HASH='{BLF-CRYPT}$2y$05$F0Xv7I19hTv69GCL0BXc6.XPsAVUE1me3qdC6Shts5MluJiKF94LG'

# 1. Vérifier si la boîte existe déjà dans Mailcow
EXISTS=$(docker exec mailcowdockerized-mysql-mailcow-1 $MYSQL_CMD -N -e \
  "SELECT COUNT(*) FROM mailbox WHERE username='$EMAIL';" 2>/dev/null)

if [ "$EXISTS" -gt 0 ]; then
  echo "EXISTS:$EMAIL"
  exit 2
fi

# 2. Créer la boîte dans Mailcow
docker exec mailcowdockerized-mysql-mailcow-1 $MYSQL_CMD -e \
  "INSERT INTO mailbox (username, password, name, local_part, domain, kind, active)
   VALUES ('$EMAIL', '$PASSWORD_HASH', '$DISPLAY_NAME', '$LOCAL_PART', 'automatisations.org', 'mailbox', 1);" 2>/dev/null

if [ $? -ne 0 ]; then
  echo "ERROR: Échec création Mailcow pour $EMAIL"
  exit 3
fi

echo "CREATED:$EMAIL"

# 3. Archiver dans PostgreSQL
docker exec n8n-db-1 $PGSQL_CMD -c \
  "INSERT INTO mail_accounts (email, display_name, password, purpose, linked_account)
   VALUES ('$EMAIL', '$DISPLAY_NAME', '$PASSWORD', 'otp', '$LINKED_ACCOUNT')
   ON CONFLICT (email) DO NOTHING;" 2>/dev/null

echo "ARCHIVED:$EMAIL"
