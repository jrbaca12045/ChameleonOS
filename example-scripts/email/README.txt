GMAIL APP PASS TOOL INSTRUCTIONS
==================================
This tool provides full email functionality (checking, searching, sending)
via Gmail IMAP/SMTP, using an App Password for authentication.

SETUP (one-time)
-----------------
This tool reads credentials from a config file:
    C:/ai/secrets/gmail.json

The file must contain exactly this structure:

    {
      "email": "your.email@gmail.com",
      "app_password": "your-16-character-app-password"
    }

To generate a Gmail App Password:
  1. Enable 2-Step Verification on your Google account.
  2. Visit https://myaccount.google.com/apppasswords
  3. Generate a new App Password for 'Mail'.
  4. Copy the 16-character password into secrets/gmail.json.

A template file is provided at secrets/gmail.json.example.
Copy it, rename to gmail.json, and fill in your values.

If secrets/gmail.json does not exist or is malformed, the tool
will print a clear [FAIL] message and exit without attempting
any network connection.

USAGES & EXAMPLES FOR AI/AUTOMATION_RUN:
---------------------------------------

1. CHECK RECENT INBOX EMAILS (Default count = 10):
   automation_run | gmail_app_pass | prompt=--action check --count 10

2. SEARCH EMAILS BY KEYWORD:
   automation_run | gmail_app_pass | prompt=--action check --search "Instagram" --count 5

3. SEND AN EMAIL:
   automation_run | gmail_app_pass | prompt=--action send --to recipient@example.com --subject "Test Subject" --body "Hello from automation script!"

PARAMETER FLAGS:
  --action   : "check" (read inbox) or "send" (deliver message). Default: check
  --count    : Number of email headers to display (integer). Default: 10
  --search   : Keyword/phrase filter for searching subject/body text.
  --to       : Target email address (Required when --action send).
  --subject  : Subject line string.
  --body     : Body content text string.
