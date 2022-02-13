#!/usr/bin/env bash
# Packages the application with all its dependencies for
# Linux, macOS, and Windows with x86-64 ISA.

set -eu

source ./package-linux.sh && source ./package-macos.sh && source ./package-windows.sh
