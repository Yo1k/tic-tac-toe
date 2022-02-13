# Contributor Guide

## Prepare the development environment

Install [Python 3.9](https://www.python.org/downloads/).

If you are using a shell capable of running [Bash](https://www.gnu.org/software/bash/) scripts, run the following from the project 
root directory:
```shell
$ source ./activate-venv.sh
```

Otherwise, follow these manual steps using this
[guide](https://docs.python.org/3.9/tutorial/venv.html?highlight=package):
1. Create virtual environment for your project.
2. Activate project's virtual environment.
3. Install all project dependencies in the project's virtual environment using `toolchain-requirements.txt`.

## Build-related commands

If you are using a shell capable of running Bash scripts, run from the project root directory:

| #   | Command                                             | Description                                                                                                                                                                                                                                                                                                                                |
|-----|-----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0   | `source ./activate-venv.sh`                         | Creates if necessary and activates a Python virtual environment for the project&mdash;`ttt-venv`. Also adds the project root directory to the `PYTHONPATH` environment variable. `toolchain-requirements.txt` specifies all Python dependencies of the project. `requirements.txt` specifies all dependencies required by the application. |
| 1   | `./pylint-check.sh && ./mypy-check.sh && ./test.sh` | Analyzes and reports errors, checks style; checks static types; and runs all tests, respectively.                                                                                                                                                                                                                                          |
| 2   | `./tic-tac-toe.sh`                                  | Runs the application.                                                                                                                                                                                                                                                                                                                      |
| 3   | `./package-all.sh`                                  | Packages the application with all its dependencies for the Linux, macOS, and Windows with x86-64 ISA to the `build` directory.                                                                                                                                                                                                             |
| 3.1 | `./package-linux.sh`                                | Packages the application with all its dependencies for the Linux x86-64 platform to the `build` directory.                                                                                                                                                                                                                                 |
| 3.2 | `./package-macos.sh`                                | Packages the application with all its dependencies for the macOS x86-64 platform to the `build` directory.                                                                                                                                                                                                                                 |
| 3.3 | `./package-windows.sh`                              | Packages the application with all its dependencies for the Windows x86-64 platform to the `build` directory.                                                                                                                                                                                                                               |
| 3.4 | `./clean.sh`                                        | Cleans the `build` directory.                                                                                                                                                                                                                                                                                                              |                                        |                                                                                                                        |
