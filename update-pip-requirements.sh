#!/usr/bin/env bash
# Updates all Python dependencies of the project in `requirements.txt` based on the project's
# Python virtual environment.
# In order to add a new dependency / upgrade the existing dependency:
# - install / upgrade the dependency in the project's Python virtual environment;
# - run this script.

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
