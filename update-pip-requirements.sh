#!/usr/bin/env bash

set -eu

source ./harness-util/util.sh
IN_PYTHON_VENV=$(in_python_venv)
if [[ ${IN_PYTHON_VENV} = "false" ]]; then
    activate_python_venv;
fi
python3 -m pip freeze > requirements.txt
if [[ ${IN_PYTHON_VENV} = "false" ]]; then
    deactivate_python_venv;
fi
