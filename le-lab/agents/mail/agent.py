#!/usr/bin/env python3
"""
agent.py — Runner principal de l'Agent Mail.
Point d'entrée unique. Le seul fichier qui doit être exécuté.

Usage interne (fichier de commande) :
  Écrire une commande dans /tmp/agent_mail_cmd.json pour piloter l'agent :
  
  {"action": "test_all"}       → Tester tous les portfolios restants
  {"action": "test_one", "portfolio": "A"} → Tester un seul portfolio
  {"action": "status"}         → Afficher le rapport
  {"action": "resume"}         → Reprendre là où on s'est arrêté
  {"action": "watch", "email": "prenom.strateur@automatisations.org", "timeout": 120} → Surveiller OTP

  L'agent lit ce fichier toutes les 30s et exécute la commande.

Appel direct (pour debug) :
  python3 agent.py test_all
  python3 agent.py resume
  python3 agent.py status
  python3 agent.py watch prenom.strateur@automatisations.org --timeout 120
"""

import sys, os, json, time, subprocess, threading
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).parent
CMD_FILE = "/tmp/agent_mail_cmd.json"
LOG_FILE = AGENT_DIR / "agent.log"
PID_FILE = AGENT_DIR / "agent.pid"
WATCHER_FILE = AGENT_DIR / "watcher.json"

def log(msg, level="info"):
    ts = datetime.now().strftime("%d/%m %H:%M:%S")
    line = f"[{ts}] [{level.upper()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def exec_script(script, args):
    """Lance un script Python et retourne le résultat."""
    script_path = AGENT_DIR / script
    cmd = [sys.executable, "-u", str(script_path)] + args
    log(f"Exécution: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        log(result.stderr[-500:], "error")
    if result.returncode != 0:
        log(f"Échec (code {result.returncode})", "error")
    return result.returncode == 0

def cmd_test_all():
    exec_script("test_mail.py", [])

def cmd_test_one(portfolio):
    exec_script("test_mail.py", ["--portfolio", str(portfolio)])

def cmd_resume():
    exec_script("test_mail.py", ["--resume"])

def cmd_status():
    exec_script("test_mail.py", ["--status"])

def cmd_clean():
    exec_script("test_mail.py", ["--clean"])

def cmd_watch(email, timeout=120):
    """Surveille une boîte mail pour un OTP."""
    log(f"Surveillance OTP: {email} (timeout {timeout}s)")
    start = time.time()
    interval = 10
    ctx = None
    while time.time() - start < timeout:
        try:
            import ssl, imaplib, email as eml_lib
            from email.header import decode_header

            if not ctx:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

            # Extraire le prénom et suffixe de l'email
            local = email.split('@')[0]
            # Trouver le prénom correspondant
            prenoms = {
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
            prenom_base = local.split('.')[0]
            prenom = prenoms.get(prenom_base, prenom_base.capitalize())
            suffixe = '.'.join(local.split('.')[1:]) if '.' in local else ''
            is_strateur = suffixe == 'strateur'
            pw = f"{prenom}.admin1!" if is_strateur else f"{prenom}1!"

            m = imaplib.IMAP4_SSL("127.0.0.1", 993, ssl_context=ctx, timeout=10)
            m.login(email, pw)
            m.select('INBOX')
            st, data = m.search(None, 'ALL')
            if st == 'OK':
                ids = data[0].split() if data[0] else []
                if ids:
                    # Chercher le dernier message
                    st2, d2 = m.fetch(ids[-1], '(RFC822)')
                    m.store(ids[-1], '+FLAGS', '\\Seen')  # Marquer comme lu
                    m.logout()

                    if st2 == 'OK':
                        for part in d2:
                            if isinstance(part, tuple) and len(part) >= 2 and isinstance(part[1], bytes):
                                msg = eml_lib.message_from_bytes(part[1])
                                subject = msg['Subject'] or ''
                                from_addr = msg['From'] or ''

                                # Extraire le corps
                                body = ""
                                if msg.is_multipart():
                                    for p in msg.walk():
                                        if p.get_content_type() == 'text/plain':
                                            try:
                                                body = p.get_payload(decode=True).decode('utf-8', errors='replace')
                                            except: pass
                                else:
                                    try:
                                        body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
                                    except: pass

                                # Chercher un OTP (code à 5-8 chiffres)
                                otp_match = re.search(r'\b(\d{5,8})\b', body)
                                otp = otp_match.group(1) if otp_match else None
                                otp_in_subject = re.search(r'\b(\d{5,8})\b', subject)
                                otp_subj = otp_in_subject.group(1) if otp_in_subject else None

                                result = {
                                    'email': email,
                                    'trouve': bool(otp or otp_subj),
                                    'otp': otp or otp_subj,
                                    'from': from_addr,
                                    'subject': subject,
                                    'body_preview': body[:200],
                                    'timestamp': datetime.now().isoformat(),
                                }
                                # Écrire le résultat
                                with open(WATCHER_FILE, 'w') as f:
                                    json.dump(result, f, indent=2)
                                
                                if result['trouve']:
                                    log(f"✅ OTP trouvé pour {email}: {result['otp']} (de: {from_addr})")
                                    return result
                                else:
                                    log(f"📩 Message trouvé mais pas d'OTP (sujet: {subject[:60]})")
                m.logout()
        except Exception as e:
            log(f"Erreur check {email}: {e}", "error")

        time.sleep(interval)

    log(f"⏰ Timeout {timeout}s pour {email} — OTP non reçu", "warning")
    result = {'email': email, 'trouve': False, 'otp': None, 'error': 'timeout', 'timestamp': datetime.now().isoformat()}
    with open(WATCHER_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    return result

def main():
    import argparse
    import re

    parser = argparse.ArgumentParser(description='Agent Mail — Runner principal')
    parser.add_argument('action', nargs='?', help='test_all | test_one | resume | status | clean | watch')
    parser.add_argument('--portfolio', '-p', help='Portfolio pour test_one')
    parser.add_argument('--email', '-e', help='Email pour watch')
    parser.add_argument('--timeout', '-t', type=int, default=120, help='Timeout watch en secondes')
    parser.add_argument('--daemon', action='store_true', help='Mode daemon: écoute les commandes')
    args = parser.parse_args()

    if args.daemon:
        log("Agent Mail démarré en mode daemon", "info")
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
        while True:
            if os.path.exists(CMD_FILE):
                try:
                    with open(CMD_FILE) as f:
                        cmd = json.load(f)
                    os.remove(CMD_FILE)
                    action = cmd.get('action')
                    log(f"Commande reçue: {action}")
                    if action == 'test_all':
                        cmd_test_all()
                    elif action == 'test_one':
                        cmd_test_one(cmd.get('portfolio', 'A'))
                    elif action == 'resume':
                        cmd_resume()
                    elif action == 'status':
                        cmd_status()
                    elif action == 'clean':
                        cmd_clean()
                    elif action == 'watch':
                        cmd_watch(cmd.get('email', ''), cmd.get('timeout', 120))
                    else:
                        log(f"Action inconnue: {action}", "warning")
                except Exception as e:
                    log(f"Erreur commande: {e}", "error")
            time.sleep(30)
        return

    if not args.action:
        parser.print_help()
        return

    if args.action == 'test_all':
        cmd_test_all()
    elif args.action == 'test_one':
        cmd_test_one(args.portfolio)
    elif args.action == 'resume':
        cmd_resume()
    elif args.action == 'status':
        cmd_status()
    elif args.action == 'clean':
        cmd_clean()
    elif args.action == 'watch':
        cmd_watch(args.email, args.timeout)
    else:
        log(f"Action inconnue: {args.action}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
