#!/usr/bin/env bash
# Packages the Python app with all its dependencies for Linux x86-64 platform.

set -eu

source ./harness-util/package-util.sh
create_pkg "linux" "x86-64" "${APP_NAME}.sh" "manylinux2010_x86_64"
