#!/bin/bash

###############################################################################
# Script Name: poetry_project_setup.sh
# Description: Automates the setup and management of a Python project using Poetry.
#              - Installs Poetry if not already installed
#              - Creates and activates a virtual environment with dependencies
#              - Runs formatters, linters, and tests
#              - Builds the project for distribution
#
# Usage: Run this script in the project root directory.
#
# Prerequisites:
#   - Python 3.7 or higher must be installed
#   - This script should be run in the root directory of the project with a pyproject.toml
#
# Parameters:
#   - PROJECT_NAME: Set the project name (default: "my_poetry_project").
#
# Author: Patrick Schneider
# Last Updated: 2024-11-02
###############################################################################

# Exit on errors and unset variables
set -euo pipefail

# Configuration Variables
PROJECT_NAME="gh-repo-traffic"
INFO_COLOR="\033[1;32m"
ERROR_COLOR="\033[1;31m"
STEP_COLOR="\033[1;34m"
RESET_COLOR="\033[0m"
CHECK_MARK="✔"
CROSS_MARK="✘"
ARROW="➔"

# Logging Functions
log() { echo -e "${INFO_COLOR}[INFO]${RESET_COLOR} ${CHECK_MARK} $1"; }
step() { echo -e "\n${STEP_COLOR}[STEP]${RESET_COLOR} ${ARROW} $1"; }
error_exit() { echo -e "${ERROR_COLOR}[ERROR]${RESET_COLOR} ${CROSS_MARK} $1" >&2; exit 1; }

# Step 1: Ensure Poetry is Installed
install_poetry() {
  step "Checking if Poetry is installed"
  if ! command -v poetry &>/dev/null; then
    log "Poetry not found. run curl -sSL https://install.python-poetry.org | python3 -"
    # log "Poetry not found. Installing Poetry."
    # curl -sSL https://install.python-poetry.org | python3 - || error_exit "Poetry installation failed."
    # log "Poetry installed successfully."
  else
    log "Poetry is already installed."
  fi
}

# Step 2: Configure the Project Environment
setup_poetry_environment() {
  step "Setting up Poetry environment and installing dependencies"
  poetry install --with dev -vvv || error_exit "Poetry failed to install dependencies."
  log "Dependencies installed successfully."
}

# Step 3: Running Linters, Formatters, and Tests
run_dev_tools() {
  step "Running formatters and linters"
  poetry run black . -vvv || error_exit "Black formatting failed"
  poetry run flake8 --exclude=.venv,node_modules,migrations --max-line-length=88 --ignore=E203,W503,E231,E501 -vvv || error_exit "Flake8 style check failed"
  log "Formatting and linting completed successfully."

  step "Running tests"
  poetry run pytest -vvv || error_exit "Tests failed"
  log "Tests passed successfully."
}

# Step 4: Building the Project for Distribution
build_project() {
  step "Building the project"
  poetry build -vvv || error_exit "Project build failed"
  log "Project built successfully."
}

# Step 5: Display Project Info
display_project_info() {
  step "Displaying project dependencies and environment information"
  poetry show --tree -vvv || error_exit "Failed to display dependencies"
  poetry env info -vvv || error_exit "Failed to display environment info"
}

# Main Execution Function
main() {
  install_poetry
  setup_poetry_environment
  run_dev_tools
  build_project
  display_project_info
}

# Execute Main Function
main

