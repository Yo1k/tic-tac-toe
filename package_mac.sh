#!/usr/bin/env bash

set -eu

declare -r MAC_OS="mac"
source ./harness-util/package-util.sh "${MAC_OS}"
create_update_package
installation_python_requirements "${MAC_PLATFORM}"
package "${MAC_OS}"
