#!/usr/bin/env bash
# Runs the Python app on Linux or macOS.

set -eu

cd "$(dirname "${0}")"
python3 -m yo1k.tic_tac_toe
