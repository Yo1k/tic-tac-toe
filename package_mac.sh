#!/usr/bin/env bash

set -eu

source ./harness-util/package-util.sh
create_dist_pkg "mac" "x86-64" "macosx_10_9_x86_64"
