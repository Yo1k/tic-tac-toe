#!/usr/bin/env bash
# An application launcher for Bash.

set -eu

cd "$(dirname "${0}")"
python3 -m yo1k.tic_tac_toe
