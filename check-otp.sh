#!/bin/bash
# Script de récupération OTP — Alan de Gira
# Vérifie les mails non lus sur toutes les boîtes OTP

SERVER="mail.automatisations.org"
PORT="993"
PASS="Automatisation1!"

# Boîtes à check
BOXES=(
  "otp@automatisations.org"
  "burgerparis0@automatisations.org"
  "burgerparis1@automatisations.org"
  "burgerparis2@automatisations.org"
  "burgerparis3@automatisations.org"
  "burgerparis4@automatisations.org"
  "burgerparis5@automatisations.org"
  "burgerparis6@automatisations.org"
  "burgerparis7@automatisations.org"
  "burgerparis8@automatisations.org"
  "burgerparis9@automatisations.org"
  "compte10@automatisations.org"
  "compte11@automatisations.org"
  "compte20@automatisations.org"
  "compte21@automatisations.org"
)

for BOX in "${BOXES[@]}"; do
  echo "📬 $BOX"
  curl -s --ssl \
    -u "$BOX:$PASS" \
    "imaps://$SERVER:${PORT}/INBOX?NEW" \
    2>/dev/null || echo "  ⚠️  Erreur de connexion"
done
