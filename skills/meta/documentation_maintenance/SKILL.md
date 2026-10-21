---
name: documentation_maintenance
description: "Maintain Free Agent documentation — update master_feature_guide.txt, rebuild section memories, and keep the docs folder coherent. Use when updating the guide, changing documentation, editing master_feature_guide, rebuilding section memories, updating documentation SOP, maintaining docs, promoting a SOP to a skill, or checking documentation for store submission."
triggers: documentation maintenance, update the guide, update master_feature_guide, change the guide, documentation change, rebuild section memories, rebuild guide memories, documentation SOP, documentation update, maintain documentation, update documentation, docs are stale, documentation drift
---

# Documentation Maintenance

Keep `C:/ai/updated_docs/master_feature_guide.txt` — the single source of truth — accurate, and keep the model's section memories in sync with it. The guide describes. Code is truth. Memory embodies. If they disagree, code wins, then the guide, then memory, then human views.

## The one rule that matters most

WHEN THE GUIDE CHANGES, THE MEMORIES MUST CHANGE TOO.

A stale memory gives a stale answer. If you edit the guide and skip Step 6, the model keeps answering from the old section. That is the failure this skill prevents.

## The four layers

- Layer 0 — CODE. Python and VB source. Ultimate truth.
- Layer 1 — THE GUIDE. `master_feature_guide.txt`. Single source of truth for what the system is.
- Layer 2 — MEMORY. Section memories in `agent_memory.db`. What the model actually reads. Derived from the guide.
- Layer 3 — HUMAN VIEWS. HTML, markdown, TOC, index. Rendered from the guide.

Code is truth. Guide describes. Memory embodies. Human views render.

## When you must update the guide

Update the guide when any of the following happens:

- A new subsystem is added to the code
- An existing subsystem changes behavior
- A tool is added, removed, or renamed in `automation_inventory.json`
- A file is moved to or from the Backup Vault
- A new memory type, persona type, or watchdog action is added
- A default value changes (thresholds, timeouts, counts)
- A previously documented claim is found to be wrong
- A section loses its header (structural bug)
- A file is renamed

If a change makes a sentence in the guide wrong, the guide must be updated.

## The procedure

Follow in order. Do not skip.

### Step 1 — Back up the guide

Copy `master_feature_guide.txt` to `master_feature_guide.txt.bak_YYYYMMDD_HHMMSS` in the same folder. This is the undo.

### Step 2 — Back up the memory database

If you will touch memory at all, back up `agent_memory.db` first: `agent_memory.db.bak_YYYYMMDD_HHMMSS`. Memory writes are irreversible without this. Always.

### Step 3 — Make the code change first (if applicable)

Documentation follows code. Do not update the guide to describe untested code.

### Step 4 — Edit the guide

Make the smallest change that makes the guide correct. Do not rewrite sections that are already correct.

STRUCTURAL INVARIANTS — verify after every edit:

- Every section header is `## N. Title` on its own line
- Section numbers run 1 through 27, in order (CURRENT as of 2026-10-21; update this line when a section is added)
- No duplicate headers
- No orphaned content between sections
- No lost `## ` headers from splice operations

Quick check: search the file for lines starting with `## `. You should see exactly 27 numbered sections plus the Layer/Provenance `# ` headers.

### Step 5 — Update the change log

Append one line to `C:/ai/updated_docs/CHANGE_LOG.txt`:

    YYYY-MM-DD HH:MM - [section number] - [what changed and why]

If the change resolved an obsolete claim, also add it to `discarded_features.txt` with the reason.

### Step 6 — Rebuild the section memories

THIS IS THE STEP THAT IS EASY TO FORGET. The guide changed, so the memories are stale.

Two options:

FULL REBUILD — when in doubt, do this.

1. Delete all section memories: `DELETE FROM memories WHERE type='System' AND metadata LIKE '%"source": "guide_section"%' AND metadata LIKE '%"section":%'`
2. Read the current guide; split by `## N.` headers.
3. For each section, generate three embeddings via Ollama (`http://localhost:11434/api/embeddings`, model `nomic-embed-text:latest`). Truncate content to 6000 chars — Ollama returns HTTP 500 for longer input.
4. Insert two memories per section: one trigger, one content. `type='System'`, `importance=10`, `decay_rate=0.0`.
5. Log every inserted id.

SURGICAL ADD — only when the only change is a brand-new section and sections 1..N-1 are unchanged. Insert only that section's two memories. Do not delete existing ones.

AUXILIARY MEMORY HAZARD — the `agent_memory.db` also contains System memories tagged `guide_section` that are NOT guide sections: keys `residents`, `sop`, `test`, `skill_triggers`, `installer`, `deployment`, `frontmatter`, `documentation_locations`. These were mis-tagged by an earlier rebuild. A naive full rebuild with only the first LIKE clause will delete them. Always include the second `AND metadata LIKE '%"section":%'` clause, OR re-tag those aux memories as `source: "auxiliary"` before the rebuild.

### Step 7 — Verify

- `memorystats` shows the new count
- `list_system_memories` shows both trigger and content per section
- A natural test query fires the right section
- An off-topic query does NOT fire

If any check fails, restore `agent_memory.db` from Step 2 and debug before retrying.

### Step 8 — Update the tracking files

If a section was added, removed, or renamed:

- `SECTION_MEMORY_CHECKLIST.txt`
- `python_layer_map.txt` (if Python tools changed)
- `TODO_queued_tasks.txt` (if tasks were completed or added)

### Step 9 — Regenerate human views

If the HTML ebook or TOC exists, regenerate it from the updated guide. If not built, note it in `TODO_queued_tasks.txt`.

### Step 10 — Notify the model (optional)

For a significant change, create a System memory: "The guide was updated on YYYY-MM-DD. Section N now says X." Useful for continuity across sessions.

## What not to do

- Do NOT splice a section without including its `## N.` header line. That was the cause of the 2026-09-25 structural damage.
- Do NOT write to `agent_memory.db` without a backup. Ever.
- Do NOT insert System memories with `decay_rate=0.01`. System memories never decay. Use `0.0`.
- Do NOT send content over 6000 chars to Ollama. Truncate first, store the full text in the content field.
- Do NOT delete section memories by content alone. Match on metadata.
- Do NOT use the `memorystore` tool for section memories. It prevents trigger keywords from being written. Use direct SQL.
- Do NOT skip the change log. Every update gets an entry.
- Do NOT trust the section count in this skill's Step 4 after a new section is added. Update it.

## The files in `updated_docs/` and what they are

- `master_feature_guide.txt` — definitive guide. Single source of truth.
- `00_READ_FIRST_documentation_sop.txt` — the original SOP this skill was promoted from. Kept for reference; this skill supersedes it for execution.
- `SECTION_MEMORY_CHECKLIST.txt` — tracks every section memory. Update after each rebuild.
- `python_layer_map.txt` — classification of every Python file. Update when Python files change.
- `TODO_queued_tasks.txt` — tasks waiting for next session.
- `CHANGE_LOG.txt` — one line per documentation change.
- `phase3_findings.txt`, `round2_findings.txt`, `handoff_phase2.txt` — historical records.
- `discarded_features.txt` — obsolete claims with date, reason, source.
- `_sec*_new.txt`, `_chameleon_new.txt`, `_front_matter_v2.txt`, `_frame_new.txt`, `_epigraph_new.txt` — temporary splice sources, kept for reference, not used at runtime.

## Distribution hygiene

`updated_docs/` is a working folder, not a distribution folder. Before a store submission or public archive, the `.bak*` files (13 as of 2026-10-21, ~925 KB) and `_*_new.txt` fragments (12 files, ~65 KB) are ballast. Move them to a `_archive/` subfolder rather than deleting — the SOP history has value, but a shipping folder should not carry backups.

## Checklist

- [ ] Searched for existing documentation skills (this one)
- [ ] Backed up the guide with a dated filename
- [ ] Backed up `agent_memory.db` if touching memory
- [ ] Code change made and tested first (if applicable)
- [ ] Guide edited with headers intact; 27 sections present
- [ ] `CHANGE_LOG.txt` updated
- [ ] Section memories rebuilt (full or surgical)
- [ ] Aux memories preserved (residents, sop, test, skill_triggers, installer, deployment, frontmatter, documentation_locations)
- [ ] Verification passed (memorystats, test query, off-topic query)
- [ ] Checklist, map, todo updated if sections changed
- [ ] Human views regenerated or noted in TODO

## Related documents

- `C:/ai/updated_docs/00_READ_FIRST_documentation_sop.txt` — the original SOP (source of this skill).
- `C:/ai/skills/library/meta/adding_skills/SKILL.md` — how to register a skill.
- `C:/ai/updated_docs/master_feature_guide.txt` — the guide itself.
- `C:/ai/populate_skill_triggers.py` — the registration script.