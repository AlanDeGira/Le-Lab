#!/usr/bin/env python3
"""
otp_watcher.py — Surveillance OTP pour l'Agent Mail.
Utilisé par agent.py. Ne pas exécuter directement.

Lit le fichier /tmp/agent_mail_watch.json pour configuration :
{
  "email": "prenom.strateur@automatisations.org",
  "timeout": 120,
  "expediteur": "facebook"  // optionnel, filtre par expéditeur
}

Écrit le résultat dans /tmp/agent_mail_otp.json.
"""

import json, ssl, imaplib, email as eml_lib, re, time, sys
from datetime import datetime
from email.header import decode_header

WATCH_FILE = "/tmp/agent_mail_watch.json"
RESULT_FILE = "/tmp/agent_mail_otp.json"

def decode(v):
    if not v: return ''
    parts = decode_header(v)
    r = []
    for p, cs in parts:
        if isinstance(p, bytes):
            try: r.append(p.decode(cs or 'utf-8', errors='replace'))
            except: r.append(p.decode('utf-8', errors='replace'))
        else: r.append(str(p))
    return ''.join(r)

PRENOMS = {
    'adam': 'Adam', 'baptiste': 'Baptiste', 'camille': 'Camille',
    'diane': 'Diane', 'emile': 'Émile', 'flora': 'Flora',
    'gabriel': 'Gabriel', 'hugo': 'Hugo', 'iris': 'Iris',
    'jules': 'Jules', 'karine': 'Karine', 'leo': 'Léo',
    'manon': 'Manon', 'nathan': 'Nathan', 'oscar': 'Oscar',
    'paul': 'Paul', 'quentin': 'Quentin', 'romane': 'Romane',
    'sacha': 'Sacha', 'theo': 'Théo', 'ulysse': 'Ulysse',
    'valentin': 'Valentin', 'william': 'William', 'xander': 'Xander',
    'yasmine': 'Yasmine', 'zoe': 'Zoé',
}

def get_password(email):
    local = email.split('@')[0]
    prenom_base = local.split('.')[0]
    prenom = PRENOMS.get(prenom_base, prenom_base.capitalize())
    suffixe = '.'.join(local.split('.')[1:])
    is_strateur = suffixe == 'strateur'
    accents = str.maketrans({'É': 'E', 'é': 'e', 'È': 'E', 'è': 'e'})
    clean = prenom.translate(accents)
    return f"{clean}.admin1!" if is_strateur else f"{clean}1!"

def find_otp(email, timeout=120, expediteur=None):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    pw = get_password(email)
    expire, interval = time.time() + timeout, 10

    while time.time() < expire:
        try:
            m = imaplib.IMAP4_SSL("127.0.0.1", 993, ssl_context=ctx, timeout=10)
            m.login(email, pw)
            m.select('INBOX')
            st, data = m.search(None, 'ALL')
            if st == 'OK' and data[0]:
                ids = data[0].split()
                # Lire les 3 derniers messages
                for mid in ids[-3:]:
                    st2, d2 = m.fetch(mid, '(RFC822)')
                    if st2 != 'OK': continue
                    m.store(mid, '+FLAGS', '\\Seen')

                    for part in d2:
                        if isinstance(part, tuple) and len(part) >= 2 and isinstance(part[1], bytes):
                            msg = eml_lib.message_from_bytes(part[1])
                            subject = decode(msg['Subject'] or '')
                            from_addr = decode(msg['From'] or '')

                            if expediteur and expediteur.lower() not in from_addr.lower():
                                continue

                            body = ""
                            if msg.is_multipart():
                                for p in msg.walk():
                                    if p.get_content_type() == 'text/plain':
                                        try: body = p.get_payload(decode=True).decode('utf-8', errors='replace')
                                        except: pass
                            else:
                                try: body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
                                except: pass

                            # OTP = 5-8 chiffres
                            codes = re.findall(r'\b(\d{5,8})\b', body + ' ' + subject)
                            if codes:
                                result = {
                                    'email': email, 'otp': codes[0], 'tous_les_codes': codes,
                                    'from': from_addr, 'subject': subject,
                                    'body_preview': body[:300],
                                    'trouve': True, 'timestamp': datetime.now().isoformat()
                                }
                                with open(RESULT_FILE, 'w') as f:
                                    json.dump(result, f, indent=2)
                                print(json.dumps(result))
                                m.logout()
                                return True

                            # Pas d'OTP mais un nouveau message
                            if msg['Message-ID']:
                                meta = {
                                    'email': email, 'otp': None, 'trouve': False,
                                    'from': from_addr, 'subject': subject,
                                    'message_id': msg['Message-ID'],
                                    'body_preview': body[:200],
                                    'timestamp': datetime.now().isoformat()
                                }
                                with open(RESULT_FILE, 'w') as f:
                                    json.dump(meta, f, indent=2)
            m.logout()
        except Exception as e:
            pass
        time.sleep(interval)

    # Timeout
    result = {'email': email, 'otp': None, 'trouve': False, 'error': 'timeout',
              'timestamp': datetime.now().isoformat()}
    with open(RESULT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result))
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--from-file":
        with open(WATCH_FILE) as f:
            cfg = json.load(f)
        find_otp(cfg.get('email', ''), cfg.get('timeout', 120), cfg.get('expediteur'))
    else:
        find_otp(sys.argv[1] if len(sys.argv) > 1 else 'otp@automatisations.org',
                 int(sys.argv[2]) if len(sys.argv) > 2 else 120)
