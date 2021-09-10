#!/usr/bin/env bash

set -eu

declare -r PYTHON_VENV="tic-tac-toe-venv"

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
expected_python_venv = sys.argv[1]
current_python_venv = sys.prefix.split("/")[-1]
if sys.prefix == sys.base_prefix:
    sys.stdout.write('false')
else:
    if current_python_venv == expected_python_venv:
        sys.stdout.write('true')
    else:
        sys.stderr.write(('The script must be run either with Python venv named "{0}" being active'
        + ' or without any active venv.{1}').format(expected_python_venv, os.linesep))
        sys.exit(1)
EOF
}

function activate_python_venv() {
    source ${PYTHON_VENV}/bin/activate
}

function deactivate_python_venv() {
    deactivate
}

create_python_venv
