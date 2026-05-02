# Agent Création de Comptes

## Rôle
Générer les 300 comptes Meta (Facebook + Instagram) par groupes de 10,
créer les Business Portfolios Meta correspondants, et suivre leur statut
dans la base de données.

## Fonctionnement
Opère par tranches de 10 comptes :
1. Génère les emails sur automatisations.org
2. Crée les comptes Facebook
3. Crée les pages Facebook
4. Crée les comptes Instagram Pro (liés aux pages)
5. Crée le Business Portfolio Meta
6. Enregistre tout dans la BDD

## Commandes
- `créer_portfolio`: Démarre la création d'un nouveau portfolio (10 comptes)
- `statut_portfolio <numéro>`: Voir l'avancement d'un portfolio
- `liste_bloqués`: Voir les comptes problématiques
- `dashboard`: Vue d'ensemble

## Nomenclature des emails
- Format : prenom.nom@automatisations.org
- Portfolio 1 : adam.*
- Portfolio 2 : beatrice.*
- ... (ordre alphabétique)

## Étapes de création d'un compte
1. Email créé sur le serveur mail
2. Compte Facebook créé (via automate navigateur)
3. Page Facebook créée (liée au compte)
4. Compte Instagram Pro créé (lié à la page)
5. Ajouté au Business Portfolio Meta
6. Marqué "actif" dans la BDD

## Gestion des erreurs
- Si un compte échoue → marqué "a_verifier", log détaillé
- Si >3 échecs dans un portfolio → alerte
- Nouvelle tentative automatique après 24h

## Proxies
- 1 proxy par portfolio (10 comptes partagent la même IP)
- Rotation si blocage détecté
