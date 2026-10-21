#!/usr/bin/env python3
"""
Select a voice on Speechma by name.

Part of the voice_switching/ example. See README.txt for details.

Usage:
    python select_voice.py "Voice Name"
Example:
    python select_voice.py "Andrew Multilingual"
"""
import sys, io, json, time, subprocess

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# --- Machine-specific constants (edit for your environment) ---
BROWSER_TARGET = 'firefox.exe,SPEECHMA'
DESK_EXECUTOR = 'C:/ai/automation/core/desk_executor_seq.py'
DESK_SCANNER = 'C:/ai/automation/core/desktop_scanner_optimized.py'
TEMP_SEQ = 'C:/ai/temp_seq.json'
VERIFY_SCAN = 'C:/ai/speechma_verify_scan.json'
SELECT_SCAN = 'C:/ai/voice_select_scan.json'
CLICK_SEQ = 'C:/ai/click_voice.json'
SCROLL_TOP = '1909, 129'      # click 5x to scroll to top
SCROLL_DOWN_1 = '1909, 1058'  # click once
SCROLL_DOWN_2 = '1909, 1072'  # click 3x
# --------------------------------------------------------------

def log(msg):
    print(msg)
    sys.stdout.flush()

def run_sequence(actions, description):
    log('  ' + description + '...')
    with open(TEMP_SEQ, 'w') as f:
        json.dump(actions, f, indent=2)
    result = subprocess.run(
        ['python', DESK_EXECUTOR, BROWSER_TARGET, TEMP_SEQ, VERIFY_SCAN],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        log('  ' + description + ' failed: ' + result.stderr)
        return False
    log('  done')
    time.sleep(0.3)
    return True

def scroll_to_voice_area():
    actions = [{'action': 'click_xy', 'value': SCROLL_TOP, 'delay_after': 0.1} for _ in range(5)]
    if not run_sequence(actions, 'Scroll to top (5 clicks)'):
        return False
    actions = [{'action': 'click_xy', 'value': SCROLL_DOWN_1, 'delay_after': 0.1}]
    if not run_sequence(actions, 'Click lower scroll'):
        return False
    actions = [{'action': 'click_xy', 'value': SCROLL_DOWN_2, 'delay_after': 0.1} for _ in range(3)]
    if not run_sequence(actions, 'Click further down (3 clicks)'):
        return False
    return True

def select_voice(voice_name):
    log('[SELECT] Selecting voice: ' + voice_name)
    if not scroll_to_voice_area():
        log('Failed to scroll to voice area')
        return False
    log('  Scanning for voice label...')
    scan_result = subprocess.run(
        ['python', DESK_SCANNER, BROWSER_TARGET, SELECT_SCAN, '--fast'],
        capture_output=True, text=True, timeout=40
    )
    if scan_result.returncode != 0:
        log('  Scan failed')
        return False
    with open(SELECT_SCAN, 'r', encoding='utf-8') as f:
        scan = json.load(f)
    target = None
    for item in scan.get('items', []):
        label = item.get('label', '').strip()
        if label.lower() == voice_name.lower():
            bbox = item.get('bbox')
            if bbox and len(bbox) == 4:
                target = (bbox[0], bbox[1], bbox[2], bbox[3])
                break
    if not target:
        log('  Voice "' + voice_name + '" not found in scan.')
        return False
    x = (target[0] + target[2]) // 2
    y = (target[1] + target[3]) // 2
    log('  Found at (' + str(x) + ', ' + str(y) + ')')
    click_seq = [{'action': 'click_xy', 'value': str(x) + ', ' + str(y), 'delay_after': 0.3}]
    with open(CLICK_SEQ, 'w') as f:
        json.dump(click_seq, f, indent=2)
    result = subprocess.run(
        ['python', DESK_EXECUTOR, BROWSER_TARGET, CLICK_SEQ, SELECT_SCAN],
        capture_output=True, text=True, timeout=20
    )
    if result.returncode != 0:
        log('  Click failed')
        return False
    log('  Voice selected successfully')
    return True

def main():
    if len(sys.argv) < 2:
        log('Usage: python select_voice.py "Voice Name"')
        log('Example: python select_voice.py "Andrew Multilingual"')
        sys.exit(1)
    voice_name = sys.argv[1]
    if select_voice(voice_name):
        log('[DONE] Voice selection complete.')
    else:
        log('[FAIL] Voice selection failed.')
        sys.exit(1)

if __name__ == '__main__':
    main()
