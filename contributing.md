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

| &#x23; | Command                                             | Description                                                                                                                                                                                                                                                                                                                                   |
|--------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | `source ./activate-venv.sh`                         | Creates or in the case existence activates Python virtual environment for the project &#8212; `ttt-venv`. Also adds the project root directory to `PYTHONPATH` environment variable. `toolchain-requirements.txt` contains all Python dependencies of the project. `requirements.txt` contains all dependencies required for the application. |
| 1      | `./pylint-check.sh && ./mypy-check.sh && ./test.sh` | Analyzes and reports errors, checks style, checks static types, and runs tests.                                                                                                                                                                                                                                                               |
| 1.1    | `./pylint-check.sh`                                 | Analyzes and reports errors, checks style.                                                                                                                                                                                                                                                                                                    |
| 1.2    | `./mypy-check.sh`                                   | Checks static types.                                                                                                                                                                                                                                                                                                                          |
| 1.3    | `./test.sh`                                         | Runs all tests.                                                                                                                                                                                                                                                                                                                               |
| 2      | `./tic-tac-toe.sh`                                  | Runs the application.                                                                                                                                                                                                                                                                                                                         |
| 3      | `./package-all.sh`                                  | Packages the application with all its dependencies for Linux, macOS, and Windows with x86-64 ISA to `build` directory.                                                                                                                                                                                                                        |
| 3.1    | `./package-linux.sh`                                | Packages the application with all its dependencies for Linux x86-64 platform to `build` directory.                                                                                                                                                                                                                                            |
| 3.2    | `./package-macos.sh`                                | Packages the application with all its dependencies for macOS x86-64 platform to `build` directory.                                                                                                                                                                                                                                            |
| 3.3    | `./package-windows.sh`                              | Packages the application with all its dependencies for Windows x86-64 platform to `build` directory.                                                                                                                                                                                                                                          |
| 3.4    | `./clean.sh`                                        | Clean the `build` directory.                                                                                                                                                                                                                                                                                                                  |                                        |                                                                                                                        |
