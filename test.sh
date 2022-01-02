#!/usr/bin/env bash
# Runs all unit tests of the Python app.

set -eu

source ./harness-util/util.sh
cd "$(dirname "${0}")"
python3 -m unittest discover "${CODE_DIR}"
