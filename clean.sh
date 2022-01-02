#!/usr/bin/env bash
# Cleans the build directory, that consists of Python app packages for different platforms.

set -eu

source ./harness-util/package-util.sh
clean_build
