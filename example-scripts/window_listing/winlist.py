#!/usr/bin/env python3
"""
Enumerate visible windows on Windows, showing PID, process name, and title.

Part of the window_listing/ example. See README.txt for details.

Usage:
    python winlist.py

Requires:
    pip install pywinauto psutil

Windows-only. Uses pywinauto's UIA backend.
"""
import os
import sys

try:
    import psutil
    from pywinauto import Desktop
except ImportError as e:
    print("[FAIL] Missing dependency: " + str(e))
    print("       Run: pip install pywinauto psutil")
    sys.exit(1)

def list_all_windows():
    print("{:<8} | {:<20} | {}".format('PID', 'Process Name', 'Window Title'))
    print("-" * 60)

    my_pid = os.getpid()
    windows = Desktop(backend="uia").windows()

    for w in windows:
        title = w.window_text()
        if title:
            try:
                pid = w.process_id()
                proc_name = psutil.Process(pid).name()
                if pid == my_pid:
                    continue
                safe_title = title.encode('ascii', 'ignore').decode('ascii')
                print("{:<8} | {:<20} | {}".format(pid, proc_name, safe_title))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print("{:<8} | {:<20} | {}".format('N/A', 'Unknown', 'Unknown'))

if __name__ == "__main__":
    list_all_windows()
