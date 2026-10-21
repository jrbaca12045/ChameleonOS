---
name: github_library_publish
description: "Publish or update the public ChameleonOS library on GitHub - the free skills, example scripts, and personas. Use when updating the GitHub repo, pushing library changes, adding a skill or script to the public repo, or refreshing what users can download."
triggers: github library, update github, push to github, publish library, public repo, github repo update, add to github, chameleonos github, publish skills, publish scripts
---

# GitHub Library Publish

The free ChameleonOS library is published at **https://github.com/jrbaca12045/ChameleonOS**. It holds the skills, the example scripts, and the persona definitions. The app itself stays on the Microsoft Store; this repo is the library, not the installer.

## The facts (verified 2026-10-21)

- **Local repo:** `D:/ai/github_chameleonos`
- **Remote:** `https://github.com/jrbaca12045/ChameleonOS.git`
- **Branch:** `main` (tracking `origin/main`)
- **First commit:** `b352b14` - Initial library, 78 files, 8,681 insertions
- **Git identity:** `jrbaca1` / `jrbaca1@gmail.com` (already configured)
- **Credentials:** stored in Windows Credential Manager - push does not prompt

## How to update the repo

When a skill, script, or persona changes in its source location, copy it into the repo folder, then commit and push.

    cd /d D:\ai\github_chameleonos
    git add .
    git commit -m "describe what changed"
    git push

The push uses the stored credential. If it ever asks for a password, use a Personal Access Token with repo scope, not the account password.

## What goes in, what stays out

| Include | Exclude |
|---|---|
| `skills/**/SKILL.md` | `*.bak` and `*.bak_*` files |
| `example-scripts/**` (no backups) | `web_persona_*_state.json` (runtime state) |
| `personas/*.txt` and `*_activation.txt` | `secrets/gmail.json` (real credentials) |
| `README.md` | `*.pdb`, `__pycache__`, `.pyc` |

The persona config JSONs (`web_persona_<slug>.json`) are safe - they contain only the quiz, the persona name, and a recovery file path. The **state** JSONs are runtime counters and should not be published.

## Source locations

When a source file changes, copy it into the repo rather than editing the repo copy, so the working tree and the published copy stay identical.

| Repo folder | Source |
|---|---|
| `skills/` | `C:/ai/skills/library/` (only `SKILL.md` files) |
| `example-scripts/` | `D:/ai/example scripts/` |
| `personas/` | `C:/ai/persona/` (only `.txt` files) |

## Verify a push

Reading the push output is not proof. Fetch a file from the live repo and confirm it returns 200:

    https://raw.githubusercontent.com/jrbaca12045/ChameleonOS/main/README.md
    https://raw.githubusercontent.com/jrbaca12045/ChameleonOS/main/skills/meta/adding_skills/SKILL.md

If those load, the push landed. If they 404, the commit or the push failed silently - check `git log --oneline -3` and `git status`.

## Rules learned the hard way

- **Never run `git init` in a folder that already has a repo above it.** Check with `git rev-parse --show-toplevel` first.
- **Never `echo` a README in the terminal's current directory.** `cd` into the repo folder first, or the wrong folder becomes a repo.
- **A public repo is permanent once crawled.** Run the credential scan before the first push of any new file set.
- **Line-ending warnings (`LF will be replaced by CRLF`) are normal on Windows** and are not errors.
- **A rejected push after a remote change needs a pull first:** `git pull --rebase origin main`, then push again.

## Checklist

- [ ] Source file changed and tested in its original location
- [ ] Copied into `D:/ai/github_chameleonos` at the matching path
- [ ] No `.bak`, no state JSON, no credentials added
- [ ] `git add .` then `git commit` with a real message
- [ ] `git push` succeeded
- [ ] Fetched a raw URL from the live repo and got 200