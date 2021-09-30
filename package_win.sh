#!/usr/bin/env bash

set -eu

source ./harness-util/package-util.sh
create_dist_pkg "win" "x86-64" "win_amd64"
