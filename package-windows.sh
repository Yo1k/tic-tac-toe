#!/usr/bin/env bash
# Packages the application with all its dependencies for the Windows x86-64 platform.

set -eu

if [[ -v BUILD_DIR ]] \
        || {
            ( source ./harness-util/python-util.sh && verify ) \
            && source ./harness-util/package-util.sh; }
then
    create_pkg "windows" "x86-64" "${APP_NAME}.cmd" "win_amd64"
fi
