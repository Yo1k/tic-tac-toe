#!/usr/bin/env bash
# Packages the application with all its dependencies for Linux x86-64 platform.

set -eu

if [[ "${BUILD_DIR+${BUILD_DIR}}" == "build" ]] \
        || ( source ./harness-util/python-util.sh && check ) \
        && source ./harness-util/package-util.sh ; then
    create_pkg "linux" "x86-64" "${APP_NAME}.sh" "manylinux2010_x86_64"
fi
