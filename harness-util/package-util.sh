#!/usr/bin/env bash

set -eu

source ./harness-util/global-util.sh
declare PACKAGE_TARGET="./${BUILD_NAME}/${PACKAGE_NAME}_${1}_${ARCH}" # ${1} is NAME_OS
function create_update_package() {
    mkdir -p "${PACKAGE_TARGET}"
    rm -rf "${PACKAGE_TARGET:?}/${PYTHON_NAMESPACE_PACKAGE}"
    cp -r "./${PYTHON_NAMESPACE_PACKAGE}" "${PACKAGE_TARGET}"
    cp "./${PACKAGE_NAME}.sh" "${PACKAGE_TARGET}"
}

function installation_python_requirements() {
    #{1} is PLATFORM
    python3 -m pip install -r requirements.txt \
        --platform="${1}" \
        --python-version="${PYTHON_VERSION}" \
        --implementation="${PYTHON_IMPLEMENTATION}" \
        --only-binary=:all: \
        --target="${PACKAGE_TARGET}"
}

function package() {
    pushd "./${BUILD_NAME}"
    zip -r "./${PACKAGE_NAME}_${1}_${ARCH}.zip" "./${PACKAGE_NAME}_${1}_${ARCH}" # ${1} is NAME_OS
    popd
}
