#!/usr/bin/env bash

set -eu

declare -r DIST_PACKAGE_NAME="tic-tac-toe"

# ${1} - the name of the target OS
# ${2} - the architecture of the target OS
function pkg_src_dir() {
    declare -r BUILD_DIR_NAME="build"
    echo "./${BUILD_DIR_NAME}/${DIST_PACKAGE_NAME}_${1}_${2}"
}

# ${1} - the name of the target OS
# ${2} - the architecture of the target OS
function copy_code() {
    PYTHON_NAMESPACE_PACKAGE="yo1k"
    declare -r PKG_SRC_DIR=$(pkg_src_dir "${1}" "${2}")
    mkdir -p "${PKG_SRC_DIR}"
    rm -rf "${PKG_SRC_DIR:?}/${PYTHON_NAMESPACE_PACKAGE}"
    cp -r "./${PYTHON_NAMESPACE_PACKAGE}" "${PKG_SRC_DIR}"
    cp -u "./${DIST_PACKAGE_NAME}.sh" "${PKG_SRC_DIR}"
}

# ${1} - the name of the target OS
# ${2} - the architecture of the target OS
# ${3} - `--platform` passed to `pip install`,
#     see https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-platform
function install_python_requirements() {
    declare -r PKG_SRC_DIR=$(pkg_src_dir "${1}" "${2}")
    python3 -m pip install -r requirements.txt \
        --platform="${3}" \
        --python-version="39" \
        --implementation="cp" \
        --only-binary=:all: \
        --target="${PKG_SRC_DIR}"
}

# ${1} - the name of the target OS
# ${2} - the architecture of the target OS
function pack() {
    declare -r PKG_SRC_DIR=$(pkg_src_dir "${1}" "${2}")
    pushd "${PKG_SRC_DIR}"
    zip -r "../${DIST_PACKAGE_NAME}_${1}_${2}.zip" "."
    popd
}

# ${1} - the name of the target OS
# ${2} - the architecture of the target OS
# ${3} - `--platform` passed to `pip install`,
#     see https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-platform
function create_dist_pkg() {
    copy_code "${1}" "${2}"
    install_python_requirements "${1}" "${2}" "${3}"
    pack "${1}" "${2}"
}
