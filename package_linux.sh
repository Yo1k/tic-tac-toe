#!/usr/bin/env bash

set -eu

source ./harness-util/package-util.sh
create_pkg "linux" "x86-64" "sh" "manylinux2010_x86_64"
