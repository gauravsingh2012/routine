def create_virtual_env_and_python_version_with_pyenv_alias(current_dir):
    shell_function = f"""
        create-and-activate-venv() {{
            python_version=""
            venv_name=""

            for arg in "$@"; do
                case "$arg" in
                    --python-version=*)
                        python_version="${{arg#*=}}"
                        ;;
                    --venv=*)
                        venv_name="${{arg#*=}}"
                        ;;
                    *)
                        echo "Invalid argument: $arg"
                        return 1
                        ;;
                esac
            done

            if [ -z "$python_version" ] || [ -z "$venv_name" ]; then
                echo "Usage: create-and-activate-venv --python-version=<version> --venv=<name>"
                return 1
            fi

            echo "$python_version"
            echo "$venv_name"

            source {current_dir}/shell_routine/create_virtual_env_with_pyenv.sh \
                "$python_version" "$venv_name"
        }}
    """
    return shell_function


def export_aws_credentials_alias(current_dir):
    shell_function = f"""
        export-aws-credentials() {{
            if [ "$#" -ne 2 ]; then
                echo "Usage: export-aws-credentials --profile <profile_name>"
                return 1
            fi

            # Assign the profile name from the argument
            profile_name=$2

            # execute the command
            source {current_dir}/shell_routine/export_aws_credentials.sh --profile "$profile_name"
        }}
    """
    return shell_function


def aws_sso_login(current_dir):
    shell_function = f"""
        aws-sso-login() {{
            if [ "$#" -ne 2 ]; then
                echo "Usage: aws-sso-login --profile <profile_name>"
                return 1
            fi

            # Assign the profile name from the argument
            profile_name=$2

            # execute the command
            source {current_dir}/shell_routine/aws_sso_login.sh --profile "$profile_name"
        }}
    """
    return shell_function


def aws_sso_login_all(current_dir):
    shell_function = f"""
        aws-sso-login-all() {{
            if [ "$#" -ne 2 ]; then
                echo "Usage: aws-sso-login-all --profile <profile_name>"
                return 1
            fi

            # Assign the profile name from the argument
            profile_name=$2

            # execute the command
            source {current_dir}/shell_routine/aws_sso_login_all.sh --profile "$profile_name"
        }}
    """
    return shell_function


def set_env_vars(current_dir):
    shell_function = f"""
        set-env-vars() {{
            source {current_dir}/shell_routine/set_env_vars.sh
        }}
    """
    return shell_function


def unset_env_vars(current_dir):
    shell_function = f"""
        unset-env-vars() {{
            source {current_dir}/shell_routine/unset_env_vars.sh
        }}
    """
    return shell_function
