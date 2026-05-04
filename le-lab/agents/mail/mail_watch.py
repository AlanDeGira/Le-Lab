#!/usr/bin/env python3
"""
mail_watch.py — Watcher mail temps réel

Surveille les logs Postfix en temps réel (tail -F /var/log/syslog).
Dès qu'un mail arrive sur une boîte @automatisations.org :
1. Détection instantanée (to=<...@automatisations.org>)
2. Connexion IMAP à CETTE boîte uniquement
3. Lecture du dernier message non-lu
4. Extraction OTP si applicable
5. Rapport dans mail_watch_report.json

Usage :
  python3 mail_watch.py                        # Démon
  python3 mail_watch.py --status               # État
  python3 mail_watch.py --check-last 5         # Derniers événements
  python3 mail_watch.py --check-now            # Vérification immédiate

Pas de dépendances externes (stdlib uniquement).
"""

import imaplib
import ssl
import time
import json
import os
import re
import sys
import logging
import signal
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime, timezone

# ── Config ──────────────────────────────────────────────────────────────
IMAP_HOST = "mail.automatisations.org"
IMAP_PORT = 993

MAIL_DOMAIN = "automatisations.org"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../../data")

# ── Telegram ────────────────────────────────────────────────────────────
# NOTIFICATIONS_ENABLED = True envoie les OTP et mails importants sur Telegram
# Le token et chat_id sont lus depuis /root/.openclaw/telegram.env
TELEGRAM_ENABLED = True
TELEGRAM_CHAT_ID = "8695655337"
TELEGRAM_BOT_TOKEN = None  # chargé depuis le fichier env
TELEGRAM_ENV_PATH = "/root/.openclaw/telegram.env"

def _load_telegram_token():
    global TELEGRAM_BOT_TOKEN
    if TELEGRAM_BOT_TOKEN is not None:
        return TELEGRAM_BOT_TOKEN
    try:
        with open(TELEGRAM_ENV_PATH) as f:
            for line in f:
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    val = line.strip().split("=", 1)[1]
                    if '"' in val:
                        val = val.split('"')[1]
                    TELEGRAM_BOT_TOKEN = val
                    return val
    except Exception as e:
        logger.warning(f"Impossible de lire {TELEGRAM_ENV_PATH}: {e}")
    return None

def notify_telegram(message: str):
    """Envoie un message Telegram. Coût : 0 token, simple appel HTTP."""
    if not TELEGRAM_ENABLED:
        return
    token = _load_telegram_token()
    if not token:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }).encode()
    try:
        req = urllib.request.Request(url, data=data)
        resp = urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        logger.debug(f"notify_telegram: {e}")
REPORT_FILE = os.path.join(DATA_DIR, "mail_watch_report.json")
LOG_DIR = os.path.join(DATA_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "mail_watch.log")
STATE_FILE = os.path.join(DATA_DIR, "mail_watch_state.json")

# Délai minimum entre la détection log et le fetch IMAP (laisser Dovecot finir)
DELIVERY_GRACE_SEC = 3

# Répercuter les flags UNSEEN ? Si True, le watcher marque les messages comme lus
# Problème potentiel : si un humain checke la boîte après, le message sera déjà marqué lu
MARK_AS_SEEN = True

OTP_RE = re.compile(r'\b(\d{5,8})\b')

OTP_SENDERS = {
    "facebook":   ["facebookmail.com", "facebook.com", "fb.com"],
    "instagram":  ["instagram.com", "mail.instagram.com"],
    "google":     ["google.com", "accounts.google.com"],
    "twitter":    ["twitter.com", "x.com"],
    "tiktok":     ["tiktok.com", "mail.tiktok.com"],
    "linkedin":   ["linkedin.com"],
    "snapchat":   ["snapchat.com"],
    "amazon":     ["amazon.com", "amazon.fr", "amazon.de"],
    "whatsapp":   ["whatsapp.com"],
    "telegram":   ["telegram.org"],
}

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger("mail_watch")

KEEP_RUNNING = True

def handle_sigterm(signum, frame):
    global KEEP_RUNNING
    logger.info("Signal d'arrêt reçu.")
    KEEP_RUNNING = False

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


# ── Helpers ─────────────────────────────────────────────────────────────

def password_for(email: str) -> str | None:
    """Détermine le mot de passe SMTP/IMAP pour une adresse."""
    local = email.split("@")[0]
    parts = local.split(".")
    if len(parts) < 2:
        return None
    prenom = parts[0]
    suffix = parts[1]
    # Pattern: Prenom1! sauf pour les strateurs qui sont Prenom.admin1!
    if suffix == "strateur":
        return f"{prenom.capitalize()}.admin1!"
    else:
        return f"{prenom.capitalize()}1!"


def detect_service(sender_email: str) -> str | None:
    domain = sender_email.lower().split("@")[-1] if "@" in sender_email else sender_email.lower()
    for svc, domains in OTP_SENDERS.items():
        for d in domains:
            if d in domain or domain in d:
                return svc
    return None


def connect_imap(email: str, password: str):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    conn.login(email, password)
    return conn


def parse_last_email(email_addr: str, password: str) -> dict | None:
    """Se connecte à une boîte et analyse le dernier message non-lu."""
    conn = None
    try:
        conn = connect_imap(email_addr, password)
        typ, data = conn.select("INBOX")
        if typ != "OK":
            return None

        mark = False
        typ, data = conn.search(None, "UNSEEN")
        if typ == "OK" and data[0]:
            mark = MARK_AS_SEEN
            uids = data[0].split()[-1:]
        else:
            typ, data = conn.search(None, "ALL")
            if typ != "OK" or not data[0]:
                return None
            uids = data[0].split()[-1:]

        uid = uids[0]
        uid_str = uid.decode() if isinstance(uid, bytes) else str(uid)

        # Headers
        typ, data = conn.fetch(uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        if typ != "OK" or not data or data[0] is None or data[0] == b')':
            return None

        raw = data[0][1].decode("utf-8", errors="replace") if isinstance(data[0][1], bytes) else ""
        h_from = re.search(r"^From:\s*(.+)$", raw, re.M | re.I)
        h_subj = re.search(r"^Subject:\s*(.+)$", raw, re.M | re.I)
        sender_raw = h_from.group(1).strip() if h_from else "inconnu"
        subject = h_subj.group(1).strip() if h_subj else "(sans sujet)"

        m = re.search(r"<?([\w.+-]+@[\w.-]+)>?", sender_raw)
        sender_email = m.group(1) if m else sender_raw
        service = detect_service(sender_email)

        # Corps complet — systématiquement extrait et conservé
        body = ""
        body_preview = ""
        try:
            typ, data = conn.fetch(uid, "(BODY[])")
            if typ == "OK" and data and data[0] and data[0] != b')':
                raw_body = data[0][1]
                if isinstance(raw_body, bytes):
                    body = raw_body.decode("utf-8", errors="replace")
                    body_preview = body[:300]
        except Exception:
            pass

        # OTP detection — on cherche le code UNIQUEMENT dans le message usager
        # Problème : les en-têtes DKIM/ARC/SPF contiennent des faux codes (signatures Google)
        # Solution : on retire les en-têtes de routage (lignes DKIM-Signature, ARC-*, Received, etc.)
        # et on ne garde que le corps visible (après le premier Content-Type: multipart ou text)
        otp = None
        body_clean = body
        # Trouver le dernier contenu text/plain ou text/html
        for marker in ["Content-Type: text/plain;", "Content-Type: text/html;"]:
            pos = body.rfind(marker)
            if pos >= 0:
                after = body.find("\n\n", pos)
                if after >= 0:
                    candidate = body[after + 2:]
                    # Couper au prochain boundary
                    next_bnd = candidate.find("\n--")
                    if next_bnd >= 0:
                        candidate = candidate[:next_bnd]
                    codes = OTP_RE.findall(candidate)
                    valid = [c for c in codes if 5 <= len(c) <= 8]
                    if valid:
                        otp = valid[0]  # premier code dans la section = le plus proche de l'objet du mail
                        break
        # Fallback : si rien trouvé dans text/plain, chercher dans tout le body
        # mais en ignorant les lignes DKIM/ARC/Received
        if not otp:
            lines = body.split("\n")
            clean_lines = []
            skip = False
            for line in lines:
                low = line.lower()
                if any(kw in low for kw in ["dkim-signature", "arc-seal", "arc-message-",
                                             "arc-authentication", "x-google-dkim",
                                             "received:", "authentication-results"]):
                    skip = True
                elif line.strip() == "":
                    skip = False
                if not skip:
                    clean_lines.append(line)
            body_clean = "\n".join(clean_lines)
            codes = OTP_RE.findall(body_clean)
            otp = next((c for c in codes if 5 <= len(c) <= 8), None)

        # Sauvegarde du corps complet dans un fichier consultable
        mail_id = f"{email_addr.replace('@', '_at_')}_{uid_str}"
        body_file = os.path.join(DATA_DIR, "mails", f"{mail_id}.txt")
        os.makedirs(os.path.join(DATA_DIR, "mails"), exist_ok=True)
        with open(body_file, "w") as f:
            f.write(body)

        # Marquer comme lu si demandé
        if mark:
            try:
                conn.store(uid, "+FLAGS", "\\Seen")
            except Exception:
                pass

        info = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "mailbox": email_addr,
            "sender": sender_email,
            "subject": subject[:300],
            "service": service or "autre",
            "otp": otp,
            "uid": uid_str,
            "body_preview": body_preview,
            "body_file": body_file,
        }

        if otp:
            info["type"] = "otp"
            info["msg"] = f"🔑 {email_addr} ← {sender_email}"
            if service and service != "autre":
                info["msg"] += f" [{service}]"
            info["msg"] += f" code: {otp}"
        else:
            info["type"] = "mail"
            info["msg"] = f"📩 {email_addr} ← {sender_email}"
            if service and service != "autre":
                info["msg"] += f" ({service})"
            info["msg"] += f" — {subject[:100]}"

        return info

    except Exception as e:
        logger.debug(f"parse_last_email({email_addr}): {e}")
        return None
    finally:
        try:
            conn.logout()
        except Exception:
            pass


def append_report(info: dict):
    reports = []
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE) as f:
                reports = json.load(f)
        except Exception:
            reports = []
    reports.append(info)
    if len(reports) > 5000:
        reports = reports[-5000:]
    with open(REPORT_FILE, "w") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)
    with open(os.path.join(DATA_DIR, "mail_watch_latest.txt"), "a") as f:
        f.write(f"{info['ts']} | {info['msg']}\n")


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Log Watcher ─────────────────────────────────────────────────────────

def watch_logs():
    """
    Boucle principale : tail -F /var/log/syslog pour détecter les
    livraisons Postfix vers nos boîtes, puis fetch IMAP sur la boîte
    concernée.
    """
    state = load_state()
    already_processed = set(state.get("processed_queue_ids", []))

    logger.info(f"🚀 Démarrage watcher logs Postfix (docker logs --follow)")
    logger.info(f"   {len(already_processed)} queue_ids déjà traités dans le cache")

    # Lancer docker logs --follow en subprocess
    POSTFIX_CONTAINER = "mailcowdockerized-postfix-mailcow-1"
    try:
        # Vérifier d'abord que le container existe et tourne
        check = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        if POSTFIX_CONTAINER not in check.stdout:
            logger.error(f"Container {POSTFIX_CONTAINER} introuvable")
            return

        proc = subprocess.Popen(
            ["docker", "logs", "--tail", "0", "--follow", POSTFIX_CONTAINER],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
    except FileNotFoundError:
        logger.error("docker command not found")
        return

    pending_emails = {}  # email -> timestamp de détection

    while KEEP_RUNNING:
        # Lire les nouvelles lignes
        line = proc.stdout.readline()
        if not line:
            if proc.poll() is not None:
                logger.error("Process tail terminé, redémarrage...")
                break
            continue

        line = line.strip()

        # On cherche les livraisons Postfix vers nos boîtes
        # Pattern: postfix/lmtp[...]: XXXXXX: to=<email@automatisations.org>, ... status=sent
        m = re.search(r'([A-F0-9]+): to=<([\w.+-]+@' + re.escape(MAIL_DOMAIN) + r')>.*status=sent', line)
        if not m:
            continue

        queue_id = m.group(1)
        email = m.group(2)
        pwd = password_for(email)
        if not pwd:
            logger.debug(f"Mot de passe inconnu pour {email}, ignoré")
            continue

        # Extraire le queue_id pour éviter les doublons
        queue_match = re.search(r'([A-F0-9]+): to=', line)
        queue_id = queue_match.group(1) if queue_match else None

        if queue_id and queue_id in already_processed:
            continue

        if queue_id:
            already_processed.add(queue_id)

        # Aussi dédupliquer par email rapidement
        if email in already_processed and not queue_id:
            continue
        if not queue_id:
            already_processed.add(email)

        # Nettoyer le cache
        if len(already_processed) > 500:
            already_processed = set(list(already_processed)[-300:])
            # Sauvegarder périodiquement
            state["processed_queue_ids"] = list(already_processed)
            save_state(state)

        logger.info(f"📨 Détecté: {email}")

        # Attendre un peu pour laisser Dovecot terminer la livraison
        time.sleep(DELIVERY_GRACE_SEC)

        try:
            info = parse_last_email(email, pwd)
            if info:
                append_report(info)
                notify_telegram(info["msg"])
                logger.info(f"✅  {info['msg']}")
            else:
                logger.debug(f"Message pour {email} pas encore accessible")
        except Exception as e:
            logger.error(f"Erreur fetch {email}: {e}")

    proc.terminate()


# ── Web UI / Check ──────────────────────────────────────────────────────

def check_last(n: int = 5):
    if not os.path.exists(REPORT_FILE):
        print("📭 Aucun rapport.")
        return
    with open(REPORT_FILE) as f:
        reports = json.load(f)
    print(f"📋 {len(reports)} événements.\n")
    for r in reports[-n:]:
        ts = r.get("ts", "?")[:19]
        mb = r.get("mailbox", "?")
        svc = r.get("service", "?")
        otp = f" → Code: {r['otp']}" if r.get("otp") else ""
        marker = "🔑" if r.get("type") == "otp" else ("📩" if r.get("type") != "other" else "💬")
        print(f"{marker} [{ts}] {mb}")
        print(f"   ← {r.get('sender','?')} ({svc}){otp}")
        print()


def check_now():
    """Vérification manuelle : cherche les nouveaux messages non-lus sur TOUTES les boîtes via MySQL."""
    logger.info("🔍 check-now: vérification de toutes les boîtes")
    
    # Récupérer toutes les boîtes depuis MySQL Mailcow
    try:
        # Lire mailcow.conf pour le mot de passe
        with open("/opt/mailcow-dockerized/mailcow.conf") as f:
            conf = f.read()
        dbpass = re.search(r'^DBPASS=(.+)$', conf, re.M)
        if not dbpass:
            logger.error("Impossible de lire DBPASS")
            return
        dbpass = dbpass.group(1).strip()
        
        import mysql.connector
        conn = mysql.connector.connect(
            host="127.0.0.1", port=13306,
            user="mailcow", password=dbpass,
            database="mailcow"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM mailbox WHERE kind='inbox' OR kind IS NULL")
        all_mailboxes = [row[0] for row in cursor.fetchall()]
        conn.close()
    except ImportError:
        logger.error("mysql-connector-python pas installé")
        return
    except Exception as e:
        logger.error(f"Erreur BDD: {e}")
        return

    logger.info(f"{len(all_mailboxes)} boîtes trouvées en base")

    count = 0
    for email in all_mailboxes:
        if not KEEP_RUNNING:
            break
        pwd = password_for(email)
        if not pwd:
            continue

        conn = None
        try:
            conn = connect_imap(email, pwd)
            typ, data = conn.select("INBOX")
            if typ != "OK":
                continue

            typ, data = conn.search(None, "UNSEEN")
            if typ != "OK" or not data[0]:
                continue

            for uid in data[0].split():
                # Marquer comme lu d'abord
                if MARK_AS_SEEN:
                    conn.store(uid, "+FLAGS", "\\Seen")

                uid_str = uid.decode() if isinstance(uid, bytes) else str(uid)

                # Récupérer les headers
                typ, data = conn.fetch(uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
                if typ != "OK" or not data[0] or data[0] == b')':
                    continue

                raw = data[0][1].decode("utf-8", errors="replace") if isinstance(data[0][1], bytes) else ""
                h_from = re.search(r"^From:\s*(.+)$", raw, re.M | re.I)
                h_subj = re.search(r"^Subject:\s*(.+)$", raw, re.M | re.I)
                sender_raw = h_from.group(1).strip() if h_from else "inconnu"
                subject = h_subj.group(1).strip() if h_subj else "(sans sujet)"

                m = re.search(r"<?([\w.+-]+@[\w.-]+)>?", sender_raw)
                sender = m.group(1) if m else sender_raw

                service = detect_service(sender)

                corps = ""
                try:
                    typ, data = conn.fetch(uid, "(BODY.PEEK[TEXT])")
                    if typ == "OK" and data and data[0] and data[0] != b')':
                        corps = data[0][1].decode("utf-8", errors="replace") if isinstance(data[0][1], bytes) else ""
                except Exception:
                    pass

                otp = None
                if service:
                    codes = OTP_RE.findall(corps)
                    otp = next((c for c in codes if 5 <= len(c) <= 8), None)

                info = {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "mailbox": email,
                    "sender": sender,
                    "subject": subject[:200],
                    "service": service or "autre",
                    "otp": otp,
                    "uid": uid_str,
                    "type": "otp" if (service and otp) else ("service" if service else "other"),
                }
                info["msg"] = f"🔑 {email} ← {sender} [{service}] code: {otp}" if (service and otp) else (
                    f"📩 {email} ← {sender} ({service})" if service else
                    f"💬 {email} ← {sender} — {subject[:80]}"
                )

                append_report(info)
                count += 1
                logger.info(f"📨 {info['msg']}")

        except Exception as e:
            logger.debug(f"{email}: {e}")
        finally:
            if conn:
                try:
                    conn.logout()
                except Exception:
                    pass

    logger.info(f"✅ check-now terminé: {count} nouveaux messages")


def status():
    reports = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE) as f:
            reports = json.load(f)

    running = False
    try:
        r = subprocess.run(["pgrep", "-f", "mail_watch.py"], capture_output=True, text=True)
        running = r.returncode == 0 and r.stdout.strip()
    except Exception:
        pass

    print(f"{'🟢' if running else '🔴'} Watcher: {'EN COURS' if running else 'ARRÊTÉ'}")
    print(f"Rapports: {len(reports)} événements")

    if running:
        try:
            pids = subprocess.run(["pgrep", "-f", "mail_watch.py"],
                capture_output=True, text=True).stdout.strip().split("\n")
            print(f"PID: {pids[0]}")
        except Exception:
            pass

    if reports:
        last = reports[-1]
        print(f"\nDernier: {last.get('msg','?')}")
        print(f"  [{last.get('ts','?')[:19]}]")

    # Compter les OTP
    otp_count = sum(1 for r in reports if r.get("type") == "otp")
    if otp_count:
        print(f"  {otp_count} codes OTP détectés")
    print()


def read_mail(identifier: str):
    """Affiche le corps complet d'un mail reçu.

    Args:
        identifier: soit une adresse email (ex: adam.app@automatisations.org)
                    soit un numéro d'index (ex: 2 pour le 2e événement)
                    soit "last" pour le dernier
    """
    if not os.path.exists(REPORT_FILE):
        print("📭 Aucun rapport.")
        return

    with open(REPORT_FILE) as f:
        reports = json.load(f)

    if not reports:
        print("📭 Aucun événement.")
        return

    # Déterminer quel événement afficher
    target = None
    if identifier == "last":
        target = reports[-1]
    elif identifier.isdigit():
        idx = int(identifier) - 1
        if 0 <= idx < len(reports):
            target = reports[idx]
        else:
            print(f"❌ Index {identifier} invalide (1-{len(reports)})")
            return
    else:
        # Chercher par adresse email
        found = [r for r in reports if r.get("mailbox", "").startswith(identifier)]
        if not found:
            print(f"❌ Aucun mail trouvé pour '{identifier}'")
            return
        target = found[-1]

    # Afficher les infos
    print(f"{'='*60}")
    print(f"📬 {target.get('mailbox','?')}")
    print(f"   Date:     {target.get('ts','?')[:19]}")
    print(f"   De:       {target.get('sender','?')}")
    print(f"   Sujet:    {target.get('subject','?')}")
    print(f"   Service:  {target.get('service','?')}")
    if target.get('otp'):
        print(f"   Code OTP: {target['otp']}")
    print(f"{'='*60}")

    # Charger le corps depuis le fichier
    body_file = target.get('body_file')
    if body_file and os.path.exists(body_file):
        with open(body_file) as f:
            body = f.read()
        # Décoder le corps si base64
        import email
        from email import policy
        try:
            msg = email.message_from_string(body, policy=policy.default)
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_text = payload.decode("utf-8", errors="replace")
                            print(body_text)
                            break
                    elif part.get_content_type() == "text/html":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_text = payload.decode("utf-8", errors="replace")
                            print("[Contenu HTML, voici le texte brut:]")
                            import html
                            print(html.unescape(re.sub(r'<[^>]+>', '', body_text)))
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body_text = payload.decode("utf-8", errors="replace")
                    print(body_text)
        except Exception as e:
            # Fallback: affichage brut
            print(f"[Impossible de décoder: {e}]")
            print(body[:2000])
    else:
        # Fallback: fetch direct IMAP
        print("[Fichier non trouvé, tentative de re-fetch IMAP...]")
        email = target.get('mailbox', '')
        pwd = password_for(email)
        if not email or not pwd:
            print("❌ Impossible de se connecter.")
            return
        try:
            conn = connect_imap(email, pwd)
            conn.select("INBOX")
            uid = target.get('uid', '')
            if uid:
                typ, data = conn.fetch(uid.encode(), "(BODY[])")
                if typ == "OK" and data and data[0]:
                    raw = data[0][1]
                    if isinstance(raw, bytes):
                        body = raw.decode("utf-8", errors="replace")
                        print(body[:3000])
            conn.logout()
        except Exception as e2:
            print(f"❌ Échec: {e2}")


def read_mail_help():
    print("Usage: python3 mail_watch.py --read-mail <id>")
    print("  <id>  = 'last' | index (1, 2...) | adresse email (adam.app)")
    print("  Ex:   --read-mail last")
    print("  Ex:   --read-mail adam.app@automatisations.org")
    print("  Ex:   --read-mail 2")


if __name__ == "__main__":
    if "--check-last" in sys.argv:
        i = sys.argv.index("--check-last")
        n = int(sys.argv[i + 1]) if len(sys.argv) > i + 1 else 5
        check_last(n)
    elif "--status" in sys.argv:
        status()
    elif "--check-now" in sys.argv:
        check_now()
    elif "--read-mail" in sys.argv:
        i = sys.argv.index("--read-mail")
        ident = sys.argv[i + 1] if len(sys.argv) > i + 1 else "last"
        read_mail(ident)
    elif "--read-mail-help" in sys.argv:
        read_mail_help()
    else:
        logger.info("🚀 Démarrage du watcher logs Postfix")
        while KEEP_RUNNING:
            try:
                watch_logs()
            except Exception as e:
                logger.error(f"Crash: {e}, redémarrage dans 5s...")
                time.sleep(5)
