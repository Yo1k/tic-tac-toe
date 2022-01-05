#!/usr/bin/env bash
# Activates Python virtual environment for the project.

source ./harness-util/util.sh
./harness-util/python-util.sh
source ./"${PYTHON_VENV}"/bin/activate
