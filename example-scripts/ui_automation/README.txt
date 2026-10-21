ui_automation/
===============

Purpose
-------
Three small scripts that together demonstrate the fundamental loop of
Windows UI automation: inspect a window, wait for a control to be ready,
and act on that control. Each script is focused on one verb. Used in
sequence, they let you automate any Windows application that exposes
its controls through UI Automation or MSAA.

The three scripts
-----------------

  ui_inspect.py   Dump the control tree of a window as JSON.
  ui_wait.py      Wait for a specific control to reach a specific state.
  ui_action.py    Click, type into, or read text from a control.

Each script takes its target as a CLI argument and emits JSON to stdout.
None of them have hardcoded targets, coordinates, or paths. All three
use pywinauto. None of them depend on Free Agent being installed.

The workflow
------------
The typical loop is:

  1. Inspect:  which controls does this window have?
  2. Wait:     is the control I want ready yet?
  3. Act:      click it, type into it, or read from it.
  4. Verify:   read the control back to confirm the action took effect.

Worked example - Notepad
------------------------
Open Notepad on Windows. The window title is "Untitled - Notepad".
The main text area has auto_id "15" in most Windows versions.

Step 1. Inspect the window's controls:

    python ui_inspect.py "Untitled - Notepad"

This prints JSON with a controls array. Look for entries where
type is "Edit" and auto_id is "15" - that is the main text area.

Step 2. Wait for the text area to be ready:

    python ui_wait.py "Untitled - Notepad" 15 enabled

Returns status success with elapsed seconds if the text area is ready.

Step 3. Type into the text area:

    python ui_action.py "Untitled - Notepad" type 15 "Hello from three scripts."

Returns status typed with the control and value echoed back.

Step 4. Read it back to verify:

    python ui_action.py "Untitled - Notepad" get_text 15

Returns status success with the text field containing what you typed.

Four commands. Inspect, wait, act, verify. That is the whole loop.

Each script in detail
---------------------

ui_inspect.py <title-or-PID>
    If the argument is all digits, it is treated as a process ID.
    Otherwise it is treated as a title substring (case-insensitive).
    Output includes: the matched window title, which backend produced
    the result (uia or win32), and an array of all descendant controls
    with their type, name, and auto_id.

    Backend fallback: tries uia first, falls back to win32 if uia finds
    nothing. Some controls are only visible through win32.

ui_wait.py <target> <control_id> <condition> [timeout] [value]
    Waits until the control reaches the condition or the timeout expires.
    Default timeout is 10 seconds. Polls every 200ms.

    Conditions:
      visible         the control exists
      enabled         the control exists and is interactive
      text_contains   the control's text contains value (case-insensitive)
      disabled        the control exists and is not interactive
      not_visible     the control no longer exists

    Success output: status success, condition, elapsed
    Timeout output: status timeout, condition, timeout

ui_action.py <target> <action> <control_id> [value]
    Actions: click, type (also set_value and set_text), get_text.

    click       Sends a real mouse click to the control
    type        Focuses the control, clears it, then types the value
    get_text    Reads the control's text

    Success output: status clicked, typed, or success, plus fields

Control lookup order (all three scripts)
----------------------------------------
When a control_id is passed, each script looks it up in this order:

  1. As an auto_id (the automation id attribute). Fastest, most reliable.
  2. As an exact title or name.
  3. As a case-insensitive regex against the control's name.

If you have the auto_id, prefer it. If you only know the visible label,
pass that. If you have a pattern, pass a regex.

How to find the auto_id
-----------------------
Run ui_inspect.py against your target window. Each control in the output
has an auto_id field. That is what you pass to ui_wait.py and ui_action.py.

If the control has an empty auto_id, use its name field instead (the
script will try name match after auto_id). If both are empty, use a
regex against the name pattern you see in the accessibility tree.

Output format differences
-------------------------
All three scripts emit JSON, but the schemas are not identical:

  ui_inspect   query, window, backend, controls array
  ui_wait      status success with condition and elapsed, or status
               timeout with condition and timeout, or error
  ui_action    status clicked or typed or success, plus fields, or error

If you are chaining these in a shell script, parse the status field:
"success", "clicked", "typed" all indicate success; "timeout" and
"error" indicate problems. None of the scripts exit non-zero on failure;
the outcome is always in the JSON.

Requirements
------------
- Windows. pywinauto uses Windows UI Automation / MSAA.
- Python 3.6 or later.
- pip install pywinauto

No other dependencies. No Free Agent dependency. No hardcoded paths.

Limitations
-----------
- Windows-only.
- Controls exposed only through unusual accessibility providers may not
  be found by either uia or win32 backend. This is rare but real.
- ui_action's type action clears the field first (ctrl+a, backspace)
  before typing. It does not append. If you need to append, read the
  current text first, concatenate, then set.
- No right-click, drag, or scroll actions. Only click, type, and read.
  Adding more actions is a small extension: pass the action name, add
  a branch, call the corresponding pywinauto method.
- The three scripts do not handle multi-window applications gracefully.
  app.top_window() picks the topmost window of the application, which
  may not be the window you want on multi-window apps. Pass a title
  substring instead of a PID if that happens.

What these demonstrate
----------------------
Windows UI automation reduces to three moves: inspect the tree, wait
for state, act on the control. These three scripts are the smallest
form of that loop. The voice_switching/ cluster uses the same underlying
pattern at a higher level: it just replaces the pywinauto control calls
with screen-coordinate clicks. Both are valid; pywinauto is more
precise when controls are exposed, screen coordinates are more general
when they are not.

See also
--------
- setup.txt                quick start and deployment notes
- ../window_listing/       discover which windows exist on the desktop
- ../voice_switching/      automation via screen coordinates
