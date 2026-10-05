#!/usr/bin/env python3
"""Verify the exact, officially downloaded lesson binary without downloading it."""
from pathlib import Path
import hashlib, subprocess, sys

binary=Path(__file__).resolve().parent/'vendor/toolbox'
expected='d8e0df24b5ce9934c8f7ae8466f64ff5512857c5a7e47640301750ee82f92db3'
if not binary.is_file():
    sys.exit('Missing vendor/toolbox. Follow README.md official download instructions first.')
h=hashlib.sha256()
with binary.open('rb') as stream:
    for block in iter(lambda: stream.read(1024*1024), b''):
        h.update(block)
actual=h.hexdigest()
assert actual==expected, 'Binary SHA-256 mismatch; stop and check the official source.'
version=subprocess.check_output([str(binary),'--version'],text=True).strip()
assert '1.13.1+binary.linux.amd64.e14cda6' in version
print('PASS: '+version)
print('PASS: measured official-download SHA-256 '+actual)
print('This file fingerprint is not an independently published signature.')
