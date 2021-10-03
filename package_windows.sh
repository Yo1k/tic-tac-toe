#!/usr/bin/env bash

set -eu

source ./harness-util/package-util.sh
create_pkg "windows" "x86-64" "${APP_NAME}.cmd" "win_amd64"
