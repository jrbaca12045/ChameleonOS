mouse_coordinates/
===================

Purpose
-------
A small always-on-top window that shows the current mouse position,
updating in real time. Intended for anyone who needs to know the pixel
coordinates of something on screen — usually just before writing
coordinate-based automation.

This is an interactive tool, not a script. You launch it, it opens a
window, and it runs until you close the window. It does not print a
result and exit.

What this demonstrates
----------------------
- Reading live mouse position with pyautogui.position()
- Building a minimal always-on-top Tk window with a custom drag handle
- Simple state handling (drag start, drag move, reset, close)
- Cross-platform behavior: pyautogui.position and tkinter both work
  on Windows, macOS, and Linux with no per-platform code

Requirements
------------
- Python 3.6 or later.
- pip install pyautogui
- Tkinter, which ships with standard CPython on Windows and macOS.
  On Linux, if tkinter is missing: sudo apt install python3-tk
  (or the equivalent for your distribution).

Cross-platform note: unlike some of the other tools in this archive,
this one genuinely runs on all three major platforms. The pyautogui
position call is cross-platform. The Tk window is cross-platform. The
only platform-specific caveat is macOS accessibility permission —
see Deployment Notes.

Usage
-----
    python mouse.py

A small window appears in the top-right corner of the screen showing
the current mouse position as X, Y. Move the mouse anywhere on the
desktop and the numbers update.

Interacting with the window:

  - Click and drag the left-side handle to move the window.
  - Double-click the handle to snap it back to the top-right corner.
  - Click anywhere on the window to close it.
  - Right-click anywhere on the window to close it.

The window is always-on-top, so it stays visible over other windows.
That is the whole point — you need to see the coordinates while the
target application has focus.

Output
------
The window itself is the output. There is no printed output besides the
startup banner that describes the controls.

There is no exit code other than the process ending when the window
closes. The window close sets a flag, the update loop stops, the tkinter
mainloop returns, the process exits with status 0.

What about the drag handle?
---------------------------
The left-side handle is rendered as two ASCII colons (::) inside a dark
grey box. This is intentional. Some of the original internal versions
of this tool used a braille character for the handle, which looks more
decorative but does not render reliably on older Windows builds or
under some console code pages. The ASCII colons render everywhere.

Use cases
---------
1. You are writing a coordinate-based automation script (like the
   voice_switching examples) and need to know where on screen a
   specific button appears. Run mouse.py, hover over the button, read
   the coordinates, use them in your script.

2. You are diagnosing an automation script that clicks the wrong
   place. Run mouse.py, watch the actual cursor position it reports,
   compare to what your script is sending.

3. You are capturing a screenshot for documentation and want to note
   the exact coordinates of interesting regions.

Limitations
-----------
- Shows position in screen pixels. Does not show which window the
  cursor is over, which element the cursor is over, or DPI scaling.
- On macOS, pyautogui.position may require the terminal or IDE to have
  Accessibility permission (System Settings > Privacy & Security >
  Accessibility). If the coordinates read as 0,0 always, this is why.
- On Linux, requires an X11 session. Wayland's security model prevents
  global mouse position reads by default. If the numbers stay at 0,0,
  this is why.
- The window position is recomputed against the primary monitor width
  only. On multi-monitor setups, the window appears on the primary
  monitor's top-right, not necessarily where the mouse is.

See also
--------
- setup.txt  quick start and deployment notes for installing on
            another machine
