import os
import click
from utils import (
    append_aliases_to_zshrc_utility,
    run_command,
    setup_zsh_profile_env_files_in_home_directory_utility,
)


@click.command()
def append_aliases_to_zshrc():
    """
    This is a command to append shell aliases to the zshrc file defined in the shell_routine_alias module
    """
    append_aliases_to_zshrc_utility()


@click.command()
def setup_zsh_profile_env_files_in_home_directory():
    """
    This is a command to update the zsh profile env files in the routine project
    """
    setup_zsh_profile_env_files_in_home_directory_utility()


@click.command()
def copy_zsh_profile_env_files_in_routine_project():
    """
    This is a command to update the zsh profile env files in the routine project
    """
    home_dir = os.path.expanduser("~")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    command = (
        f"cp {home_dir}/.zshrc {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc && "
        f"cp {home_dir}/.zshrc_aws_variables {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_aws_variables && "
        f"cp {home_dir}/.zshrc_path_variables {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_path_variables && "
        f"cp {home_dir}/.zshrc_config_variables {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_config_variables &&"
        f"cp {home_dir}/.zshrc_aliases {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_aliases && "
        f"cp {home_dir}/.config/starship.toml {current_dir}/zsh_profile_env_files/starship.toml"
    )
    run_command(command)
