#!/usr/bin/env python3
"""
Dump the control tree of a Windows application window as JSON.

Part of the ui_automation/ example. See README.txt for details.

Usage:
    python ui_inspect.py <title-or-PID>

If the argument is all digits, it is treated as a process ID. Otherwise
it is treated as a window title substring (case-insensitive).

Output is JSON with fields:
    query           what was passed in
    window          the matched window's title
    backend         'uia' or 'win32' (which backend produced the result)
    controls        list of {type, name, auto_id} for each descendant
    backends_tried  which backends were tried before success

Requires:
    pip install pywinauto

Windows-only. Uses pywinauto's UIA backend, with a win32 fallback.
"""
import json, sys, time
from pywinauto import Desktop

def quick_inspect(title_or_pid, timeout=5):
    start = time.time()
    result = {'query': title_or_pid, 'controls': [], 'backends_tried': []}

    if str(title_or_pid).isdigit():
        try:
            from pywinauto import Application
            app = Application(backend='uia').connect(process=int(title_or_pid), timeout=2)
            win = app.top_window()
            result['window'] = win.window_text()
            result['backend'] = 'uia'
            for c in win.descendants():
                if time.time() - start > timeout:
                    break
                try:
                    info = c.element_info
                    if info.control_type:
                        result['controls'].append({
                            'type': info.control_type,
                            'name': info.name or '',
                            'auto_id': getattr(info, 'automation_id', '')
                        })
                except:
                    pass
            return json.dumps(result)
        except:
            pass

    for backend in ['uia', 'win32']:
        if time.time() - start > timeout:
            break
        result['backends_tried'].append(backend)
        try:
            desktop = Desktop(backend=backend)
            win = None
            for w in desktop.windows():
                try:
                    if title_or_pid.lower() in w.window_text().lower():
                        win = w
                        break
                except:
                    pass
            if not win:
                continue
            result['window'] = win.window_text()
            result['backend'] = backend
            for c in win.descendants():
                if time.time() - start > timeout:
                    break
                try:
                    info = c.element_info
                    if info.control_type:
                        result['controls'].append({
                            'type': info.control_type,
                            'name': info.name or '',
                            'auto_id': getattr(info, 'automation_id', '')
                        })
                except:
                    pass
            if result['controls']:
                break
        except Exception as e:
            result[backend + '_error'] = str(e)
            continue

    if not result.get('controls') and not result.get('window'):
        return json.dumps({'error': 'Window not found or no accessible controls'})
    return json.dumps(result)

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    if not arg:
        print(json.dumps({'error': 'Provide window title or PID'}))
    else:
        print(quick_inspect(arg))
