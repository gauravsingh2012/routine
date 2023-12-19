import subprocess

import click


@click.group()
@click.option("--debug/--no-debug", default=False, help="set debug mode")
def cli(debug: bool):
    click.echo("Debug mode is %s" % ("on" if debug else "off"))


@cli.command()
@click.argument("container_id", nargs=1)
def go_inside_docker_container(container_id: str):
    """
    This is a command to start a shell inside the docker container with the given container_id
    """
    command = f"docker exec -it {container_id} bash"
    run_command(command)


@cli.command()
@click.argument("container_id", nargs=1)
def stop_and_remove_docker_container(container_id: str):
    """
    This is a command to stop and remove a docker container with the given container_id
    """
    command = f"docker stop {container_id}"
    run_command(command)
    command = f"docker rm {container_id}"
    run_command(command)


@cli.command()
@click.option(
    "--min_size",
    nargs=1,
    default="100",
    help="set this option to specify the min size of the files to be searched for in MEGABYTES",
)
def find_files_taking_disk_space(min_size: str):
    """
    This is a command to find files greater than min_size on your disk
    """
    command = f"sudo find / -xdev -type f -size +{min_size}M -exec ls -lh {{}} \\; | awk '{{ print $5 \": \" $9 }}' | sort -n"
    run_command(command)


@cli.command()
def get_disk_usage_in_current_dir():
    """
    This is a command to get disk usage of current directory
    """
    command = "du -h -d 0"
    run_command(command)


@cli.command()
@click.option(
    "--filter/--no-filter",
    nargs=1,
    default=False,
    help="set this option to an integer value to delete everything in the last specified hours",
)
@click.argument("filter_value", default="24", nargs=1)
def docker_prune_everything(filter: bool, filter_value: str):
    """
    This is a command to remove all docker dangling containers, images, volumes, networks
    """
    if filter:
        command = f'docker system prune --filter "until={filter_value}h"'
    else:
        command = "docker system prune --volumes"
    run_command(command)


@cli.command()
@click.argument(
    "image_ids",
    nargs=-1,
    required=True,
)
def remove_multiple_docker_images(image_ids: tuple):
    """
    This is a command to remove multiple docker images which takes image ids as argument
    separated by space
    """
    for image_id in image_ids:
        command = f"docker rmi {image_id}"
        run_command(command)


@cli.command()
@click.option(
    "--python-version",
    nargs=1,
    default="system",
    help="set this option value as the python version for your venv",
)
@click.option(
    "--venv",
    nargs=1,
    default="venv",
    help="set this option value as name of your venv",
)
def create_virtual_env_with_pyenv(python_version: str, venv: str):
    """
    This is a command to create a virtual env and activate it using pyenv
    """
    create_venv_command = f"pyenv virtualenv {python_version} {venv}-{python_version}"
    run_command(create_venv_command)
    activate_venv_command = f"pyenv activate {venv}-{python_version}"
    run_command(activate_venv_command)


def run_command(command: str):
    print(command)
    process = subprocess.run(
        command,
        shell=True,
    )
    return process


@cli.command()
@click.option(
    "--token/--no-token",
    nargs=1,
    default=False,
    help="set this option to your Gitlab personal token to login",
)
@click.option(
    "--hostname",
    nargs=1,
    default="gitlab.com",
    help="set this option value as the group name of your gitlab project",
)
@click.option(
    "--group",
    nargs=1,
    required=True,
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


if __name__ == "__main__":
    cli()
