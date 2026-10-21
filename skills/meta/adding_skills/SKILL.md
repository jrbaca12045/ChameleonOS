---
name: adding_skills
description: "Create a new skill and register it in memory so it surfaces by trigger. Covers finding an existing skill first, writing SKILL.md with correct frontmatter, choosing triggers that do not collide, running the population script, and verifying the memory was created. Use when adding a skill, creating a skill, writing a new skill, registering a skill, adding to the skill library, or growing the skill set."
triggers: adding a skill, create a skill, creating a skill, new skill, write a skill, writing a skill, register a skill, add to the skill library, growing the skill library, skill authoring
---

# Adding Skills

A skill is a folder with a `SKILL.md` file. It becomes discoverable by a System memory whose trigger keywords fire when the user asks for it. This procedure covers the whole loop: finding whether the skill already exists, writing it, registering it, and proving it works.

Two layers, cheap first, expensive second. The trigger memory brings the description and path into context. The full `SKILL.md` is opened only when the skill actually fires. You are adding a row to the first layer and a file to the second.

## Step 0: Find before you build

Always run this step first. Writing a skill that already exists creates a collision and the wrong one fires.

- Read `C:/ai/skills/library/meta/finding_skills/SKILL.md` and follow it.
- Search the memory: `{"command":"memoryrecall","query":"<what the skill does>","top_k":"5"}`. If a close match comes back, read its `SKILL.md` before deciding to duplicate.
- Search the filesystem: `{"command":"dir","path":"C:/ai/skills/library","pattern":"SKILL.md"}`.

If a skill already covers this, extend it instead of adding a new one. Two skills that do the same thing is a collision waiting to happen.

## Step 1: Choose the location

Skills live under `C:/ai/skills/library/<category>/<skill_name>/SKILL.md`. Categories are broad buckets, not rules. Existing examples: `meta` for skills about the system itself, `writing` for text work, `sales` for sales work.

- One folder per skill.
- Folder name and frontmatter `name` should match, in `snake_case`.
- The script uses the frontmatter `name` if present, else the folder name. Keep them the same so you are not surprised later.

## Step 2: Write the frontmatter

Every `SKILL.md` starts with YAML frontmatter between two `---` lines.

Required:
- `name` - the skill name in snake_case.
- `description` - one or two sentences. Its `Use when ...` clause is what the trigger extractor parses, so write it carefully.

Optional:
- `triggers` - a comma-separated override. If present, it replaces the auto-extracted triggers for this skill.

Example of the minimum:

```
---
name: proofreading
description: "Identify grammar, logical, and flow errors in text and suggest targeted fixes. Use when proofreading content, checking writing quality, or reviewing a draft."
---
```

The description's `Use when` clause is parsed like this: split on commas, split on the word `or`, trim each fragment, drop single generic words (content, text, writing, document, task, use, when, the, and, or, a, an), then prepend the skill name with underscores turned into spaces. Everything else becomes a trigger phrase.

## Step 3: Write triggers that do not collide

Triggers are comma-separated phrases. Commas separate triggers. Spaces stay inside a phrase.

Correct:

```
triggers: proofreading, check grammar, review draft, copyedit
```

Wrong - spaces used as separators, the phrase is lost:

```
triggers: proofreading check grammar review draft copyedit
```

Rules that keep triggers from colliding:

- Do not claim a single generic word as a trigger. `writing`, `content`, `text`, `document` will all be claimed by something else.
- Prefer distinctive two-word or three-word phrases over single words.
- Include the skill name as a trigger. The extractor does this automatically; if you write an override, include it yourself.
- If a phrase is already claimed by another skill, either drop it or make it more specific.

The population script reports collisions. Read that report. A collision means two skills both fire on the same phrase and one will lose silently.

## Step 4: Write the body

The body is the procedure the model follows when the skill fires. It is not shown to the user unless the model chooses to. Structure it however the task needs. What works in this library:

- A one-sentence statement of what the skill does.
- The inputs it expects.
- The steps in order, each concrete enough to act on.
- Examples where the distinction between good and bad output matters.
- A checklist at the end if the task has many failure modes.

Keep it plain. No emoji. No marketing voice. Assume the reader is a model that will act on it, not a human who will admire it.

## Step 5: Register the skill in memory

A skill file on disk is invisible until a System memory points at it. Run the population script.

Always dry-run first. It shows the extracted triggers before anything is written.

```
python C:/ai/populate_skill_triggers.py --dry-run
```

Read the output. Check two things:

1. The `keywords=` line for your new skill. Are the extracted triggers sensible? If they are awkward, fix the description's `Use when` clause or add a `triggers:` override in the frontmatter, then dry-run again.
2. The collision report. If your new skill collides with another, fix the triggers before going live.

When the dry-run looks right, run it for real:

```
python C:/ai/populate_skill_triggers.py
```

The script will report `[OK] <name>` for the new skill. If it reports `[FAIL]`, read the stderr it prints and fix the cause before retrying.

## Step 6: Verify the memory exists

Reading the script output is not proof. Check the database.

Recall test. Ask for the skill the way a user would:

```
{"command":"memoryrecall","query":"<a phrase your trigger should match>","top_k":"5"}
```

The new memory should come back with `SKILL: <name> - <description>. Full procedure at <path>.`

Direct database check if recall is ambiguous:

```
import sqlite3
con = sqlite3.connect(r'C:/ai/agent_memory.db')
r = con.execute("SELECT id, trigger_keywords FROM memories WHERE content LIKE 'SKILL: <name> %'").fetchone()
print(r)
```

If no row comes back, the memory was not written. Re-run the populate script and read its output for the failure.

## Step 7: Test the trigger end to end
The trigger is not proven until it fires. Say a phrase a user would say when they want this skill, and check whether the skill memory surfaces in context. A passing recall test in Step 6 is not the same thing as a passing trigger test, because trigger matching runs through the two-stage gate described in the memory reference: the phrase must match the keyword list, and the query embedding must be at least 0.65 similar to the trigger embedding.The last check is behavioral. Say a phrase that should fire the skill and see whether it surfaces. If the trigger does not fire, either the phrase is not in the keyword list or the semantic gate rejected it. Add the phrase to the `triggers:` override and re-run the population script.

## What happens when a skill is removed

When a skill file is deleted from the library, the next population run deletes its memory and logs the deletion to `C:/ai/logs/skill_memory_deletions.log`. The log contains the full content and keywords, so an accidental deletion is recoverable by re-promoting from the log.

If a skill file is moved rather than deleted, the script cannot tell the difference. The memory is deleted. Move the file back or fix the path, then re-run to restore.

## Checklist

- [ ] Searched memory and filesystem; no existing skill covers this
- [ ] Folder created at `C:/ai/skills/library/<category>/<skill_name>/`
- [ ] `SKILL.md` written with `name` and `description` frontmatter
- [ ] Description has a clear `Use when` clause, or a `triggers:` override was written
- [ ] Triggers are comma-separated phrases, not space-separated words
- [ ] No trigger claimed by another skill
- [ ] Dry-run showed sensible keywords and no collisions
- [ ] Live run reported `[OK]` for the new skill
- [ ] `memoryrecall` returns the new skill memory
- [ ] A spoken trigger phrase actually fires the skill

## Related documents

- `C:/ai/skills/library/meta/finding_skills/SKILL.md` - the search procedure this skill starts with.
- `C:/ai/populate_skill_triggers.py` - the script that writes and deletes skill memories.
- `C:/ai/logs/skill_memory_deletions.log` - receipts for every deleted skill memory.