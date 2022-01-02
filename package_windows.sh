#!/usr/bin/env bash
# Packages the Python app with all its dependencies for Windows x86-64 platform.

set -eu

source ./harness-util/package-util.sh
create_pkg "windows" "x86-64" "${APP_NAME}.cmd" "win_amd64"
