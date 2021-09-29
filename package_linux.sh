#!/usr/bin/env bash

set -eu

declare -r LINUX_OS="linux"
source ./harness-util/package-util.sh "${LINUX_OS}"
create_update_package
installation_python_requirements "${LINUX_PLATFORM}"
package "${LINUX_OS}"
