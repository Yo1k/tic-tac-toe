#!/usr/bin/env bash

set -eu

declare -r WIN_OS="win"
source ./harness-util/package-util.sh "${WIN_OS}"
create_update_package
installation_python_requirements "${WIN_PLATFORM}"
package "${WIN_OS}"
