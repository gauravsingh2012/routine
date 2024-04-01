import click
from utils import run_command


@click.command()
@click.option(
    "--filter/--no-filter",
    nargs=1,
    default=False,
    show_default=True,
    help="set this option to an integer value to delete everything in the last specified hours",
)
@click.argument("filter_value", default="24", nargs=1)
def docker_prune_everything(filter: bool, filter_value: str):
    """
    This is a command to remove all docker dangling containers, images, volumes, networks
    """
    if filter:
        command = f'docker system prune -a --filter "until={filter_value}h"'
    else:
        command = "docker system prune -a --volumes"
    run_command(command)


@click.command()
@click.argument("container_id", nargs=1)
def go_inside_docker_container(container_id: str):
    """
    This is a command to start a shell inside the docker container with the given container_id
    """
    command = f"docker exec -it {container_id} bash"
    run_command(command)


@click.command()
def list_ip_address_of_all_running_containers():
    """
    This is a command to list all the ip addresses of all the running containers
    """
    msg_format = "%-51s%-101s%s"
    msg_format_values = (
        "CONTAINER NAME",
        "CONTAINER IMAGE NAME",
        "CONTAINER IP ADDRESS",
    )
    command = 'docker inspect $(docker ps -q ) --format=\'{{ printf "%-50s" .Name}} {{printf "%-100s" .Config.Image}} {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}\''
    run_command(command, [msg_format, msg_format_values])


@click.command()
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


@click.command()
@click.argument("container_id", nargs=1)
def stop_and_remove_docker_container(container_id: str):
    """
    This is a command to stop and remove a docker container with the given container_ids
    """
    command = f"docker stop {container_id}"
    run_command(command)
    command = f"docker rm {container_id}"
    run_command(command)


@click.command()
@click.argument(
    "container_ids",
    nargs=-1,
    required=True,
)
def stop_and_remove_multiple_docker_containers(container_ids: tuple):
    """
    This is a command to remove multiple docker images which takes image ids as argument
    separated by space
    """
    for container_id in container_ids:
        command = f"docker stop {container_id}"
        run_command(command)
        command = f"docker rm {container_id}"
        run_command(command)
