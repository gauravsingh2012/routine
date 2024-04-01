import os
import click
from utils import (
    append_aliases_to_zshrc_utility,
    run_command,
    setup_zsh_profile_env_files_in_home_directory_utility,
)


@click.command()
def setup_sandbox():
    """
    This is a command to setup a sandbox
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Setting up sandbox .....")
    setup_zsh_profile_env_files_in_home_directory_utility()
    append_aliases_to_zshrc_utility()
    command = (
        "source ~/.zshrc && "
        "brew update && "
        "brew upgrade && "
        f"brew bundle install --file={current_dir}/Brewfile && "
        "brew cleanup --prune=all"
    )
    run_command(command)
