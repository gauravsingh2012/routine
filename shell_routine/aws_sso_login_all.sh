#!/bin/bash

# Default values for arguments
profile=""
region="us-east-1"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --profile)
            profile="$2"
            shift # past argument
            shift # past value
            ;;
        --region)
            region="$2"
            shift # past argument
            shift # past value
            ;;
        *)
            echo "Invalid argument: $1"
            exit 1
            ;;
    esac
done

# Check if required argument is provided
if [ -z "$profile" ]; then
    echo "Usage: $0 --profile <profile_name>"
    return 1
fi

unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
unset AWS_EXPIRATION

# Set the AWS profile
export AWS_PROFILE="$profile"

# Execute AWS SSO login with the specified profile
aws sso login --profile "$profile"

