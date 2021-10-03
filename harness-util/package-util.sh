#!/usr/bin/env bash

set -eu

declare -r APP_NAME="tic-tac-toe"

# ${1} - the target OS
# ${2} - the target ISA
function pkg_src_dir() {
    declare -r BUILD_DIR_NAME="build"
    echo "./${BUILD_DIR_NAME}/${APP_NAME}_${1}_${2}"
}

# ${1}, ${2} - see `pkg_src_dir()`
# ${3} - the application launcher name
function copy_code() {
    CODE_DIR="yo1k"
    declare -r PKG_SRC_DIR=$(pkg_src_dir "${1}" "${2}")
    mkdir -p "${PKG_SRC_DIR}"
    rm -rf "${PKG_SRC_DIR:?}/${CODE_DIR}"
    cp -r "./${CODE_DIR}" "${PKG_SRC_DIR}"
    cp -u "${3}" "${PKG_SRC_DIR}"
}

# ${1}, ${2} - see `pkg_src_dir()`
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

# ${1}, ${2} - see `pkg_src_dir()`
function pack() {
    declare -r PKG_SRC_DIR=$(pkg_src_dir "${1}" "${2}")
    pushd "${PKG_SRC_DIR}"
    zip -r "../${APP_NAME}_${1}_${2}.zip" "."
    popd
}

# ${1}, ${2}, ${3} - see `copy_code()`
# ${4} - see `install_python_requirements()`
function create_pkg() {
    copy_code "${1}" "${2}" "${3}"
    install_python_requirements "${1}" "${2}" "${4}"
    pack "${1}" "${2}"
}
