#!/usr/bin/env bash
# Packages the application with all its dependencies for the Linux x86-64 platform.

set -eu

if [[ -v BUILD_DIR ]] \
        || {
            ( source ./harness-util/python-util.sh && verify ) \
            && source ./harness-util/package-util.sh; }
then
    create_pkg "linux" "x86-64" "${APP_NAME}.sh" "manylinux2010_x86_64"
fi
