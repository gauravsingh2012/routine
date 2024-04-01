#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <python_version> <virtualenv_name>"
    return 1
fi

# Assign arguments to variables
python_version="$1"
venv_name="$2"

# Concatenate python_version and venv_name to create the full virtual environment name
full_venv_name="${python_version}-${venv_name}"

# Initialize pyenv if not already initialized
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Create a virtual environment using pyenv
pyenv virtualenv "$python_version" "$full_venv_name"

# Activate the virtual environment
pyenv activate "$full_venv_name"

# Optionally, confirm that the virtual environment is activated
echo "Virtual environment $full_venv_name is activated."
