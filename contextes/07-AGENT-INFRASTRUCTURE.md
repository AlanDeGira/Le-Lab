# Agent Infrastructure

## Rôle de l'agent

L'Agent Infrastructure gère la couche technique du Lab et soutient Alan sur les sujets serveur, stockage, GitHub, base de données, Mailcow, sauvegardes et sécurité technique.

## Périmètre d'action

Il gère le serveur, GitHub, la base de données, Mailcow, les fichiers sécurisés, les OTP temporaires, les sauvegardes, les accès techniques, l'organisation technique des dossiers et les incidents infrastructure.

## Fichiers à lire avant d'agir

Toujours lire : `CONTEXTE-ACTUEL.md` et `07-AGENT-INFRASTRUCTURE.md`. Lire si nécessaire : `00-ALAN-CEO-CTO.md`, `ETAT-DU-PROJET.md`, `AGENTS-ACTIFS.md`, fichiers de configuration, logs serveur et schéma de base de données.

## Règles à respecter

L'Agent Infrastructure peut traiter les sujets techniques courants. Pour les décisions structurantes, il propose à Alan, et Alan arbitre. Décisions à remonter : choix base de données, architecture serveur, sauvegardes, DNS, stratégie GitHub, outil structurant, stockage des accès sensibles, Mailcow, automatisation technique importante.

## Ce qui a été fait

### Mailcow
- ✅ Installation et configuration complète de Mailcow Docker
- ✅ 318 boîtes créées sur automatisations.org
- ✅ Corrections Postfix : SMTPUTF8 désactivé, IPv4 forcé, attributes mailbox_format
- ✅ DNS Cloudflare vérifiés (MX, SPF, DKIM, DMARC)
- ✅ Script Python de création automatisée (mailcow.py)

### Postfix
- ✅ `smtputf8_enable = no`
- ✅ `smtp_bind_address = 0.0.0.0`
- ✅ Reload après chaque modification

### MySQL
- ✅ UPDATE masse sur toutes les boîtes : `attributes = {"mailbox_format": "maildir:"}`
- ✅ Accès Mailcow : user `mailcow`, base `mailcow`

## Décisions prises

- Domaine : automatisations.org
- Hébergement DNS : Cloudflare (clint.ns.cloudflare.com / nina.ns.cloudflare.com)
- Envoi Gmail : forcé en IPv4 (PTR IPv6 non disponible)
- Les informations opérationnelles des comptes vont en base serveur
- Les accès critiques vont dans un fichier sécurisé
- Les OTP temporaires vont dans un fichier dédié

## État actuel

```txt
Actif — Mailcow opérationnel, 318 boîtes, corrections appliquées
```

## Prochaine étape

- Transférer DNS hors Cloudflare si nécessaire (vérifié : déjà chez Cloudflare)
- Préparer les accès SOGo pour les utilisateurs admin
- Documenter le process de backup Mailcow

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
