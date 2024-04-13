#!/bin/bash

# Check if arguments are provided
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    exit 1
fi

# Loop through the arguments
for var_name in "$@"; do
    # Unset the environment variable
    unset "$var_name"

    echo "Unset $var_name"
done