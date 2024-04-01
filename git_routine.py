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
