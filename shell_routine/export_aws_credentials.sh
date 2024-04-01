#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 --profile <profile_name>"
    return 1
fi

# Assign the profile name from the argument
profile_name=$2

# Construct the command with the provided profile name
command="eval \"\$(aws configure export-credentials --profile $profile_name --format env)\""

# Set the AWS profile
export AWS_PROFILE="$profile_name"

# Execute the command
eval "$command"