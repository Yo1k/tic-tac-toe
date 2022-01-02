#!/usr/bin/env bash
# Updates `requirements.txt`, that stores all Python project's dependencies.

set -eu

source ./harness-util/python-util.sh
IN_PYTHON_VENV=$(in_python_venv)
if [[ ${IN_PYTHON_VENV} = "false" ]]; then
    activate_python_venv;
fi
python3 -m pip freeze > requirements.txt
if [[ ${IN_PYTHON_VENV} = "false" ]]; then
    deactivate_python_venv;
fi
