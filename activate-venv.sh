#!/usr/bin/env bash
# Creates or in the case existence activates Python virtual environment for the project.
# Adds the project root directory to `PYTHONPATH` environment variable.

source ./harness-util/util.sh
./harness-util/python-util.sh
source ./"${PYTHON_VENV}"/bin/activate
[[ ":${PYTHONPATH}:" != *":${PWD}:"* ]] && export PYTHONPATH=${PYTHONPATH:+${PYTHONPATH}:}${PWD}
