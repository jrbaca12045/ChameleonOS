#!/usr/bin/env python3
"""make_qr.py - generate a QR code PNG for any URL or text.

Usage:
  python make_qr.py <url> [output.png]

Examples:
  python make_qr.py https://example.com
  python make_qr.py https://example.com my-qr.png

Requires: pip install qrcode
"""
import os, sys

if len(sys.argv) < 2:
    print('Usage: python make_qr.py <url> [output.png]')
    print('Example: python make_qr.py https://example.com')
    sys.exit(1)

url = sys.argv[1].strip()
out = sys.argv[2].strip() if len(sys.argv) > 2 else 'qr.png'

try:
    import qrcode
except ImportError:
    print('[FAIL] qrcode library not installed.')
    print('       Run: pip install qrcode')
    sys.exit(1)

try:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(out)
except Exception as e:
    print('[FAIL] could not generate QR:', e)
    sys.exit(1)

print('[OK] wrote:', out)
print('[OK] size: %d bytes' % os.path.getsize(out))
print('[OK] url:', url)
print('[OK] version: %d' % qr.version)
print('[OK] modules: %d' % qr.modules_count)
