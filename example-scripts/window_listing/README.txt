window_listing/
================

Purpose
-------
Print a table of every visible window on Windows: PID, process name,
and window title. Useful for finding the exact process name of a window
you want to automate, or for seeing what is running on the desktop.

What this demonstrates
----------------------
- Using pywinauto's UIA (UI Automation) backend to enumerate windows
- Cross-referencing window handles to processes via psutil
- Handling windows whose owning process has closed or is protected
  (AccessDenied) without crashing the enumeration
- ASCII-sanitising window titles, which can contain non-ASCII characters

Requirements
------------
- Windows. This uses pywinauto's UIA backend, which is Windows-only.
  It will not run on macOS or Linux.
- Python 3.6 or later.
- pip install pywinauto psutil

Usage
-----
    python winlist.py

No arguments. Prints a table and exits.

Output
------
    PID      | Process Name         | Window Title
    ------------------------------------------------------------
    1234     | firefox              | Google - Mozilla Firefox
    5678     | Code                 | Visual Studio Code
    9012     | chrome               | New Tab - Google Chrome
    ...

Column widths are fixed at 8 and 20 characters, with the title as the
remaining width. Long titles are not truncated, so the table may wrap
on narrow consoles.

Exit codes
----------
    0   Success. Windows enumerated.
    1   Missing dependency (pywinauto or psutil not installed).

No other failure mode exits non-zero. Individual window lookup errors
(process closed, access denied) are caught per-window and printed as
"Unknown" without aborting the whole listing.

Limitations
-----------
- Windows-only. See Requirements above.
- Titles with non-ASCII characters are stripped to their ASCII subset.
  A title like "<unicode>.txt - Notepad" becomes " .txt - Notepad".
  That is intentional; printing raw unicode to a Windows console risks
  a UnicodeEncodeError on default code pages.
- The script's own process is excluded from the output.
- Does not filter by visibility state. pywinauto's Desktop.windows()
  returns windows that are considered part of the desktop, but does
  not distinguish minimised windows from hidden ones. Some entries
  may have empty titles and are skipped.

Why this might be useful outside Free Agent
-------------------------------------------
If you are writing any desktop automation, this is the fastest way to
find the (process_name, window_title) pair that your automation tool
will need to target a window. Run winlist.py, find your target in the
table, and use its process name.

See also
--------
- setup.txt  quick start and deployment notes for installing on
            another machine
