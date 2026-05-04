#!/usr/bin/env python3
"""
Test massif des 318 boîtes mail — Émission, réception et lecture.
Par portfolio, en interne (pas de Gmail).

Flux :
1. Chaque boîte envoie un email unique à son strateur
2. Le strateur répond à toutes
3. On vérifie IMAP que la réponse est bien reçue
4. On log tout dans le_lab.logs

Usage :
  python3 test_mail_massif.py         # Test complet des 26 portfolios
  python3 test_mail_massif.py --lot A # Test d'un seul portfolio
  python3 test_mail_massif.py --status # État d'avancement
"""

import smtplib
import imaplib
import ssl
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import sqlite3
import os
import sys
import json
import time
import uuid
import re
from datetime import datetime, timedelta
from pathlib import Path

# ─── CONFIG ─────────────────────────────────────────────────────────────────

SMTP_HOST = "127.0.0.1"
SMTP_PORT = 587
IMAP_HOST = "127.0.0.1"
IMAP_PORT = 993
DOMAIN = "automatisations.org"

MAILCOW_PASS = "Lun49BMX6Ba38L3lspqACCqvDpqY"

BASE_DIR = Path(__file__).resolve().parent.parent.parent  / "le-lab"
DB_PATH = BASE_DIR / "data" / "le-lab.db"
LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

SESSION_LOG = LOG_DIR / f"test_mail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

PAUSE_LOT = 3       # Pause entre chaque envoi d'un lot
PAUSE_PORTFOLIO = 10 # Pause entre chaque portfolio
TIMEOUT = 30         # Timeout SMTP/IMAP

# ─── PRÉNOMS ────────────────────────────────────────────────────────────────

PRENOMS = {
    1: 'Adam', 2: 'Baptiste', 3: 'Camille', 4: 'Diane', 5: 'Émile',
    6: 'Flora', 7: 'Gabriel', 8: 'Hugo', 9: 'Iris', 10: 'Jules',
    11: 'Karine', 12: 'Léo', 13: 'Manon', 14: 'Nathan', 15: 'Oscar',
    16: 'Paul', 17: 'Quentin', 18: 'Romane', 19: 'Sacha', 20: 'Théo',
    21: 'Ulysse', 22: 'Valentin', 23: 'William', 24: 'Xander',
    25: 'Yasmine', 26: 'Zoé',
}

SUFFIXES_PUBLICATION = [
    'app', 'web', 'fr', 'hub', 'labs', 'studio',
    'media', 'news', 'ideaz', 'idies', 'biz',
]
SUFFIXE_STRATEUR = 'strateur'

# ─── BDD LOCALE ──────────────────────────────────────────────────────────────

def _get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def _init_tracking():
    """Crée la table de suivi du test si elle n'existe pas."""
    conn = _get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS test_mail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            portfolio_num INTEGER,
            prenom TEXT,
            suffixe TEXT,
            etape TEXT,   -- 'envoi', 'attente_reponse', 'verification', 'ok', 'echec'
            message_id TEXT,
            sujet TEXT,
            statut TEXT DEFAULT 'en_attente',
            erreur TEXT,
            date_test TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duree_ms INTEGER
        )
    """)
    conn.commit()
    conn.close()

def _log_result(email, portfolio_num, prenom, suffixe, etape, statut, erreur=None, message_id=None, sujet=None, duree_ms=None):
    conn = _get_db()
    conn.execute("""
        INSERT INTO test_mail (email, portfolio_num, prenom, suffixe, etape, message_id, sujet, statut, erreur, duree_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (email, portfolio_num, prenom, suffixe, etape, message_id, sujet, statut, erreur, duree_ms))
    conn.commit()
    conn.close()

def _log_signalement(niveau, source, message, details=None):
    conn = _get_db()
    conn.execute("""
        INSERT INTO logs (niveau, source, message, details)
        VALUES (?, ?, ?, ?)
    """, (niveau, source, message, json.dumps(details) if details else None))
    conn.commit()
    conn.close()

# ─── HELPER MDP ──────────────────────────────────────────────────────────────

def _get_password(prenom, suffixe=None):
    """Génère le mot de passe selon la règle établie."""
    if prenom == 'Émile':
        prenom_clean = 'Emile'
    else:
        prenom_clean = prenom
    
    if suffixe == SUFFIXE_STRATEUR:
        return f"{prenom_clean}.admin1!"
    else:
        return f"{prenom_clean}1!"

def _get_prenom_clean(prenom):
    """Nettoie les accents pour les mots de passe."""
    replacements = {'É': 'E', 'é': 'e', 'È': 'E', 'è': 'e'}
    result = prenom
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result

# ─── SMTP ────────────────────────────────────────────────────────────────────

def _send_email(from_email, from_pw, to_email, subject, body):
    """Envoie un email via SMTP avec STARTTLS. Retourne le message_id."""
    start = time.time()
    
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Message-ID'] = f"<{uuid.uuid4().hex}@test.automatisations.org>"
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    msg.attach(MIMEText(f"<p>{body}</p>", 'html', 'utf-8'))
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=TIMEOUT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(from_email, from_pw)
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()
        
        duree = int((time.time() - start) * 1000)
        return msg['Message-ID'], duree
    except Exception as e:
        raise

# ─── IMAP ────────────────────────────────────────────────────────────────────

def _check_imap(mailbox, password, search_criteria='ALL', max_attempts=5, delay=5):
    """
    Vérifie via IMAP si des emails sont présents.
    Réessaie plusieurs fois (laisse le temps à Postfix de livrer).
    Retourne les messages trouvés.
    """
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    for attempt in range(max_attempts):
        try:
            mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context, timeout=TIMEOUT)
            mail.login(mailbox, password)
            mail.select('INBOX')
            
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                mail.logout()
                if attempt < max_attempts - 1:
                    time.sleep(delay)
                continue
            
            raw_ids = messages[0] if isinstance(messages[0], bytes) else messages[0]
            message_ids = raw_ids.split() if raw_ids else []
            results = []
            
            for mid in message_ids:
                status, msg_data = mail.fetch(mid, '(RFC822)')
                if status != 'OK':
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple) and len(response_part) >= 2:
                        raw_email = response_part[1]
                        if isinstance(raw_email, bytes):
                            email_msg = email.message_from_bytes(raw_email)
                        else:
                            continue
                        
                        subject = _decode_header(email_msg['Subject'])
                        from_addr = email_msg['From']
                        date_str = email_msg['Date']
                        msg_id = email_msg['Message-ID']
                        
                        body = _get_email_body(email_msg)
                        
                        results.append({
                            'subject': subject,
                            'from': from_addr,
                            'date': date_str,
                            'message_id': msg_id,
                            'body': body[:500],
                        })
            
            mail.logout()
            
            if results or attempt >= max_attempts - 1:
                return results
            
            time.sleep(delay)
            
        except Exception as e:
            if attempt >= max_attempts - 1:
                raise
            time.sleep(delay)
    
    return []

def _decode_header(header_value):
    """Décode un header email encodé."""
    if not header_value:
        return ""
    decoded_parts = decode_header(header_value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(charset or 'utf-8', errors='replace'))
            except:
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(str(part))
    return ''.join(result)

def _get_email_body(email_msg):
    """Extrait le corps texte d'un email."""
    if email_msg.is_multipart():
        for part in email_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition', ''))
            
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        return payload.decode(charset, errors='replace')
                except:
                    pass
            elif content_type == 'text/html' and 'attachment' not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        import html
                        charset = part.get_content_charset() or 'utf-8'
                        text = payload.decode(charset, errors='replace')
                        # Nettoyer le HTML basique
                        text = re.sub(r'<[^>]+>', ' ', text)
                        text = html.unescape(text)
                        text = re.sub(r'\s+', ' ', text).strip()
                        return text
                except:
                    pass
    else:
        try:
            payload = email_msg.get_payload(decode=True)
            if payload:
                charset = email_msg.get_content_charset() or 'utf-8'
                return payload.decode(charset, errors='replace')
        except:
            pass
    return "[corps non lisible]"

# ─── TEST D'UN PORTFOLIO ────────────────────────────────────────────────────

def test_portfolio(numero):
    """
    Test complet d'un portfolio :
    1. Chaque boîte envoie un mail au strateur
    2. Le strateur répond à toutes
    3. Vérification IMAP de la réponse
    """
    prenom = PRENOMS[numero]
    prenom_clean = _get_prenom_clean(prenom)
    strateur_email = f"{prenom_clean.lower()}.{SUFFIXE_STRATEUR}@{DOMAIN}"
    strateur_pw = _get_password(prenom_clean, SUFFIXE_STRATEUR)
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"\n{'='*60}")
    print(f"  Portfolio #{numero} — {prenom}")
    print(f"  Strateur: {strateur_email}")
    print(f"  Début: {timestamp}")
    print(f"{'='*60}")
    
    results = {'ok': 0, 'echec': 0, 'details': []}
    
    # ── ÉTAPE 1 : Chaque boîte envoie au strateur ──
    print(f"\n  📤 Envoi des mails au strateur...")
    messages_envoyes = []
    
    for suffixe in SUFFIXES_PUBLICATION:
        email = f"{prenom_clean.lower()}.{suffixe}@{DOMAIN}"
        pw = _get_password(prenom_clean)
        
        sujet = f"Test {prenom}.{suffixe} — {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        body = f"Bonjour {prenom},\n\nCeci est un test de la boîte {email}.\nPortfolio #{numero} — {prenom} — suffixe {suffixe}.\n\nTest émission/réception — {datetime.now().isoformat()}"
        
        start = time.time()
        try:
            msg_id, duree = _send_email(email, pw, strateur_email, sujet, body)
            messages_envoyes.append({'email': email, 'suffixe': suffixe, 'msg_id': msg_id, 'sujet': sujet})
            _log_result(email, numero, prenom, suffixe, 'envoi', 'ok', message_id=msg_id, sujet=sujet, duree_ms=duree)
            print(f"    ✅ {prenom}.{suffixe} → strateur ({duree}ms)")
            time.sleep(PAUSE_LOT)
        except Exception as e:
            _log_result(email, numero, prenom, suffixe, 'envoi', 'echec', erreur=str(e))
            print(f"    ❌ {prenom}.{suffixe} → strateur : {str(e)[:80]}")
    
    if not messages_envoyes:
        print(f"  ⚠️ Aucun message envoyé pour {prenom}, on passe")
        return results
    
    print(f"    → {len(messages_envoyes)} messages envoyés")
    time.sleep(PAUSE_LOT * 2)  # Attendre que Postfix traite
    
    # ── ÉTAPE 2 : Vérifier que le strateur a bien reçu les messages ──
    print(f"\n  📥 Vérification réception par le strateur...")
    
    try:
        mails_recus = _check_imap(strateur_email, strateur_pw, max_attempts=5, delay=5)
        
        # Filtrer les mails de test (ceux qu'on vient d'envoyer)
        mails_test = []
        for sent in messages_envoyes:
            found = [m for m in mails_recus if sent['suffixe'] in m.get('subject', '')]
            if found:
                mails_test.append({**sent, 'recu': True, 'reponse': found})
                _log_result(sent['email'], numero, prenom, sent['suffixe'], 'reception', 'ok')
                results['ok'] += 1
                results['details'].append({'email': sent['email'], 'etape': 'reception', 'ok': True})
            else:
                mails_test.append({**sent, 'recu': False, 'reponse': []})
                _log_result(sent['email'], numero, prenom, sent['suffixe'], 'reception', 'echec', erreur='Message non trouvé dans INBOX')
                results['echec'] += 1
                results['details'].append({'email': sent['email'], 'etape': 'reception', 'ok': False, 'erreur': 'Non reçu'})
                print(f"    ❌ {sent['suffixe']} → strateur: NON REÇU")
        
        reçus = sum(1 for m in mails_test if m['recu'])
        print(f"    → {reçus}/{len(messages_envoyes)} messages reçus par le strateur")
        
    except Exception as e:
        print(f"    ❌ Impossible de lire les mails du strateur : {e}")
        results['echec'] += len(messages_envoyes)
        _log_signalement('error', 'test_mail', f"Échec IMAP strateur {strateur_email}", str(e))
        return results
    
    # ── ÉTAPE 3 : Le strateur répond à chaque boîte ──
    print(f"\n  📤 Le strateur répond à toutes les boîtes...")
    
    for sent in mails_test:
        if not sent['recu']:
            continue
        
        email_dest = sent['email']
        suffixe = sent['suffixe']
        sujet_reponse = f"RE: {sent['sujet']}"
        body_reponse = f"Bonjour {prenom}.{suffixe},\n\nJ'ai bien reçu ton message de test. Tout fonctionne.\n\nRéponse automatique — {datetime.now().isoformat()}"
        
        try:
            msg_id, duree = _send_email(strateur_email, strateur_pw, email_dest, sujet_reponse, body_reponse)
            _log_result(email_dest, numero, prenom, suffixe, 'reponse_strateur', 'ok', message_id=msg_id, duree_ms=duree)
            print(f"    ✅ strateur → {prenom}.{suffixe} ({duree}ms)")
            time.sleep(PAUSE_LOT)
        except Exception as e:
            _log_result(email_dest, numero, prenom, suffixe, 'reponse_strateur', 'echec', erreur=str(e))
            print(f"    ❌ strateur → {prenom}.{suffixe} : {str(e)[:80]}")
    
    time.sleep(PAUSE_LOT * 2)  # Laisser Postfix livrer
    
    # ── ÉTAPE 4 : Vérifier que chaque boîte a reçu la réponse ──
    print(f"\n  📥 Vérification des réponses par les boîtes...")
    
    for sent in mails_test:
        if not sent['recu']:
            continue
        
        email_dest = sent['email']
        pw = _get_password(prenom_clean)
        
        try:
            mails = _check_imap(email_dest, pw, max_attempts=3, delay=3)
            
            # Chercher la réponse du strateur
            reponse_trouvee = False
            contenu_trouve = None
            for m in mails:
                if 'RE:' in m.get('subject', '') and strateur_email.lower() in m.get('from', '').lower():
                    reponse_trouvee = True
                    contenu_trouve = m.get('body', '')[:200]
                    break
            
            if reponse_trouvee:
                _log_result(email_dest, numero, prenom, sent['suffixe'], 'verification_finale', 'ok', 
                          sujet=f"Réponse trouvée", duree_ms=0)
                results['ok'] += 1
                print(f"    ✅ {prenom}.{sent['suffixe']} → Réponse lue !")
                
                # Enregistrer la preuve de lecture
                conn = _get_db()
                conn.execute("""
                    UPDATE test_mail SET statut='ok', erreur=?
                    WHERE email=? AND etape='verification_finale'
                """, (f"Contenu: {contenu_trouve}", email_dest))
                conn.commit()
                conn.close()
            else:
                _log_result(email_dest, numero, prenom, sent['suffixe'], 'verification_finale', 'echec',
                          erreur='Réponse du strateur non trouvée dans INBOX')
                results['echec'] += 1
                results['details'].append({'email': email_dest, 'etape': 'verification', 'ok': False})
                print(f"    ❌ {prenom}.{sent['suffixe']} → Réponse NON trouvée")
                
        except Exception as e:
            _log_result(email_dest, numero, prenom, sent['suffixe'], 'verification_finale', 'echec', erreur=str(e)[:200])
            results['echec'] += 1
            print(f"    ❌ {prenom}.{sent['suffixe']} → Erreur IMAP : {str(e)[:60]}")
    
    return results

# ─── RAPPORT ─────────────────────────────────────────────────────────────────

def _generer_rapport():
    """Génère un rapport complet depuis la table test_mail."""
    conn = _get_db()
    
    print(f"\n{'='*60}")
    print(f"  📊 RAPPORT TEST MAIL — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*60}")
    
    cur = conn.execute("""
        SELECT portfolio_num, prenom,
               SUM(CASE WHEN statut='ok' THEN 1 ELSE 0 END) as ok,
               SUM(CASE WHEN statut='echec' THEN 1 ELSE 0 END) as echec,
               SUM(CASE WHEN statut='en_attente' THEN 1 ELSE 0 END) as attente,
               COUNT(*) as total
        FROM test_mail
        WHERE etape = 'verification_finale'
        GROUP BY portfolio_num
        ORDER BY portfolio_num
    """)
    
    total_ok = 0
    total_echec = 0
    total_attente = 0
    
    for row in cur.fetchall():
        total_ok += row['ok']
        total_echec += row['echec']
        total_attente += row['attente']
        taux = (row['ok'] / row['total'] * 100) if row['total'] > 0 else 0
        barre = '█' * int(taux / 10) + '░' * (10 - int(taux / 10))
        print(f"  #{row['portfolio_num']:2d} {row['prenom']:10s} | {barre} {taux:5.1f}% | {row['ok']:2d}/{row['total']:2d}")
    
    total = total_ok + total_echec + total_attente
    if total > 0:
        taux_global = total_ok / total * 100
        print(f"\n  {'─'*60}")
        print(f"  TOTAL: {total_ok}/{total} OK ({taux_global:.1f}%) | {total_echec} échecs | {total_attente} en attente")
    
    # Rapport détaillé des échecs
    cur.execute("""
        SELECT email, portfolio_num, prenom, suffixe, erreur
        FROM test_mail
        WHERE statut='echec'
        ORDER BY portfolio_num
    """)
    echecs = cur.fetchall()
    if echecs:
        print(f"\n  ❌ Détail des échecs ({len(echecs)}) :")
        for e in echecs:
            print(f"    #{e['portfolio_num']} {e['prenom']}.{e['suffixe']} <{e['email']}>")
            if e['erreur']:
                print(f"      → {e['erreur'][:120]}")
    
    conn.close()
    return {'ok': total_ok, 'echec': total_echec, 'attente': total_attente}

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test massif des boîtes mail')
    parser.add_argument('--lot', type=str, help='Tester un seul portfolio (A-Z ou 1-26)')
    parser.add_argument('--status', action='store_true', help='Afficher le rapport')
    parser.add_argument('--clean', action='store_true', help='Nettoyer les logs de test')
    parser.add_argument('--debut', type=int, help='Démarrer à partir du portfolio N')
    parser.add_argument('--fin', type=int, help='Finir au portfolio N')
    
    args = parser.parse_args()
    
    _init_tracking()
    
    if args.status:
        _generer_rapport()
        return
    
    if args.clean:
        conn = _get_db()
        conn.execute("DROP TABLE IF EXISTS test_mail")
        conn.commit()
        conn.close()
        print("✅ Table test_mail nettoyée")
        return
    
    if args.lot:
        # Tester un seul portfolio
        if args.lot.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            lettre = args.lot.upper()
            numero = {PRENOMS[i][0] if isinstance(PRENOMS[i], tuple) else 'A': i for i in PRENOMS}
            # On cherche par prénom
            for num, prenom in PRENOMS.items():
                if prenom[0].upper() == lettre:
                    numero = num
                    break
        else:
            numero = int(args.lot)
        
        test_portfolio(numero)
        _generer_rapport()
        return
    
    # Test complet
    debut = args.debut or 1
    fin = min(args.fin or 26, 26)
    
    print(f"🚀 TEST MAIL MASSIF — Portfolios {debut} à {fin}")
    print(f"   {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    resultats_globaux = {'ok': 0, 'echec': 0, 'attente': 0}
    
    for num in range(debut, fin + 1):
        print(f"\n{'#'*60}")
        print(f"  PORTFOLIO #{num} / {fin} — {PRENOMS[num]}")
        print(f"{'#'*60}")
        
        try:
            r = test_portfolio(num)
            resultats_globaux['ok'] += r.get('ok', 0)
            resultats_globaux['echec'] += r.get('echec', 0)
            resultats_globaux['attente'] += r.get('attente', 0)
        except Exception as e:
            print(f"  🔴 Erreur critique portfolio {num}: {e}")
            _log_signalement('critical', 'test_mail', f"Erreur portfolio #{num}", str(e))
        
        # Pause entre portfolios
        if num < fin:
            print(f"\n  ⏳ Pause {PAUSE_PORTFOLIO}s avant le prochain portfolio...")
            time.sleep(PAUSE_PORTFOLIO)
    
    # Rapport final
    print(f"\n{'='*60}")
    print(f"  🏁 TEST TERMINÉ !")
    print(f"{'='*60}")
    
    total = resultats_globaux['ok'] + resultats_globaux['echec']
    if total > 0:
        taux = resultats_globaux['ok'] / total * 100
        print(f"  ✅ {resultats_globaux['ok']} OK")
        print(f"  ❌ {resultats_globaux['echec']} échecs")
        print(f"  📊 Taux de succès: {taux:.1f}%")
    
    _generer_rapport()
    _log_signalement('info', 'test_mail', f"Test terminé: {resultats_globaux['ok']} OK, {resultats_globaux['echec']} échecs")

if __name__ == "__main__":
    main()
