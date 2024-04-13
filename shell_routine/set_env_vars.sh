#!/bin/bash

# Check if arguments are provided
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    exit 1
fi

# Loop through the arguments
for var in "$@"; do
    # Check if the argument contains '=' to separate variable name and value
    if [[ "$var" == *"="* ]]; then
        # Split the argument into variable name and value
        var_name="${var%%=*}"
        var_value="${var#*=}"

        # Set the environment variable
        export "$var_name"="$var_value"

        echo "Set $var_name=$var_value"
    else
        echo "Error: Argument '$var' is not in the form 'VAR=value'. Skipping."
    fi
done
