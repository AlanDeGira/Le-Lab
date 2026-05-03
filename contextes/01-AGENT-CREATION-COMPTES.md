# Agent Création Comptes

## Rôle de l'agent

L'Agent Création Comptes prépare, structure et suit la création des comptes sociaux du Lab. Il intervient avant la publication et avant l'analyse.

## Périmètre d'action

Il gère la nomenclature des comptes, les prénoms, les suffixes, la **création des boîtes mail** (via Mailcow), les emails, les comptes Facebook, les pages Facebook, les comptes Instagram, TikTok, YouTube, les statuts de création et la transmission des informations utiles à l'Agent Historique & Identités. Il ne gère pas la publication, les statistiques ou l'analyse.

## Fichiers à lire avant d'agir

Toujours lire : `CONTEXTE-ACTUEL.md` et `01-AGENT-CREATION-COMPTES.md`. Lire si nécessaire : `ETAT-DU-PROJET.md`, `AGENTS-ACTIFS.md`, `02-AGENT-HISTORIQUE-IDENTITES.md` et les données de comptes en base.

## Règles à respecter

- Domaine email : **automatisations.org** (avec s)
- Structure : `prenom.suffixe@automatisations.org`
- Instagram/TikTok : `@prenom.suffixe`
- Facebook/Page Facebook/YouTube : `Prénom Suffixe`
- **12 suffixes validés :** app, biz, fr, hub, ideaz, idies, labs, media, news, studio, web, strateur
- Strateur : `prenom.strateur@automatisations.org` (admin portfolio)
- Compte principal : `prenom.ideaz`
- **Mot de passe unique** pour toutes les boîtes publication (stocké en base)
- Date de naissance : 15/10/1978

## Ce qui a été fait

- ✅ 26 portfolios créés (A→Z) avec leurs 12 boîtes chacun
- ✅ 312 boîtes publication + 5 système + 1 perso = 318 boîtes totales
- ✅ Validation automatique : envoi test vers validation@automatisations.org
- ✅ Corrections Postfix appliquées (SMTPUTF8, IPv4, attributes)
- ✅ Toutes les boîtes peuvent recevoir des mails (Gmail testé ok)
- ✅ DNS Cloudflare vérifiés et opérationnels

### Infrastructure mail actuelle
- **Serveur :** Mailcow Docker (mailcowdockerized)
- **SMTP :** Postfix (IPv4 forcé pour Gmail)
- **IMAP :** Dovecot
- **Web :** SOGo sur https://mail.automatisations.org
- **Base :** MySQL (table mailbox, 318 entrées)

## Décisions prises

- Domaine officiel : automatisations.org (avec s)
- DNS : Cloudflare (clint.ns.cloudflare.com / nina.ns.cloudflare.com)
- Strateur obligatoire : prenom.strateur pour chaque portfolio
- 12 suffixes définitifs : app, biz, fr, hub, ideaz, idies, labs, media, news, studio, web, strateur
- Création des boîtes mail intégrée au périmètre de l'agent
- Mot de passe unique pour les boîtes publication (générique, stocké en base)
- L'agent crée les boîtes mail Mailcow avant que les outils externes créent les comptes sociaux

## État actuel

```txt
Actif — 318 boîtes créées, en attente création comptes sociaux
```

## Prochaine étape

Créer les comptes sociaux (Facebook, Instagram) via les outils externes (Selenium, insta_create).

---

## Mise à jour après tâche

À la fin d'une tâche, l'agent doit :

1. mettre à jour son propre fichier Markdown ;
2. résumer ce qui a été fait ;
3. noter les décisions prises sur son périmètre ;
4. indiquer l'état actuel ;
5. indiquer la prochaine étape utile si nécessaire ;
6. proposer à Alan une mise à jour de `CONTEXTE-ACTUEL.md` si le contexte central doit changer ;
7. proposer à Alan une mise à jour de `ETAT-DU-PROJET.md` si un arbitrage, une décision ou un état important a changé.

L'agent ne modifie pas directement les fichiers centraux. Alan valide les modifications centrales.

## Dernière mise à jour

2026-05-03
