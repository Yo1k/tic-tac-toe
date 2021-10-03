#!/usr/bin/env bash

set -eu

source ./harness-util/package-util.sh
create_pkg "macos" "x86-64" "${APP_NAME}.sh" "macosx_10_9_x86_64"
