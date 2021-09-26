#!/usr/bin/env bash

set -eu

function create_ttt_linux_build() {
    declare -r APP_LINUX="ttt-linux"
    if [ ! -d "./build/${APP_LINUX}" ]; then
        mkdir ./build/${APP_LINUX}
    fi
    cp -r ./yo1k ./build/${APP_LINUX}
    cp ./tic-tac-toe.sh ./build/${APP_LINUX}
    python3 -m pip install -r requirements.txt --platform=manylinux2010_x86_64 --python-version=39 \
    --implementation=cp --only-binary=:all: --target=./build/${APP_LINUX}
    zip -r ./build/"${APP_LINUX}.zip" ./build/${APP_LINUX}
}

create_ttt_linux_build
