---
name: gui_automation_loop
description: "Build a reliable GUI automation for any Windows app using the sequence path. Teaches the four-phase shape: preamble (dismiss popups, verify the app), orient (scan, find a starting point), loop (act, re-scan, diff, check three stop conditions), and report (save results). Covers the two layers, executor and orchestrator, and the pitfalls that silently break automation. Use when automating an app, writing a script to click through a UI, scraping a chat or list, building a multi-step GUI workflow, or driving an app that has no API."
triggers: automate this app, automate an app, automate the ui, gui automation, write an automation script, click through, scrape a chat, scrape a list, multi step automation, drive an app, automation loop, scroll and capture, app automation, build an automation, automation script
---

# GUI Automation Loop

How to build a reliable automation for any Windows app using the sequence path. The Facebook chat script is the worked example throughout — it is a proven, working automation and the pattern it follows is the pattern this skill teaches.

## The two layers

Every automation has two layers. They do different jobs and it is a mistake to confuse them.

**Layer one: the step executor.** A tool that runs one sequence of actions against one window. `desk_executor_seq` is the one used throughout. It takes a sequence JSON, a target window, and a scan file, and it performs the clicks, types, and scrolls in order. It handles one pass and exits.

**Layer two: the orchestrator.** A Python script you write. It calls the executor in a loop, with preambles, verifications, stop conditions, and a report. It holds the state — what has been collected, how many scrolls, whether the target has been reached. It decides when to stop.

The executor is a tool. The orchestrator is the script. The Facebook automation is an orchestrator; `desk_executor_seq` is the executor it calls.

## The four-phase shape

Every reliable automation follows the same shape. The Facebook script is a clean example of all four phases.

### Phase 0 — Preamble

Before touching the target, make sure nothing is in the way and the target is actually running.

- **Dismiss popups first.** A popup blocks every action underneath it, silently. `C:/ai/automation/facebook/dismiss_facebook_popup.py` is the worked example: it scans with `desktop_scanner_vision`, detects the overlay by native pattern and then by vision description, locates the dismiss button inside the overlay's bounding box, clicks it through `desk_executor_seq`, and re-scans to verify it is gone. Read that file before writing a preamble of your own.
- **Verify the target is running.** Call `winlist` and check that the process name appears. If it does not, stop and say so. Do not scan a window that is not there.

### Phase 1 — Orient

Get to a known starting state before the loop begins.

- **Scan the window** with `desktop_scanner_fast`, saving to a known scan file.
- **Check the state** with a small helper script if the app has modes (chat open or closed, list at top or scrolled). The Facebook script calls `check_chat_status.py` and opens the chat if it is closed.
- **Navigate to a known point.** If the app has a 'go to latest' or 'go to top' control, use it. The Facebook script checks for it with `check_most_recent.py` and clicks it with `go_to_latest_click.py`.

### Phase 2 — The loop

This is the core. Each iteration:

1. **Act.** Run the executor against a sequence file — one scroll, one click, one batch of actions.
2. **Re-scan.** Scan the window again and save to the same path.
3. **Extract.** Pull the new data out of the scan.
4. **Diff.** Add only what is new to the accumulator. Count how many were added.
5. **Check stop conditions.** See below.

### Phase 3 — Report

Save everything at the end, in a structured form. The Facebook script writes `last_2_days_report.json` with the date, the counts, the scrolls performed, and every message. Interruption does not mean loss.

## The three stop conditions

Every loop needs all three. Missing any one of them causes a different failure.

**One: a hard maximum.** `MAX_SCROLLS = 100`. A safety net. If the other two conditions never fire, this one stops the loop eventually. Without it, a bug in the stop logic runs forever.

**Two: consecutive empty iterations.** `EMPTY_SCAN_LIMIT = 3`. Three iterations in a row that add nothing means you have reached the beginning of the data. Without it, the loop stops on the first UI lag and misses half the content.

**Three: the target reached.** The Facebook script checks `has_yesterday and has_older` — the actual thing it came for. Without it, the loop scrolls past the target and keeps going.

The three are not alternatives. They are the three ways a loop can correctly stop, and every one of them is needed.

## The pitfalls that silently break automation

These are from the definitive automation guide. They apply to every automation built this way.

| Pitfall | Solution |
|---|---|
| Using `pyautogui` directly | Always use `desk_executor_seq` for UI actions. Never call `pyautogui` in the orchestrator. |
| Hardcoding coordinates | Calculate from the current scan's bounding box. Never hardcode a click point. |
| Not saving state | Save `scroll_count`, the accumulated data, and flags. Interruption must not mean loss. |
| No max iterations | Always include `MAX_SCROLLS` or `MAX_RETRIES`. |
| Ignoring Unicode errors | Clean with `re.sub(r'[^\x00-\x7F]+', '', text)` or encode with `errors='replace'`. |
| Wrong prompt format | Always use `process.exe,WindowTitle` in the scan prompt. |
| Not checking the scan exists | Check `os.path.exists()` before loading. |
| One-shot scroll too short | Use several scroll actions per iteration in one sequence file. |
| Premature stop on empty scan | Wait for N consecutive empty scans before stopping. |
| Not verifying popup dismissal | Re-scan after clicking dismiss. |
| Not using vision for popups | Supplement native controls with `vision_description`. |
| Ignoring return codes | Check `result.returncode` on every subprocess call. |
| Not handling timeouts | Set a `timeout` on every subprocess call. |

## Which executor to use

There are two executors and one editor. One is the general tool, one is the specialist, and one is the editor that builds what they run.

| Tool | What it is | When to use it |
|---|---|---|
| `run_sequence` | The general executor. Finds the window itself, scans, and runs every step. Supports fifteen action types including `detect_icon`, `click_at_anchor`, and the hover family. Accepts `--fast` and variable overrides. Retries a failed step once after a re-scan. | **The default.** Use it unless you have a specific reason not to. It is the one tool that does the whole job from start to finish. |
| `desk_executor_seq` | The specialist. Takes a sequence, a scan file you have already made, and a target window. Executes the steps. Simpler and faster because it does not scan. | When you already have a scan and want to reuse it, or when you are inside an orchestrator that scans on its own schedule. The Facebook script uses this one. |
| `automation_manager` | The editor. A GUI tool for turning a recording into a sequence. | When you need to build or edit a sequence. Not called by the model. Opened by the user. |

`run_sequence` is the culmination of the automation work. It absorbed the useful parts of the earlier tools and became the general one. The others still have their niches, but `run_sequence` is the tool that takes the cake. Reach for it first.

## Building a sequence from scratch

If no sequence exists yet, the workflow is record, edit, run.

**1. Record.** Run `python C:/ai/recording_studio.py`. Click Record, perform the actions you want to automate, click Stop, and name the project. The recording lands in `C:/ai/recordings/<name>/` as `events.json` with screenshots alongside.

**2. Edit.** Run `python C:/ai/automation_manager.py`. It opens a GUI. Load the recording from `C:/ai/recordings/`, translate the events into a first-pass sequence, then refine each step: change a click to a click-by-label, add a wait, reorder, delete a step that is not needed. Save the result as `translated_sequence.json`.

**3. Run.** Execute the sequence with `run_sequence`:

```
python C:/ai/automation/core/run_sequence.py C:/ai/recordings/<name>/translated_sequence.json
```

Or through the inventory: `automation_run | run_sequence | prompt=C:/ai/recordings/<name>/translated_sequence.json`.

**Telling the user how to use the editor.** When a user asks how to build an automation, describe it in that order: record with `recording_studio.py`, open `automation_manager.py` to translate and edit, save `translated_sequence.json`, run it with `run_sequence`. The editor is a GUI the user drives; the model does not call it.

## The worked example

The Facebook chat automation is the full pattern in one file:

`C:/ai/automation/facebook/scripts/get_pampered_2days_with_popup_detection.py`

Read it before writing an automation of your own. Every phase is present: PHASE 0 dismisses popups, PHASE 1 verifies Facebook is running, PHASE 2 scans, PHASE 3 checks the chat state, PHASE 5 calculates safe coordinates, PHASE 8 is the loop. The three stop conditions are at the top as `MAX_SCROLLS`, `EMPTY_SCAN_LIMIT`, and the `has_yesterday and has_older` check.

The popup dismisser it depends on is at:

`C:/ai/automation/facebook/dismiss_facebook_popup.py`

And the executor it calls is at:

`C:/ai/automation/core/desk_executor_seq.py`

The general-purpose runner, which supports more action types including `detect_icon`, `click_at_anchor`, and the hover family, is at:

`C:/ai/automation/core/run_sequence.py`

## When the sequence path is the right choice

Use this path when:

- You have a recording, or you can build a sequence by hand.
- The app exposes stable labels, or you have a scan to work from.
- The task is a repeated loop — scroll and collect, click through a list, fill a form repeatedly.
- You want it to run through the existing pipeline tools with the existing scan files.

## When CUA is the better choice

The CUA path (see the `computer_use` skill) is the alternative. Use it when:

- The app has a rich accessibility tree and you want element-index precision.
- You are doing a one-off task that does not justify building a sequence.
- The sequence path fails — labels changed, layout shifted, or the control is not reachable by bounding box.

The two paths can be combined in the same script. Try one, verify, and if it fails try the other. That is a separate skill and a separate decision.

## Related

- `C:/ai/skills/library/automation/computer_use/SKILL.md` — the CUA path, for the alternative execution method.
- `C:/ai/updated_docs/master_feature_guide.txt` — Section 23 covers the Python tool layer in full.
- `C:/ai/updated_docs/AUTOMATION_PIPELINE_DOCUMENTATION.txt` — the pipeline documentation.
- `C:/ai/aispace/automation_inventory.json` — the live registry of every automation tool.