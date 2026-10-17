#!/usr/bin/env python3
"""Only publish app metadata after the container images exist."""
from pathlib import Path
import re
import sys

version, digest = sys.argv[1:]
if not re.fullmatch(r'1\.0\.\d+', version):
    raise SystemExit('Invalid app version')
if not re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
    raise SystemExit('Invalid upstream digest')
config = Path('aiostreams/config.yaml')
original = config.read_text()
updated, count = re.subn(r'(?m)^version: "[^"]+"$', f'version: "{version}"', original)
if count != 1:
    raise SystemExit('Expected exactly one version in config.yaml')
config.write_text(updated)
Path('aiostreams/upstream-digest.txt').write_text(digest + '\n')
