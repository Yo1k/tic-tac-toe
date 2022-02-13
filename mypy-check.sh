#!/usr/bin/env bash
# Uses Mypy to check static types of the code.

set -eu

source ./harness-util/python-util.sh
mypy_check
