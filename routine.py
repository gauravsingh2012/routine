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
    "--filter/--no-dilter",
    nargs=1,
    default=False,
    help="set this option to an integer value to delete everything in the last specified hours",
)
@click.argument("filter_value", default="24")
def docker_prune_everything(filter: bool, filter_value: str):
    """
    This is a command to remove all docker dangling containers, images, volumes, networks
    """
    if filter:
        command = f'docker system prune --volumes --filter "until={filter_value}h"'
    else:
        command = "docker system prune --volumes"
    run_command(command)


def run_command(command: str):
    print(command)
    process = subprocess.run(
        command,
        shell=True,
    )
    return process


if __name__ == "__main__":
    cli()
