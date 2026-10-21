CHAMELEONOS QR CODE
==================

FILES
-----
  chameleonos-qr.png  - the QR code image (860 bytes, version 4, 33x33 modules)
  make_qr.py          - the script that generated it, reusable for any URL
  QR-README.txt       - this file

WHAT chameleonos-qr.png ENCODES
-------------------------------
  https://progenitorfreeagen.wixsite.com/my-site-62

HOW TO USE
----------

  1. Open chameleonos-qr.png in any image viewer.
  2. Point a phone camera at the screen (15-30 cm away, bright display).
  3. Phone shows a link to open the URL.

  To print: open the PNG, File - Print.

HOW TO REGENERATE OR MAKE A NEW ONE
-----------------------------------

  Install the QR library once:
    pip install qrcode

  Then generate for any URL:
    python make_qr.py https://example.com my-qr.png

  Examples:
    python make_qr.py https://progenitorfreeagen.wixsite.com/my-site-62
        -> qr.png (uses default output name)
    python make_qr.py https://progenitorfreeagen.wixsite.com/my-site-62 chameleonos-qr.png
        -> chameleonos-qr.png (explicit output name)

  The script defaults to Version 4, error correction M.
  That size holds URLs up to about 80 characters with good scan reliability.

VERIFY THE URL WITHOUT SCANNING
------------------------------

  pip install pyzbar pillow
  python -c "from pyzbar.pyzbar import decode; from PIL import Image; print(decode(Image.open('chameleonos-qr.png'))[0].data.decode())"
