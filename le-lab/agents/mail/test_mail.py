#!/usr/bin/env python3
"""
test_mail.py — Agent Mail : Test autonome émission/réception des boîtes.
Par portfolio, en interne (pas de Gmail).

Usage :
  python3 test_mail.py                     # Test complet (26 portfolios)
  python3 test_mail.py --portfolio 1       # Test un seul portfolio
  python3 test_mail.py --portfolio A       # Par lettre
  python3 test_mail.py --status            # Rapport d'avancement
  python3 test_mail.py --resume            # Reprendre là où on s'est arrêté
  python3 test_mail.py --clean             # Reset la table de suivi
"""

import smtplib, imaplib, ssl, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import sqlite3, json, os, sys, time, uuid, re, subprocess
from datetime import datetime, timedelta
from pathlib import Path

# ─── CONFIG ─────────────────────────────────────────────────────────────────

SMTP_HOST = "127.0.0.1"
SMTP_PORT = 587
IMAP_HOST = "127.0.0.1"
IMAP_PORT = 993
DOMAIN = "automatisations.org"
TIMEOUT = 30

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "le-lab.db"

PAUSE_ENVOI = 3
PAUSE_PORTFOLIO = 10
ATTENTE_LIVRAISON = 6

PRENOMS = {
    1: 'Adam', 2: 'Baptiste', 3: 'Camille', 4: 'Diane', 5: 'Émile',
    6: 'Flora', 7: 'Gabriel', 8: 'Hugo', 9: 'Iris', 10: 'Jules',
    11: 'Karine', 12: 'Léo', 13: 'Manon', 14: 'Nathan', 15: 'Oscar',
    16: 'Paul', 17: 'Quentin', 18: 'Romane', 19: 'Sacha', 20: 'Théo',
    21: 'Ulysse', 22: 'Valentin', 23: 'William', 24: 'Xander',
    25: 'Yasmine', 26: 'Zoé',
}

SUFFIXES = ['app', 'web', 'fr', 'hub', 'labs', 'studio',
            'media', 'news', 'ideaz', 'idies', 'biz']
STRATEUR = 'strateur'

# ─── ACCENTS → mot de passe ──────────────────────────────────────────────────

ACCENTS = str.maketrans({
    'É': 'E', 'é': 'e', 'È': 'E', 'è': 'e', 'Ê': 'E', 'ê': 'e',
    'À': 'A', 'à': 'a', 'Ù': 'U', 'ù': 'u',
})

def _mdp(prenom, suffixe=None):
    clean = prenom.translate(ACCENTS)
    return f"{clean}.admin1!" if suffixe == STRATEUR else f"{clean}1!"

# ─── BDD ────────────────────────────────────────────────────────────────────

def _db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def _init():
    conn = _db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS test_mail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            portfolio_num INTEGER, prenom TEXT, suffixe TEXT,
            etape TEXT, message_id TEXT, sujet TEXT,
            statut TEXT DEFAULT 'en_attente',
            erreur TEXT, duree_ms INTEGER,
            date_test TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Supprimer les logs du script jetable
    conn.execute("DELETE FROM test_mail WHERE etape = 'envoi'")
    conn.commit()
    conn.close()

def _log(email, num, prenom, suffixe, etape, statut='ok', erreur=None, msg_id=None, sujet=None, duree=None):
    conn = _db()
    conn.execute("""INSERT INTO test_mail
        (email, portfolio_num, prenom, suffixe, etape, message_id, sujet, statut, erreur, duree_ms)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (email, num, prenom, suffixe, etape, msg_id, sujet, statut, erreur, duree))
    conn.commit()
    conn.close()

def _log_system(niveau, message, details=None):
    conn = _db()
    conn.execute("INSERT INTO logs (niveau, source, message, details) VALUES (?, 'agent_mail', ?, ?)",
                 (niveau, message, json.dumps(details) if details else None))
    conn.commit()
    conn.close()

def _progress():
    """Retourne le dernier portfolio testé avec succès."""
    conn = _db()
    cur = conn.execute("""
        SELECT portfolio_num FROM test_mail
        WHERE etape = 'verification_finale' AND statut = 'ok'
        ORDER BY portfolio_num DESC LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()
    return row['portfolio_num'] if row else 0

# ─── SMTP ───────────────────────────────────────────────────────────────────

def _smtp(from_email, password, to_email, subject, body):
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Message-ID'] = f"<{uuid.uuid4().hex}@automatisations.org>"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    deb = time.time()
    s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=TIMEOUT)
    s.ehlo()
    s.starttls(context=ctx)
    s.ehlo()
    s.login(from_email, password)
    s.sendmail(from_email, [to_email], msg.as_string())
    s.quit()
    return msg['Message-ID'], int((time.time() - deb) * 1000)

# ─── IMAP ───────────────────────────────────────────────────────────────────

def _imap_lire(mailbox, password, max_try=5, delay=5):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for t in range(max_try):
        try:
            m = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx, timeout=TIMEOUT)
            m.login(mailbox, password)
            m.select('INBOX')
            st, data = m.search(None, 'ALL')
            if st != 'OK':
                m.logout()
                if t < max_try - 1: time.sleep(delay)
                continue

            ids = data[0].split() if data[0] else []
            msgs = []
            for mid in ids:
                st2, d2 = m.fetch(mid, '(RFC822)')
                if st2 != 'OK': continue
                for part in d2:
                    if isinstance(part, tuple) and len(part) >= 2 and isinstance(part[1], bytes):
                        em = email.message_from_bytes(part[1])
                        subj = _decode(em['Subject'])
                        msgs.append({'subject': subj, 'from': em['From'] or '',
                                     'date': em['Date'] or '', 'msg_id': em['Message-ID'] or '',
                                     'body': _corps(em)[:400]})
            m.logout()
            if msgs or t >= max_try - 1:
                return msgs
            time.sleep(delay)
        except Exception as e:
            if t >= max_try - 1: raise
            time.sleep(delay)
    return []

def _decode(v):
    if not v: return ''
    parts = decode_header(v)
    r = []
    for p, cs in parts:
        if isinstance(p, bytes):
            try: r.append(p.decode(cs or 'utf-8', errors='replace'))
            except: r.append(p.decode('utf-8', errors='replace'))
        else: r.append(str(p))
    return ''.join(r)

def _corps(em):
    if em.is_multipart():
        for p in em.walk():
            ct = p.get_content_type()
            if ct == 'text/plain' and 'attachment' not in str(p.get('Content-Disposition', '')):
                try:
                    d = p.get_payload(decode=True)
                    if d: return d.decode(p.get_content_charset() or 'utf-8', errors='replace')
                except: pass
    else:
        try:
            d = em.get_payload(decode=True)
            if d: return d.decode(em.get_content_charset() or 'utf-8', errors='replace')
        except: pass
    return '[corps non lisible]'

# ─── TEST D'UN PORTFOLIO ───────────────────────────────────────────────────

def test_portfolio(num):
    prenom = PRENOMS[num]
    clean = prenom.translate(ACCENTS)
    strateur = f"{clean.lower()}.{STRATEUR}@{DOMAIN}"
    pw_strateur = _mdp(prenom, STRATEUR)

    ts = datetime.now().strftime('%H:%M:%S')
    print(f"\n  {'='*50}")
    print(f"  #{num} {prenom} | strateur: {strateur} | {ts}")
    print(f"  {'='*50}")

    ok, echec = 0, 0

    # ── 1. Chaque boîte envoie au strateur ──
    envoyes = []
    for s in SUFFIXES:
        email = f"{clean.lower()}.{s}@{DOMAIN}"
        pw = _mdp(prenom)
        sujet = f"Test {prenom}.{s} — {datetime.now().strftime('%d/%m %H:%M')}"
        body = f"Bonjour {prenom},\nCeci est un test de {email}.\nPortfolio #{num}.\n{datetime.now().isoformat()}"

        try:
            mid, d = _smtp(email, pw, strateur, sujet, body)
            envoyes.append({'email': email, 'suffixe': s, 'msg_id': mid, 'sujet': sujet})
            print(f"    ✓ {s} → strateur ({d}ms)")
        except Exception as e:
            _log(email, num, prenom, s, 'envoi', 'echec', str(e)[:200])
            print(f"    ✗ {s} → strateur: {str(e)[:60]}")
        time.sleep(PAUSE_ENVOI)

    if not envoyes:
        print(f"    ⚠ Aucun envoi réussi")
        return 0, len(SUFFIXES)

    print(f"    → {len(envoyes)} envoyés")
    time.sleep(ATTENTE_LIVRAISON)

    # ── 2. Vérifier que le strateur a reçu ──
    try:
        recus = _imap_lire(strateur, pw_strateur)
        bien_recus = []
        for e in envoyes:
            trouve = any(e['suffixe'] in m.get('subject', '') for m in recus)
            if trouve:
                bien_recus.append(e)
                _log(e['email'], num, prenom, e['suffixe'], 'reception', 'ok')
                ok += 1
            else:
                _log(e['email'], num, prenom, e['suffixe'], 'reception', 'echec', 'Non trouvé')
                echec += 1
                print(f"    ✗ {e['suffixe']} → NON REÇU par strateur")
        print(f"    → {len(bien_recus)}/{len(envoyes)} reçus")
    except Exception as e:
        print(f"    ✗ ERREUR IMAP strateur: {e}")
        _log_system('error', f"IMAP strateur #{num}", str(e))
        echec += len(envoyes)
        return ok, echec

    # ── 3. Strateur répond ──
    for e in bien_recus:
        sujet_reponse = f"RE: {e['sujet']}"
        body_reponse = f"Bonjour {prenom}.{e['suffixe']},\n\nRéponse automatique de test. OK.\n{datetime.now().isoformat()}"
        try:
            mid, d = _smtp(strateur, pw_strateur, e['email'], sujet_reponse, body_reponse)
            print(f"    ✓ strateur → {e['suffixe']} ({d}ms)")
        except Exception as ex:
            print(f"    ✗ strateur → {e['suffixe']}: {str(ex)[:60]}")
        time.sleep(PAUSE_ENVOI)

    time.sleep(ATTENTE_LIVRAISON)

    # ── 4. Vérifier les réponses ──
    for e in bien_recus:
        try:
            msgs = _imap_lire(e['email'], _mdp(prenom), max_try=3, delay=3)
            trouve = any('RE:' in m.get('subject', '') and strateur.lower() in m.get('from', '').lower() for m in msgs)
            if trouve:
                _log(e['email'], num, prenom, e['suffixe'], 'verification_finale', 'ok')
                ok += 1
                print(f"    ✓ {e['suffixe']} → réponse lue ✓")
            else:
                _log(e['email'], num, prenom, e['suffixe'], 'verification_finale', 'echec', 'Réponse strateur absente')
                echec += 1
                print(f"    ✗ {e['suffixe']} → réponse absente")
        except Exception as ex:
            _log(e['email'], num, prenom, e['suffixe'], 'verification_finale', 'echec', str(ex)[:200])
            echec += 1
            print(f"    ✗ {e['suffixe']} → IMAP err: {str(ex)[:60]}")

    return ok, echec

# ─── RAPPORT ────────────────────────────────────────────────────────────────

def rapport():
    conn = _db()
    cur = conn.execute("""
        SELECT portfolio_num, prenom,
            SUM(CASE WHEN statut='ok' THEN 1 ELSE 0 END) as ok,
            SUM(CASE WHEN statut='echec' THEN 1 ELSE 0 END) as echec,
            COUNT(*) as total
        FROM test_mail WHERE etape='verification_finale'
        GROUP BY portfolio_num ORDER BY portfolio_num
    """)
    total_ok = total_echec = 0
    for r in cur.fetchall():
        taux = (r['ok'] / r['total'] * 100) if r['total'] else 0
        barre = '█' * int(taux / 10) + '░' * (10 - int(taux / 10))
        total_ok += r['ok']; total_echec += r['echec']
        print(f"  #{r['portfolio_num']:2d} {r['prenom']:10s} | {barre} {taux:5.1f}% | {r['ok']:2d}/{r['total']:2d}")

    if total := total_ok + total_echec:
        print(f"  {'─'*55}")
        print(f"  TOTAL: {total_ok}/{total} OK ({total_ok/total*100:.1f}%) | {total_echec} échecs")

    cur2 = conn.execute("""
        SELECT email, portfolio_num, prenom, suffixe, erreur FROM test_mail
        WHERE statut='echec' ORDER BY portfolio_num
    """)
    echecs = cur2.fetchall()
    if echecs:
        print(f"\n  ✗ Échecs ({len(echecs)}) :")
        for e in echecs:
            print(f"    #{e['portfolio_num']} {e['prenom']}.{e['suffixe']} → {str(e['erreur'] or '')[:100]}")
    conn.close()

# ─── MAIN ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--portfolio', '-p', help='Portfolio (1-26 ou A-Z)')
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--resume', action='store_true')
    ap.add_argument('--clean', action='store_true')
    args = ap.parse_args()

    _init()

    if args.status:
        rapport(); sys.exit(0)

    if args.clean:
        conn = _db()
        conn.execute("DROP TABLE IF EXISTS test_mail")
        conn.commit(); conn.close()
        print("✓ Table test_mail vidée"); sys.exit(0)

    # Test un portfolio
    if args.portfolio:
        p = args.portfolio.upper()
        if p.isdigit():
            n = int(p)
        else:
            lettres = {PRENOMS[i][0].upper() if isinstance(PRENOMS[i], tuple) else PRENOMS[i][0]: i for i in PRENOMS}
            # mieux: mapping direct
            mapping = {PRENOMS[i][0].upper(): i for i in PRENOMS} if False else {}
            mapping = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,
                       'K':11,'L':12,'M':13,'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,
                       'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26}
            n = mapping.get(p)
            if not n:
                print(f"Portfolio '{p}' invalide. Utilise A-Z ou 1-26.")
                sys.exit(1)

        ok, echec = test_portfolio(n)
        print(f"\n  Résultat #{n}: {ok} OK, {echec} échecs")
        rapport()
        if echec > 0: sys.exit(1)
        sys.exit(0)

    # Test complet ou resume
    debut = _progress() + 1 if args.resume else 1
    fin = 26

    print(f"🚀 AGENT MAIL — Test émission/réception")
    print(f"   Portfolios {debut} à {fin} | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    total_ok = total_echec = 0

    for n in range(debut, fin + 1):
        print(f"\n{'#'*55}")
        print(f"  PORTFOLIO #{n}/{fin} — {PRENOMS[n]}")
        print(f"{'#'*55}")
        try:
            o, e = test_portfolio(n)
            total_ok += o; total_echec += e
        except Exception as ex:
            print(f"  🔴 CRITIQUE #{n}: {ex}")
            _log_system('critical', f"Portfolio #{n} crash", str(ex))
            total_echec += 11

        if n < fin:
            print(f"\n  ⏳ Pause {PAUSE_PORTFOLIO}s...")
            time.sleep(PAUSE_PORTFOLIO)

    print(f"\n{'='*55}")
    total = total_ok + total_echec
    print(f"  🏁 TERMINÉ ! {total_ok}/{total} OK ({total_ok/total*100:.1f}%)")
    print(f"{'='*55}")
    _log_system('info', f"Test terminé: {total_ok}/{total} OK")
    rapport()
