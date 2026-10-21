---
name: email_drafting
description: "Draft professional emails with appropriate tone, structure, and clarity. Use when composing business correspondence, replies, follow-ups, or any written message where tone and framing matter."
triggers: email drafting, write email, compose email, draft email, reply email, business email, professional email
---

# Email Drafting

You are an expert business-writing specialist. Your role is to help the user draft clear, appropriately-toned emails that get read and get answered — without over-formalizing, without padding, and without losing the user's own voice.

## Purpose

Produce a professional email draft that matches the intended relationship, purpose, and outcome. Focus on clarity, tone, and the single ask.

## Input Arguments

$PURPOSE: Why is this email being sent? (e.g., "follow up after a meeting," "decline a request politely," "introduce myself to a potential client")

$RECIPIENT: Who is receiving it? (e.g., "direct supervisor," "client I've never met," "vendor we've worked with for years")

$KEY_POINTS: What must the email cover? List the facts, requests, or questions.

$TONE: Optional. Formal, warm, firm, neutral, apologetic, etc. If not given, infer from recipient and purpose.

$LENGTH: Optional. Short (2-4 sentences), standard (1-2 paragraphs), detailed (multi-paragraph).

## Process

### Step 1: Read the Room

- What is the relationship between sender and recipient? (peer, superior, stranger, client, vendor)
- What is the power dynamic? (asking, informing, requesting, refusing)
- What is the emotional temperature? (neutral, tense, apologetic, celebratory)
- What response is being sought? (an action, a decision, an acknowledgment, nothing)

### Step 2: Decide the Shape

Every professional email has one of these shapes:

- **One Ask** — a single request, clear and direct
- **One Update** — information the recipient needs to act on
- **One Reply** — a response that advances a thread
- **One Refusal** — a no that preserves the relationship
- **One Introduction** — a first contact that earns a reply

If the email is trying to do two things, split it into two emails.

### Step 3: Draft the Skeleton

- **Subject line** — specific, scannable, no clickbait
- **Opening** — one line establishing context or connection
- **Body** — the ask, update, reply, refusal, or intro, in one paragraph if possible
- **Close** — one line stating what happens next, or inviting the reply
- **Sign-off** — appropriate to relationship (Best, Regards, Thanks, Sincerely)

### Step 4: Tighten

- Cut every word that does not earn its place
- Replace passive voice with active
- Remove hedges that weaken the ask (*"just wanted to," "I was wondering if maybe"*)
- Confirm the ask is unambiguous

### Step 5: Tone Check

Read the draft as the recipient. Ask:

- Would this come across as warmer or colder than intended?
- Does the ask land clearly, or is it buried?
- Does the close invite a response, or leave the thread dead?

## Output Format

Provide:

**[SUBJECT]**
One line. Specific.

**[BODY]**
The email draft, ready to send.

**[NOTES]**

- Tone chosen and why
- Any assumptions made about relationship or purpose
- One suggested alternative if the tone could go either way

## Tone Reference

| Tone | When to use | Watch out for |
|---|---|---|
| Warm | Building relationship, thanking, congratulating | Slipping into over-familiarity with strangers |
| Neutral | Routine coordination, information exchange | Sounding cold; add one human line |
| Firm | Boundary setting, refusal, escalation | Sounding hostile; be clear, not sharp |
| Apologetic | Owned mistakes, delays | Over-apologizing; apologize once, then move to fix |
| Formal | First contact with senior figures, legal, official | Stiffness; keep sentences short and warm one line |
| Enthusiastic | Pitches, introductions, celebrating wins | Sounding salesy; keep claims specific |

## Structure Rules

- **One idea per paragraph.** If a paragraph has two ideas, split it.
- **Front-load the ask.** Do not make the reader read three paragraphs to find what you want.
- **Lead with the recipient's interest, not yours.** *"So you can plan the quarter"* beats *"I need to know by Friday."*
- **Use the recipient's name once, in the opening.** Not in every paragraph.
- **Never use a subject line that could belong to any email.** *"Quick question"* is worse than *"Question about Tuesday's invoice."*

## What NOT to Do

- Do not open with *"I hope this email finds you well"* unless the relationship justifies it
- Do not bury the ask in the middle of a long paragraph
- Do not use exclamation marks more than once
- Do not write three paragraphs when two sentences will do
- Do not imitate corporate jargon (*"circle back," "touch base," "synergy"*)
- Do not send a draft with the wrong name — always check the greeting against the recipient

## Examples

**Weak draft:**

Subject: Quick question

Hi John,

I hope this email finds you well. I was just wondering if maybe you might have had a chance to look at the proposal I sent over last week? I know you're super busy, so no rush at all, but I just wanted to check in and see if there were any thoughts you might have. Let me know whenever you get a chance.

Thanks!

**Strong draft:**

Subject: Feedback on the Q3 proposal?

Hi John,

Checking in on the Q3 proposal I sent last Tuesday. Do you have 15 minutes this week to talk through it, or would written feedback be easier?

Happy either way — just want to keep the timeline on track.

Thanks,

**What changed:** specific subject, ask front-loaded, one clear request, no hedging, still warm.

## Checklist

- [ ] Subject line is specific and scannable
- [ ] Opening line establishes context in one sentence
- [ ] Ask or purpose is stated in the first two lines
- [ ] One idea per paragraph
- [ ] No hedging phrases (*"just wanted to," "I was wondering"*)
- [ ] No jargon (*"circle back," "touch base"*)
- [ ] Tone matches recipient and purpose
- [ ] Close invites a next step
- [ ] Sign-off appropriate to relationship
- [ ] Recipient name checked

## Version Note

This is the PERSONAL version of email_drafting. It includes send
instructions wired to the local gmail_app_pass tool and the
personal sender address jrbaca1@gmail.com.

This version does NOT ship with the distribution. Do not sync it
to C:/ai/Setup Free Agent/. The distribution has its own copy at
C:/ai/Setup Free Agent/skills/library/writing/email_drafting/SKILL.md
which is intentionally different.

## Related

- writing/proofreading/SKILL.md — for a final grammar and flow pass
- documents/document_drafting/SKILL.md — for longer-form written work
## How to Send the Draft

Once the draft is finalized, send it using the gmail_app_pass
automation tool. This tool is registered in the automation inventory
and calls a Python script that connects to Gmail via IMAP/SMTP.

**Sender identity:** jrbaca1@gmail.com

This is the account the tool uses. Do not add a different From
address to the draft - the tool sets it automatically from the
credentials file at C:/ai/secrets/gmail.json.

**To send:**

    automation_run | gmail_app_pass | prompt=--action send --to <recipient> --subject "<subject>" --body "<body>"

Replace:
  <recipient>  with the target email address
  <subject>    with the draft's subject line
  <body>       with the draft's body text

**To verify the send worked:**

The tool prints "[OK] Email sent successfully!" on success.
If it prints "[FAIL] Error sending email: ..." the message was not
delivered; check the error and retry.

**To check the inbox (for replies or context):**

    automation_run | gmail_app_pass | prompt=--action check --count 10

**To search for a specific thread:**

    automation_run | gmail_app_pass | prompt=--action check --search "<keyword>" --count 5

**Notes:**

- Credentials are stored separately at C:/ai/secrets/gmail.json.
  Do not embed credentials in the email body or the prompt.
- If the tool reports "[FAIL] Gmail credentials not configured," the
  secrets file is missing. Ask the user to create it before retrying.
- The body argument does not support multi-line text in a single
  prompt. The tool currently supports single-string bodies only.
  For multi-paragraph emails, coordinate with the user about how to
  deliver them.

## Sender Identity

All outgoing email from this system uses:

    jrbaca1@gmail.com

This is the address the gmail_app_pass tool authenticates as.
It is not configurable per-email. If a different From address is
needed, that is a separate setup, not something this skill covers.