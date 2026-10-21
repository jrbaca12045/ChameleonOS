#!/usr/bin/env python3
"""
Act on a Windows UI control: click it, type into it, or read its text.

Part of the ui_automation/ example. See README.txt for details.

Usage:
    python ui_action.py <PID-or-title> <action> <control_id> [value]

Actions:
    click       Click the control.
    type        Clear the control and type the value into it.
    set_value   Same as type.
    set_text    Same as type.
    get_text    Read the control's text and print it.

The control_id is looked up three ways, in order:
    1. As an auto_id (the automation id attribute)
    2. As an exact title/name
    3. As a case-insensitive regex against the control's name

Requires:
    pip install pywinauto

Windows-only. Uses pywinauto's UIA backend, with a win32 fallback.
Outputs JSON to stdout. Always exits 0; errors appear as {"error": "..."}.
"""
import json, sys, time
from pywinauto import Application
import pywinauto.keyboard as kbd

def get_app(target, backend='uia'):
    try:
        if target.isdigit():
            return Application(backend=backend).connect(process=int(target), timeout=5)
        else:
            return Application(backend=backend).connect(title=target, timeout=5)
    except:
        try:
            return Application(backend='win32').connect(title=target, timeout=5)
        except:
            return None

def find_control(win, ctrl_id):
    try:
        ctrl = win.child_window(auto_id=ctrl_id)
        if ctrl.exists(timeout=2):
            return ctrl
    except:
        pass
    try:
        ctrl = win.child_window(title=ctrl_id)
        if ctrl.exists(timeout=2):
            return ctrl
    except:
        pass
    try:
        import re
        pattern = re.compile(ctrl_id, re.I)
        for c in win.descendants():
            try:
                nm = c.element_info.name or ''
                if pattern.search(nm) and c.exists(timeout=0.5):
                    return c
            except:
                pass
    except:
        pass
    return None

def run_action():
    if len(sys.argv) < 4:
        print(json.dumps({"error": "Usage: ui_action.py <PID/Title> <action> <control_id> [value]"}))
        return
    target, action, ctrl_id = sys.argv[1], sys.argv[2], sys.argv[3]
    value = sys.argv[4] if len(sys.argv) > 4 else ""
    try:
        app = get_app(target)
        if not app:
            print(json.dumps({"error": "Process not found"}))
            return
        win = app.top_window()
        time.sleep(0.3)
        ctrl = find_control(win, ctrl_id)
        if not ctrl or not ctrl.exists(timeout=1):
            print(json.dumps({"error": "Control '" + ctrl_id + "' not found"}))
            return
        if action == "click":
            ctrl.click_input()
            time.sleep(0.2)
            print(json.dumps({"status": "clicked", "control": ctrl_id}))
        elif action in ["type", "set_value", "set_text"]:
            ctrl.set_focus()
            time.sleep(0.1)
            kbd.send_keys('^a{BACKSPACE}', with_spaces=True)
            time.sleep(0.1)
            kbd.send_keys(value, with_spaces=True, with_tabs=True)
            print(json.dumps({"status": "typed", "control": ctrl_id, "value": value}))
        elif action == "get_text":
            txt = ""
            try:
                txt = ctrl.window_text() or ctrl.texts()[-1] if ctrl.texts() else ""
            except:
                try:
                    txt = ctrl.get_value()
                except:
                    txt = str(ctrl)
            print(json.dumps({"status": "success", "text": str(txt).strip()}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    run_action()
