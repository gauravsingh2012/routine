import click
from utils import run_command


@click.command()
def run_brew_update_upgrade_and_cleanup():
    """
    This is a command to brew update, upgrade and cleanup
    """
    brew_update_command = "brew update"
    run_command(brew_update_command)
    brew_upgrade_command = "brew upgrade"
    run_command(brew_upgrade_command)
    brew_cleanup_command = "brew cleanup --prune=all"
    run_command(brew_cleanup_command)
