voice_switching/
================

Purpose
-------
Two scripts that demonstrate Free Agent driving a web page via screen
coordinates and accessibility scanning:

  list_voices.py    - scan the Speechma voice list and print voice names
  select_voice.py   - find a named voice in the Speechma page and click it

Together they show a complete loop: scroll to a target area of a web page,
scan the page for labels, and act on what was found. That is the core
pattern Free Agent uses for any web UI it has not been given an API for.

What this demonstrates
----------------------
- Coordinate-based clicking via desk_executor_seq.py
- Accessibility-tree scanning via desktop_scanner_optimized.py
- Extracting structured data (voice names, bounding boxes) from a scan
- Chaining multiple actions into a sequence with subprocess calls

Requirements
------------
- Free Agent installed at C:/ai (this pair depends on Free Agent's
automation scripts to run)
- Firefox open, Speechma loaded, window maximised
- The Speechma page must be in the voice-selection view before either
script runs. Neither script navigates to the page for you.
- Python 3.6+ in PATH as "python"

What "standalone" means here
-----------------------------
These scripts are NOT standalone utilities. They are Free Agent automation
examples. They depend on Free Agent's automation tree:

  C:/ai/automation/core/desk_executor_seq.py
  C:/ai/automation/core/desktop_scanner_optimized.py

If a user receives this pair without Free Agent installed, the scripts
cannot run. If they have Free Agent, they can run them as-is (subject to
the machine assumptions below).

Usage - list_voices.py
----------------------
    python list_voices.py

Scrolls the Speechma page to the voice-list area, runs a fast scan, filters
out common UI elements, and prints voice names found. No arguments.

Usage - select_voice.py
-----------------------
    python select_voice.py "Andrew Multilingual"

Scans for a label matching the argument (case-insensitive), extracts the
bounding box, and clicks the centre of it. Exits 1 if no match is found.

Machine assumptions (change these on a different machine)
---------------------------------------------------------
Both scripts have a block at the top marked:

    # --- Machine-specific constants (edit for your environment) ---

Values to check before running on a new machine:

  BROWSER_TARGET   currently 'firefox.exe,SPEECHMA'
                   change the process name to match your browser

  SCROLL_TOP       '1909, 129'    click 5x to scroll to top
  SCROLL_DOWN_1    '1909, 1058'   click once
  SCROLL_DOWN_2    '1909, 1072'   click 3x
                   these pixel coordinates assume a 1920x1080 display
                   with the browser maximised. Change them for other
                   resolutions, or if the browser window is not maximised.

  VOICE_AREA_Y_MIN / _MAX   currently 300 / 800 (list_voices.py only)
                   the vertical band of the page where voice labels are
                   expected. Change if your page layout is different.

  DESK_EXECUTOR    path to Free Agent's sequence executor
  DESK_SCANNER     path to Free Agent's scanner
                   if Free Agent is installed somewhere other than C:/ai,
                   change these paths in both scripts.

  TEMP_SEQ, VERIFY_SCAN, OUTPUT_SCAN, SELECT_SCAN, CLICK_SEQ
                   temporary JSON files. Keep them somewhere writable.
                   Default is C:/ai/, which exists on any Free Agent install.

Output
------
list_voices.py prints a numbered list of voice names, or "No voice names
found." and exits 0 either way.

select_voice.py prints progress, the found coordinates, and either
"[DONE] Voice selection complete." on success or "[FAIL] Voice selection
failed." with exit 1 on failure.

Exit codes
----------
    0   Success
    1   Failure (missing voice, scan failed, click failed, missing arg)

Limitations
-----------
- Brittle. Depends on Speechma's current page layout. If Speechma changes
  its voice list, the scroll coordinates and voice-area bounds may need
  updating.
- Screen resolution-specific. The pixel coordinates are not computed at
  runtime; they are hardcoded for 1920x1080 or larger.
- Depends on Free Agent. See "What standalone means here" above.
- No retry logic. A single transient scan or click failure is fatal.

See also
--------
- setup.txt  quick start and deployment notes for installing on
            another machine
