#!/usr/bin/env bash

set -eu

source ./harness-util/package-util.sh
create_dist_pkg "linux" "x86-64" "manylinux2010_x86_64"
