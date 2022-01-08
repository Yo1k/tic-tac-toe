#!/usr/bin/env bash
# Packages the application with all its dependencies for macOS x86-64 platform.

set -eu

source ./harness-util/package-util.sh
create_pkg "macos" "x86-64" "${APP_NAME}.sh" "macosx_10_9_x86_64"
