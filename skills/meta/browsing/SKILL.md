---
name: browsing
description: "Use native server-side browsing to search, read, and gather from the web, then use Free Agent's local file tools to save what was gathered. The combined loop that lets one turn search, screen, and persist without a paste step. Use when the task is to find something on the web and keep it."
triggers: browsing, browse web, browse internet, read page, fetch from web, look up online, find on the web, gather from web
---

# Browsing

A two-hand loop. Native browsing is the eyes; Free Agent file tools are the hands. Neither alone completes the task - together they do.

## When to use this

Use this skill when:

- The user asks you to find something on the web and save it
- The user asks you to research a topic and keep the result
- A skill needs to be found in a registry and written to the library
- Any task where the pattern is *go look, then keep what you found*

Do NOT use this skill when the result is only needed in conversation. If nothing needs to persist, native browsing alone is enough.

## The two hands

| Hand | What it does | What it cannot do |
|---|---|---|
| **Native browsing** (server-side) | Search, open, read pages on the web | Write anything to disk |
| **Free Agent tools** (local) | Read/write files, run Python, store memory | Reach the open web on their own |

**The pattern:** browse natively to find and read; save locally to keep. The two steps never mix. The web stays outside the disk; the disk stays outside the web.

## The procedure

1. **Understand the ask.** What is being looked for? What has to persist when it is found?

2. **Search natively.** Use server-side web search. Try more than one registry or source. Cross-check claims.

3. **Read the candidate.** Open the page. Read it. Every line of it. Do not skim.

4. **Screen it.** See *What NOT to do* below for the red-flag list.

5. **Show the shortlist.** Before writing anything, present the candidate(s) and what was actually found. The user approves.

6. **Save with local tools.** Use file_write (or file_write_append for large files). Back up any file being edited first, per the backup_rule card.

7. **Index and verify.** If the target is the skills library, add one line to library/index.md and read the written file back. If the target is elsewhere, verify with file_read.

8. **Report provenance.** Say where the content came from. *Found on X, read on Y, saved to Z.* No pretending a written-from-scratch file came from the web.