# Contexte actuel - Le Lab

## Rôle du fichier

`CONTEXTE-ACTUEL.md` est la fiche de démarrage rapide d'Alan.

Alan lit ce fichier au début du travail avec `00-ALAN-CEO-CTO.md`.

Ce fichier doit être court en consommation de tokens, mais assez détaillé pour être efficace. Taille cible : 3 à 4 pages maximum.

## Phase actuelle

Phase actuelle : **structuration initiale du Lab**.

Le projet met en place : gouvernance d'Alan, agents permanents, documentation Markdown, structure des comptes et infrastructure serveur / GitHub / base de données / Mailcow.

## Sens rapide du projet

Le Lab est un projet e-commerce dont l'objectif est de vendre des produits grâce à du contenu organique publié sur une multitude de comptes sociaux : Instagram, Facebook, TikTok et YouTube.

## Alan

Alan est le **CEO & CTO du Lab**. Il est l'agent principal et le chef d'orchestre du projet.

Alan est autonome par défaut. Il demande validation à Kevyn uniquement pour les décisions critiques : coût, suppression de fichiers importants, DNS, accès sensibles, architecture principale, automatisation à grande échelle, modification massive de base de données.

## Budget et modèles IA

Budget IA maximum : **20 € / mois**.

Modèles disponibles : DeepSeek et Ollama local petite version. OpenRouter est prévu à terme.

Au début, Alan demande validation avant d'utiliser ou de changer de modèle pour une tâche importante.

## Agents permanents validés

- `00-ALAN-CEO-CTO.md`
- `01-AGENT-CREATION-COMPTES.md`
- `02-AGENT-HISTORIQUE-IDENTITES.md`
- `03-AGENT-PUBLICATION.md`
- `04-AGENT-DATA-STATISTIQUES.md`
- `05-AGENT-ANALYSE-PERFORMANCE.md`
- `06-AGENT-SUPERVISEUR-AUDIT.md`
- `07-AGENT-INFRASTRUCTURE.md`
- `08-AGENT-DOCUMENTATION-MD.md`

Agents actifs au démarrage : Alan, Agent Documentation MD, Agent Création Comptes, Agent Infrastructure.

Agents en veille : Historique & Identités, Publication, Data & Statistiques, Analyse Performance, Superviseur & Audit.

## Structure comptes validée

- 1 prénom = 1 groupe / portfolio (A → Z)
- **12 suffixes** par prénom : app, biz, fr, hub, ideaz, idies, labs, media, news, studio, web, strateur
- Compte principal : `prenom.ideaz`
- Strateur : `prenom.strateur` (admin portfolio)
- 26 portfolios × 12 boîtes = 312 boîtes publication + 6 système = 318 boîtes totales
- Domaine : automatisations.org (avec s)
- DNS : Cloudflare (clint.ns.cloudflare.com / nina.ns.cloudflare.com)
- Mot de passe unique pour les boîtes publication (stocké en base)
- Date de naissance par défaut : 15/10/1978

## Infrastructure mail (Mailcow)

- **Serveur :** Mailcow Docker (mailcowdockerized)
- **Composants :** nginx → Postfix → Dovecot → MySQL + Rspamd + Redis + Let's Encrypt
- **Interface :** SOGo sur https://mail.automatisations.org
- **Corrections appliquées :**
  - SMTPUTF8 désactivé (conflit Dovecot)
  - IPv4 forcé pour Postfix (Gmail rejette IPv6 sans PTR)
  - attributes mailbox_format sur toutes les boîtes (fix "User unknown")
- **Script :** mailcow.py (création automatisée par lots)

## Source documentaire

Source principale : serveur.

GitHub : sauvegarde historisée.

Alan lit les fichiers sur le serveur. GitHub ne remplace pas le serveur comme source de travail.

Règle absolue : **ne rien perdre**.

## Fichiers centraux

- `00-ALAN-CEO-CTO.md`
- `CONTEXTE-ACTUEL.md`
- `ETAT-DU-PROJET.md`
- `AGENTS-ACTIFS.md`

Alan lit `00-ALAN-CEO-CTO.md` et `CONTEXTE-ACTUEL.md` au démarrage. Il lit les autres seulement si nécessaire.

## 🔐 Règles de sécurité

- Jamais de mots de passe, tokens, clés API, logins, IPs internes dans les emails ou messages à des tiers
- Gravée dans SOUL.md (Core Truths)
- Applicable à tous les agents du Lab

## Règle de mise à jour

Chaque agent peut mettre à jour son propre fichier Markdown.

Les agents ne modifient pas directement les fichiers centraux. Ils proposent une synthèse à Alan. Alan valide et met à jour si nécessaire.

## État opérationnel actuel

Validé : rôle d'Alan, autonomie d'Alan, liste des agents, agents comme business units, structure des comptes (12 suffixes), source serveur + GitHub, budget IA, audit hebdomadaire, gestion des incidents, structure contextes/ complète, files MD officiels remplacés sur le serveur, Mailcow opérationnel (318 boîtes), règle sécurité externe.

Résolu : DNS sur Cloudflare (étaient déjà chez Cloudflare, pas o2switch).

À faire : créer les comptes sociaux (FB, IG) pour commencer le test sur Adam.

## Décisions ouvertes

À arbitrer plus tard : règle exacte de publication, fonctionnement détaillé des agents Publication / Data / Analyse, choix précis de base de données, stratégie OpenRouter, autonomie future sur publications sociales réelles.

## Dernière mise à jour

2026-05-03
