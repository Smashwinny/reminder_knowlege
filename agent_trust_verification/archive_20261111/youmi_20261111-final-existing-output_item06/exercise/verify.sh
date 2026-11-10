#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
for step in legacy types runtime unsafe guarded test; do
 python3 exercise/guard_lab.py "$step"
done
