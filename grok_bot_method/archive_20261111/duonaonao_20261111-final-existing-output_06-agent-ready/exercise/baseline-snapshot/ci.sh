#!/bin/sh
set -eu
python3 -m unittest discover -s tests -v
python3 tools/lint.py
