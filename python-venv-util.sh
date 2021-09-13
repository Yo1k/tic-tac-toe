#!/usr/bin/env bash

set -eu

declare -r PYTHON_VENV="ttt-venv"

function create_python_venv() {
    python3 -m venv ${PYTHON_VENV}
    IN_PYTHON_VENV=$(in_python_venv)
    if [[ ${IN_PYTHON_VENV} = "false" ]]; then
        activate_python_venv;
    fi
    python3 -m pip install -r requirements.txt
    if [[ ${IN_PYTHON_VENV} = "false" ]]; then
        deactivate_python_venv;
    fi
}

function in_python_venv() {
    python3 - ${PYTHON_VENV} <<EOF
import sys
import os
from pathlib import PurePath
if sys.prefix == sys.base_prefix:
    print("false")
else:
    expected_python_venv = sys.argv[1]
    current_python_venv = PurePath(sys.prefix).name
    if current_python_venv == expected_python_venv:
        print("true")
    else:
        sys.exit(("The script must be run either with Python venv named"
        + " '{expected_python_venv}' being active"
        + " or without any active venv.{linesep}").format(
        expected_python_venv = expected_python_venv, linesep = os.linesep))
EOF
}

function activate_python_venv() {
    source ${PYTHON_VENV}/bin/activate
}

function deactivate_python_venv() {
    deactivate
}

create_python_venv
