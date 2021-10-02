#!/usr/bin/env bash

set -eu

source ./harness-util/package-util.sh
create_pkg "windows" "x86-64" "ps1" "win_amd64"
