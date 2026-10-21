import sys
import io
import os
import json
import argparse
import smtplib
import imaplib
import email
from email.mime.text import MIMEText

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SECRETS_PATH = r'C:/ai/secrets/gmail.json'

def load_gmail_credentials():
    if not os.path.isfile(SECRETS_PATH):
        print('[FAIL] Gmail credentials not configured.')
        print('[FAIL] Expected: ' + SECRETS_PATH)
        print('[FAIL] File must contain: "{\"email\": \"...\", \"app_password\": \"...\"}"')
        sys.exit(1)
    try:
        with open(SECRETS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print('[FAIL] Could not read credentials file: ' + str(e))
        sys.exit(1)
    email_addr = data.get('email', '').strip()
    password = data.get('app_password', '').strip()
    if not email_addr or not password:
        print('[FAIL] Credentials file missing email or app_password.')
        sys.exit(1)
    return email_addr, password

EMAIL_ADDRESS, APP_PASSWORD = load_gmail_credentials()

def check_gmail(count=10, search_term=None):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_ADDRESS, APP_PASSWORD)
        mail.select('inbox')
        if search_term:
            status, messages = mail.search(None, f'TEXT "{search_term}"')
        else:
            status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        print('----------')
        print(f'[OK] Found {len(email_ids)} emails. Fetching last {min(count, len(email_ids))}:')
        for e_id in email_ids[-count:]:
            _, msg_data = mail.fetch(e_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    print(f"From: {msg.get('from', 'Unknown')}")
                    print(f"Subject: {msg.get('subject', '(No Subject)')}")
                    print('----------')
        mail.logout()
    except Exception as e:
        print(f'[FAIL] Error checking emails: {e}')
    sys.stdout.flush()

def send_gmail(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, APP_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print('[OK] Email sent successfully!')
    except Exception as e:
        print(f'[FAIL] Error sending email: {e}')
    sys.stdout.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gmail CLI Helper')
    parser.add_argument('--action', choices=['check', 'send'], default='check')
    parser.add_argument('--count', type=int, default=10)
    parser.add_argument('--search', type=str, default=None)
    parser.add_argument('--to', type=str, default=None)
    parser.add_argument('--subject', type=str, default='')
    parser.add_argument('--body', type=str, default='')
    args, unknown = parser.parse_known_args()

    if args.action == 'send':
        if not args.to:
            print('[FAIL] Recipient address (--to) is required for sending email.')
        else:
            send_gmail(args.to, args.subject, args.body)
    else:
        check_gmail(args.count, args.search)