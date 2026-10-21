#!/usr/bin/env python3
"""
List available voices on Speechma using explicit scroll coordinates.

Part of the voice_switching/ example. See README.txt for details.
"""
import sys, io, json, time, subprocess, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# --- Machine-specific constants (edit for your environment) ---
BROWSER_TARGET = 'firefox.exe,SPEECHMA'
DESK_EXECUTOR = 'C:/ai/automation/core/desk_executor_seq.py'
DESK_SCANNER = 'C:/ai/automation/core/desktop_scanner_optimized.py'
TEMP_SEQ = 'C:/ai/temp_seq.json'
VERIFY_SCAN = 'C:/ai/speechma_verify_scan.json'
OUTPUT_SCAN = 'C:/ai/voice_list_scan.json'
SCROLL_TOP = '1909, 129'      # click 5x to scroll to top
SCROLL_DOWN_1 = '1909, 1058'  # click once
SCROLL_DOWN_2 = '1909, 1072'  # click 3x
VOICE_AREA_Y_MIN = 300
VOICE_AREA_Y_MAX = 800
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

def main():
    log('[START] Listing voices with explicit scroll')
    actions = [{'action': 'click_xy', 'value': SCROLL_TOP, 'delay_after': 0.1} for _ in range(5)]
    if not run_sequence(actions, 'Scroll to top (5 clicks)'):
        sys.exit(1)
    actions = [{'action': 'click_xy', 'value': SCROLL_DOWN_1, 'delay_after': 0.1}]
    if not run_sequence(actions, 'Click lower scroll'):
        sys.exit(1)
    actions = [{'action': 'click_xy', 'value': SCROLL_DOWN_2, 'delay_after': 0.1} for _ in range(3)]
    if not run_sequence(actions, 'Click further down (3 clicks)'):
        sys.exit(1)
    log('[SCAN] Running fast scan...')
    scan_result = subprocess.run(
        ['python', DESK_SCANNER, BROWSER_TARGET, OUTPUT_SCAN, '--fast'],
        capture_output=True, text=True, timeout=40
    )
    if scan_result.returncode != 0:
        log('Scan failed')
        sys.exit(1)
    with open(OUTPUT_SCAN, 'r', encoding='utf-8') as f:
        scan = json.load(f)
    voice_names = []
    for item in scan.get('items', []):
        label = item.get('label', '').strip()
        if not label:
            continue
        exclude = ['Input', 'Text', 'Security', 'Refresh', 'Generate', 'Voice Effects',
                   'Tutorials', 'Clear', 'Open help', 'Downloads', 'Pane', 'Group',
                   'List', 'Item', 'Separator', 'Title', 'Speechma API', 'Home', 'About',
                   'Contact', 'FAQ', 'Use Cases', 'Features', 'API', 'Support',
                   'English', 'Multilingual', 'Male', 'Female', 'United States', 'France',
                   'Play', 'Download', 'Delete', 'Generated', 'Audios', 'Support SPEECHMA',
                   'Try Now', 'Dismiss', 'Open support form', 'SpeechmaPRO']
        if any(ex in label for ex in exclude):
            continue
        bbox = item.get('bbox')
        if not bbox or len(bbox) < 4:
            continue
        y_center = (bbox[1] + bbox[3]) // 2
        if y_center < VOICE_AREA_Y_MIN or y_center > VOICE_AREA_Y_MAX:
            continue
        if re.search(r'[A-Za-z]', label) and len(label) > 2:
            voice_names.append(label)
    if voice_names:
        log('Found ' + str(len(voice_names)) + ' voice names:')
        for idx, name in enumerate(voice_names, 1):
            log('  ' + str(idx) + '. ' + name)
    else:
        log('No voice names found.')
    log('[DONE]')

if __name__ == '__main__':
    main()
