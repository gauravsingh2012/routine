import os
import click
from utils import run_command


@click.command()
@click.option(
    "--token/--no-token",
    nargs=1,
    default=False,
    show_default=True,
    help="set this option to your Gitlab personal token to login",
)
@click.option(
    "--hostname",
    nargs=1,
    default="gitlab.com",
    show_default=True,
    help="set this option value as the group name of your gitlab project",
)
@click.option(
    "--group",
    nargs=1,
    required=True,
    show_default=True,
    help="set this option value as the group name of your gitlab project",
)
@click.argument("token_value", default="", nargs=1)
def clone_all_git_lab_projects(token: str, hostname: str, token_value: str, group: str):
    """
    This is a command to clone all projects including subprojects in a gitlab group
    """
    if token and token != "":
        glab_auth_command = (
            f"glab auth login --hostname {hostname} --token {token_value}"
        )
    else:
        glab_auth_command = "glab auth login"
    run_command(glab_auth_command)
    glab_clone_command = f"glab repo clone -g {group} -p --paginate"
    run_command(glab_clone_command)


def is_git_repository(directory):
    git_dir = os.path.join(directory, ".git")
    return os.path.exists(git_dir)


def git_pull_recursive(directory, git_command):
    """
    Recursively check if the directory is a Git repository and perform git pull
    """
    if is_git_repository(directory):
        print(f"Git pull latest from master for directory: {directory}")
        run_command(git_command, cwd=directory)
    else:
        print(
            f"{directory} is not a Git repository. Skipping current directory and iterating through subdirectories."
        )
    for dir_name in os.listdir(directory):
        full_path = os.path.join(directory, dir_name)
        if os.path.isdir(full_path):
            git_pull_recursive(full_path, git_command)


@click.command()
def git_pull_all():
    """
    This is a command to pull all git repositories in the current directory and its subdirectories
    """
    print(
        "====================================== Git pull all started. ======================================"
    )
    checkout_master_and_pull_command = "git checkout master && git pull"
    current_dir = os.getcwd()
    print(f"Git pull latest from master for current directory: {current_dir}")
    # Perform git checkout master and a git pull in the current directory
    if is_git_repository(current_dir):
        run_command(checkout_master_and_pull_command, cwd=current_dir)
    else:
        print(
            f"{current_dir} is not a Git repository. Skipping current directory and iterating through subdirectories."
        )

    # Loop through subdirectories and perform git pull
    for dir_name in os.listdir(current_dir):
        full_path = os.path.join(current_dir, dir_name)
        if os.path.isdir(full_path):
            git_pull_recursive(full_path, checkout_master_and_pull_command)

    print(
        "====================================== Git pull all completed. ======================================"
    )
