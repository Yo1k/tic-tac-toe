#!/usr/bin/env bash
# Packages the application with all its dependencies for Windows x86-64 platform.

set -eu

if [[ "${BUILD_DIR+${BUILD_DIR}}" == "build" ]] \
        || ( source ./harness-util/python-util.sh && check ) \
        && source ./harness-util/package-util.sh ; then
    create_pkg "windows" "x86-64" "${APP_NAME}.cmd" "win_amd64"
fi
