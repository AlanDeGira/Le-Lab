# État du projet - Le Lab

## Rôle du fichier

`ETAT-DU-PROJET.md` est la photographie claire de l'état du Lab à un instant donné.

Il doit permettre de comprendre exactement où en est le projet à chaque lecture.

## Sens global du projet

Le Lab est un projet e-commerce dont l'objectif est de vendre des produits grâce à du contenu organique publié sur une multitude de comptes sociaux.

Le projet s'appuie sur une organisation d'agents, une infrastructure serveur, des fichiers Markdown de contexte, des comptes sociaux structurés, des contenus organiques, une base de données, une analyse de performance et une logique d'optimisation des coûts IA.

## Gouvernance

Alan est le CEO & CTO du Lab. Il est le chef d'orchestre du projet et gère la vision, la technique, les agents, les arbitrages, les coûts IA, le serveur, GitHub, les fichiers Markdown et la cohérence générale.

Alan est autonome par défaut. Kevyn intervient uniquement pour les décisions critiques.

## État actuel

Le projet est en phase de structuration initiale.

La priorité actuelle est de finaliser l'infrastructure mail et de démarrer la création des comptes sociaux.

## Ce qui est validé

- Le projet s'appelle **Le Lab**.
- Le Lab vise la vente de produits e-commerce via contenu organique.
- Alan est CEO & CTO.
- Alan est autonome sauf décisions critiques.
- Budget IA : 20 € / mois.
- Modèles : DeepSeek + Ollama local, OpenRouter plus tard.
- Les fichiers Markdown sont sur le serveur.
- GitHub est une sauvegarde historisée.
- Alan peut faire les commits lui-même en français.
- Les agents permanents sont validés.
- La structure des comptes est validée.

## Agents permanents

- Alan
- Agent Création Comptes
- Agent Historique & Identités
- Agent Publication
- Agent Data & Statistiques
- Agent Analyse Performance
- Agent Superviseur & Audit
- Agent Infrastructure
- Agent Documentation MD

## Structure comptes validée (MAJ 03/05)

- 1 prénom = 1 groupe / portfolio (26 lettres A→Z)
- **12 suffixes** par prénom : app, biz, fr, hub, ideaz, idies, labs, media, news, studio, web, **strateur**
- Compte principal : `prenom.ideaz`
- Strateur (admin) : `prenom.strateur`
- Date de naissance : 15/10/1978
- Email : `prenom.suffixe@automatisations.org`
- Instagram / TikTok : `@prenom.suffixe`
- Facebook / Page Facebook / YouTube : `Prénom Suffixe`
- Mot de passe unique pour boîtes publication (stocké en base)

## Infrastructure mail (MAJ 03/05)

- Mailcow Docker opérationnel (mailcowdockerized)
- 318 boîtes mail créées (312 publication + 6 système)
- DNS Cloudflare : MX, SPF, DKIM, DMARC (vérifiés)
- Corrections Postfix : SMTPUTF8 off, IPv4 forcé, attributes mailbox_format
- Envoi/réception Gmail fonctionnel (IPv4)
- Interface SOGo sur https://mail.automatisations.org

## Arbitrages déjà faits

| Sujet | Arbitrage |
|---|---|
| Relance session à 50% contexte | Alan propose, Kevyn valide ou refuse |
| Règle recontextualisation | Début de session : Alan lit 00 + CONTEXTE-ACTUEL uniquement |
| DOMAINE EMAIL | automatisations.org (avec s) |
| HÉBERGEMENT DNS | Cloudflare (clint / nina) — vérifié, pas o2switch |
| SUFFIXES DÉFINITIFS | app, biz, fr, hub, ideaz, idies, labs, media, news, studio, web, strateur |
| DATE NAISSANCE | 15/10/1978 (remplace 1990-01-01) |
| MOT DE PASSE | Unique pour toutes les boîtes publication (jamais transmis par mail) |
| YOUTUBE | Réintégré dans la structure comptes (non prioritaire) |
| AGENTS SOURCES | Fichiers officiels fournis par Kevyn → version serveur actualisée |
| STRUCTURE DOSSIER | contextes/ (12 fichiers) + incidents/ |
| Rôle d'Alan | Alan est CEO & CTO du Lab |
| Autonomie | Alan est autonome sauf décisions critiques |
| Budget IA | Maximum 20 € / mois |
| Modèles | DeepSeek + Ollama local, OpenRouter plus tard |
| Source MD | Serveur |
| GitHub | Sauvegarde historisée |
| Commits | Alan peut les faire lui-même en français |
| Agents | 8 agents permanents + Alan |
| Agents temporaires | Créés si besoin puis supprimés |
| Agents actifs au démarrage | Alan, Documentation MD, Création Comptes, Infrastructure |
| Fichiers centraux | Alan valide les modifications |
| Agent Superviseur | Audit hebdomadaire le dimanche soir |
| Informations opérationnelles | Base de données serveur |
| Accès critiques | Fichier sécurisé serveur |
| OTP | Fichier spécial temporaire |
| Google Workspace | Supprimé pour le moment |
| **SÉCURITÉ EXTERNE** | **Jamais de credentials dans les emails/messages à des tiers (règle absolue)** |
| **SMTPUTF8** | Désactivé (conflit Dovecot) |
| **ENVOI IPv4** | Forcé (Gmail rejette IPv6 sans PTR) |
| **ATTRIBUTES MAILBOX** | `{"mailbox_format": "maildir:"}` sur toutes les boîtes |

## Décisions en attente

| Sujet | Options | Urgence | Impact | Arbitre | Prochaine action |
|---|---|---|---|---|---|
| Règle de publication | À définir | Moyenne | Élevé | Kevyn + Alan | Définir plus tard avec Agent Publication |
| Fonction détaillée Agent Publication | À définir | Moyenne | Élevé | Alan | À traiter quand publication démarre |
| Fonction détaillée Agent Data | À définir | Moyenne | Moyen | Alan | À traiter quand stats disponibles |
| Fonction détaillée Agent Analyse | À définir | Moyenne | Moyen | Alan | À traiter quand données disponibles |
| Base de données | SQLite / MySQL / PostgreSQL / autre | Moyenne | Élevé | Alan propose | Décider selon besoin réel |
| OpenRouter | Intégration future | Faible | Moyen | Alan | Étudier plus tard |
| Autonomie sur publications | À définir | Moyenne | Élevé | Kevyn + Alan | Attendre règles publication |

## Risques / points de vigilance

| Risque | Niveau | Impact | Responsable | Action de prévention |
|---|---|---|---|---|
| Perte de fichiers MD | Élevé | Très important | Alan | Sauvegarde serveur + GitHub |
| Contexte trop long | Moyen | Coût IA élevé | Alan | Garder `CONTEXTE-ACTUEL.md` compact |
| Agents incohérents | Moyen | Mauvaise exécution | Agent Superviseur & Audit | Audit hebdomadaire |
| Coûts IA trop élevés | Moyen | Dépassement budget | Agent Superviseur & Audit | Suivi hebdomadaire |
| Accès sensibles mal stockés | Élevé | Risque sécurité | Alan + Infrastructure | Fichier sécurisé serveur |
| Publication non cadrée | Élevé | Risque opérationnel | Alan + Agent Publication | Règle à définir avant exécution |
| Contenus sans droits clairs | Élevé | Risque juridique | Agent Publication | Vérifier preuve de droit |
| **PTR IPv6 manquant** | **Faible** | Envoi Gmail | Infrastructure | Contourné par IPv4 forcé |

## Ce qui reste à faire

Fait cette session :
- ✅ 318 boîtes mail créées (312 + 6 système)
- ✅ Corrections Postfix : SMTPUTF8 off, IPv4 forcé, attributes mailbox_format
- ✅ DNS Cloudflare vérifiés (étaient déjà chez Cloudflare)
- ✅ Règle de sécurité externe instaurée (jamais de credentials aux tiers)
- ✅ Envoi récap mail à Ahmidouche (architecture safe)
- ✅ Mise à jour de tous les .md concernés

Reste à faire :
- Créer les comptes sociaux (test sur Adam d'abord)
- Définir la base de données quand le besoin sera concret
- Préparer les règles de publication plus tard

## Dernière mise à jour

2026-05-03
