#!/usr/bin/env bash
# Activates Python project's virtual environment.

source ./harness-util/util.sh
./harness-util/python-util.sh
source ./"${PYTHON_VENV}"/bin/activate
