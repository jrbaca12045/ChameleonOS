---
name: d_drive_handoff
description: Preserve the work from a C:/ai session to D:/ai so examples, scripts, and skills survive for posterity. Use at the end of any session that created or updated example scripts, tools, skills, or documentation. Covers what goes where, how each item must be documented, the safety rule for credentials, and the cadence for when to do it.
---

# D Drive Handoff — Preserve the Work

Every session that produces something worth keeping must leave a copy on D:/ai. The C: drive can be lost. The D: drive is where the lasting artifacts live.

## 1. Source of truth

Files ALWAYS flow FROM C:/ai/ TO D:/ai/. Never the reverse.

C:/ai/ is the working tree. D:/ai/ is the preserved mirror. If C and D disagree, C is correct and D is stale.

## 2. What goes to D

Any file that a future session would need and that would be expensive to recreate:

- **Example scripts** — the reusable tools a customer or another session could pick up
- **New skills** — SKILL.md files, plus the population script must be re-run after
- **Supporting docs** — setup guides, READMEs, config examples
- **Reference data** — templates, checklists, manifests

What does NOT go to D:

- Credentials of any kind (`secrets/gmail.json`, API keys, tokens)
- Personal data (email addresses, names, account IDs)
- Backups (`*.bak_*`, `*.broken_*`, `*.tmp`)
- Large binaries that live elsewhere (models, MSIX packages — keep those in their own backups)
- Logs, error screenshots, cache files
- Compiled artifacts (`__pycache__`, `.pyc`)

## 3. Folder layout

```
D:/ai/
  README.txt                 -- what this tree is, one page
  example scripts/
    README.txt               -- index of everything in this folder
    <name>/
      <main script>.py       -- the tool itself
      README.txt             -- full usage reference
      <config>.example       -- placeholder template, never real credentials
      setup.txt              -- quick-start for a first-time user
    <name2>/
      ...
```

Every subfolder is self-contained. A user can copy that folder anywhere and run it. No dependency on Free Agent being installed.

## 4. Documentation requirement (mandatory)

A folder without a README is not finished. Every example folder MUST have:

- `README.txt` — what the tool does, its usage examples, its flags/parameters
- `setup.txt` — step-by-step: install Python, copy config, obtain credentials, test it
- `<config>.example` — the placeholder template. Include the file structure but no real values.

If a tool has no config, the setup.txt explains how to run it directly.

Update the parent `README.txt` in `example scripts/` to list the new entry.

## 5. The safety rule

Before writing ANY file to D, scan it for:

- `jrbaca1` — your Gmail address
- `app_password` followed by a 16-character value
- Any `sk-...` API key pattern (OpenAI), `AIza...` (Google), `AKIA...` (AWS)
- Filenames matching `secrets/` except `*.example`

If any of those match, do NOT copy. Rewrite the source file to remove the credential first, or ship the `.example` version.

Real credentials belong in `C:/ai/secrets/` (live) and never leave that folder.

## 6. The copy procedure

For each item to preserve:

1. Confirm the source exists in `C:/ai/` at the expected path and size
2. Scan for personal data (section 5)
3. Copy with `shutil.copy2` (preserves timestamps)
4. Verify destination size equals source size
5. If the file is new to D, update the parent README.txt

One small script per handoff is fine. A general-purpose sync script is also fine, provided it enforces the safety rule and the folder layout rule.

## 7. When to do the handoff

Do it at the END of every session that produced new artifacts. If the session added an example, updated a tool, wrote a skill, or built a doc — the corresponding files go to D before closing.

The rule in one sentence: **if losing C: would lose this work, it goes to D before the session ends.**

Do NOT try to mirror the entire C:/ai tree — that has 984 root-level Python files, most of which are scratch scripts that were used once and no longer matter. Preserve only what a future session or a future user would actually need.

## 8. What to check after a handoff

- Every new example folder has a README.txt and a setup.txt
- Every config example contains only placeholders (no real emails, no real passwords)
- The parent `example scripts/README.txt` lists every subfolder
- The `D:/ai/README.txt` explains the tree
- All copied files opened without errors

## 9. The D:/ai tree today

Currently on D:/ai:

- `example scripts/email/` — Gmail check/send tool (self-contained, config from `secrets/gmail.json`)
- `example scripts/QR-README.txt` + `chameleonos-qr.png` — the site QR code and its instructions
- `example scripts/check_disk_space/` -- report disk usage for a drive or path, warns above 80%
- `example scripts/voice_switching/` -- list and select Speechma voices via screen automation
- `example scripts/window_listing/` -- list visible windows with PID, process name, title
- `example scripts/mouse_coordinates/` -- live mouse position display, cross-platform GUI
- `example scripts/ui_automation/` -- inspect, wait for, and act on Windows UI controls via pywinauto
- `example scripts/README.txt` — index of the folder
- `README.txt` — this tree's top-level README

When a new example is added, update section 9 and the parent `example scripts/README.txt`.
