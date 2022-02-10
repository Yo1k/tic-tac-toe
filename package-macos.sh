#!/usr/bin/env bash
# Packages the application with all its dependencies for the macOS x86-64 platform.

set -eu

if [[ -v BUILD_DIR ]] \
        || {
            ( source ./harness-util/python-util.sh && verify ) \
            && source ./harness-util/package-util.sh; }
then
    create_pkg "macos" "x86-64" "${APP_NAME}.sh" "macosx_10_9_x86_64"
fi
