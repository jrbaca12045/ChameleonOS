#!/usr/bin/env python3
"""
Wait for a Windows UI control to reach a specific state.

Part of the ui_automation/ example. See README.txt for details.

Usage:
    python ui_wait.py <target> <control_id> <condition> [timeout] [value]

Conditions:
    visible         Wait until the control exists and is visible
    enabled         Wait until the control exists and is enabled
    text_contains   Wait until the control text contains the value
    disabled        Wait until the control exists and is not enabled
    not_visible     Wait until the control no longer exists

Default timeout is 10 seconds. Polls every 200ms. On success prints
JSON with status=success and elapsed seconds. On timeout prints
JSON with status=timeout. Never exits non-zero.

Requires:
    pip install pywinauto

Windows-only. Uses pywinauto's UIA backend.
"""
import json, sys, time, re
from pywinauto import Application

def wait_for_control(target, control_id, condition, timeout=10, value=""):
    try:
        if target.isdigit():
            app = Application(backend='uia').connect(process=int(target), timeout=2)
        else:
            app = Application(backend='uia').connect(title=target, timeout=2)
    except:
        try:
            app = Application(backend='uia').connect(title=target, timeout=2)
        except:
            return json.dumps({"error": "App not found"})

    win = app.top_window()
    start = time.time()

    ctrl = None
    try:
        ctrl = win.child_window(auto_id=control_id)
    except:
        pass
    if not ctrl or not ctrl.exists(timeout=0.5):
        try:
            ctrl = win.child_window(title=control_id)
        except:
            pass
    if not ctrl or not ctrl.exists(timeout=0.5):
        try:
            pat = re.compile(control_id, re.I)
            for c in win.descendants():
                try:
                    if c.exists(0.2) and c.element_info.name and pat.search(c.element_info.name):
                        ctrl = c
                        break
                except:
                    pass
        except:
            pass

    if not ctrl:
        return json.dumps({"error": "Control " + control_id + " not found initially"})

    while time.time() - start < timeout:
        try:
            exists = ctrl.exists(timeout=0.5)
            if condition == "visible":
                if exists:
                    return json.dumps({"status": "success", "condition": condition, "elapsed": round(time.time()-start, 2)})
            elif condition == "enabled":
                if exists and ctrl.is_enabled():
                    return json.dumps({"status": "success", "condition": condition, "elapsed": round(time.time()-start, 2)})
            elif condition == "text_contains":
                txt = ctrl.window_text() or ""
                if exists and value.lower() in txt.lower():
                    return json.dumps({"status": "success", "condition": condition, "elapsed": round(time.time()-start, 2)})
            elif condition == "disabled":
                if exists and not ctrl.is_enabled():
                    return json.dumps({"status": "success", "condition": condition, "elapsed": round(time.time()-start, 2)})
            elif condition == "not_visible":
                if not exists:
                    return json.dumps({"status": "success", "condition": condition, "elapsed": round(time.time()-start, 2)})
        except Exception:
            pass
        time.sleep(0.2)

    return json.dumps({"status": "timeout", "condition": condition, "timeout": timeout})

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 3:
        print(json.dumps({"error": "Usage: ui_wait.py <target> <control_id> <condition> [timeout] [value]"}))
    else:
        timeout = int(args[3]) if len(args) > 3 else 10
        value = args[4] if len(args) > 4 else ""
        print(wait_for_control(args[0], args[1], args[2], timeout, value))
