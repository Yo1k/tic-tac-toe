#!/usr/bin/env bash

set -eu

cd "$(dirname "${0}")"
python3 -m unittest discover yo1k
