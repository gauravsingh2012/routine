import importlib.util
import os
import subprocess
import click
import shell_routine_alias
from shell_routine_alias.shell_routine_alias import (
    create_virtual_env_and_python_version_with_pyenv_alias,
)


def run_command(
    command: str,
    msg_format_list: list = [],
    capture_output: bool = False,
    text: bool = False,
):
    print(command)
    if msg_format_list:
        print(msg_format_list[0] % msg_format_list[1])

    process = subprocess.run(
        command,
        shell=True,
        executable="/bin/zsh",
        capture_output=capture_output,
        text=text,
    )
    return process


@click.group()
@click.option(
    "--debug/--no-debug", default=False, show_default=True, help="set debug mode"
)
def cli(debug: bool):
    if debug:
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
    This is a command to stop and remove a docker container with the given container_ids
    """
    command = f"docker stop {container_id}"
    run_command(command)
    command = f"docker rm {container_id}"
    run_command(command)


@cli.command()
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


@cli.command()
@click.option(
    "--min_size",
    nargs=1,
    default="100",
    show_default=True,
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


@cli.command()
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


@cli.command()
@click.option(
    "--python-version",
    nargs=1,
    default="system",
    show_default=True,
    help="set this option value as the python version for your venv",
)
@click.option(
    "--venv",
    nargs=1,
    default="venv",
    show_default=True,
    help="set this option value as name of your venv",
)
def create_virtual_env_and_python_version_with_pyenv(python_version: str, venv: str):
    """
    This is a command to create a virtual env and activate it using pyenv
    """
    venv_name = f"{python_version}-{venv}"
    create_venv_command = f"pyenv virtualenv {python_version} {venv_name}"
    run_command(create_venv_command)
    # Create .python-version file and write venv_name to it
    with open(".python-version", "w") as file:
        file.write(venv_name)


@cli.command()
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


@cli.command()
def get_all_kube_contexts():
    """
    This is a command to get all the kube contexts
    """
    command = "kubectl config get-contexts"
    run_command(command)


@cli.command()
@click.option(
    "-k",
    "--kube-context",
    nargs=1,
    required=True,
    show_default=True,
    help="set this option value as the name of the kube context to switch to",
)
@click.option(
    "-n",
    "--namespace",
    nargs=1,
    show_default=True,
    help="set this option value as the namespace of the kube context to switch to",
)
def switch_kube_context(kube_context: str, namespace: str = None):
    """
    This is a command to switch kube context
    """
    command = f"kubectl config use-context {kube_context}"
    run_command(command)
    if namespace:
        command = f"kubectl config set-context --current --namespace={namespace}"
        run_command(command)
    else:
        command = "kubectl config set-context --current --namespace="
        run_command(command)


@cli.command()
@click.argument("kube_context", default="", nargs=1)
def delete_kube_context(kube_context: str):
    """
    This is a command to delete kube context
    """
    command = f"kubectl config delete-context {kube_context}"
    run_command(command)


@cli.command()
@click.argument("current_kube_context", default="", nargs=1)
@click.argument("new_kube_context", default="", nargs=1)
def rename_kube_context(current_kube_context: str, new_kube_context: str):
    """
    This is a command to rename kube context
    """
    command = f"kubectl config rename-context {current_kube_context} {new_kube_context}"
    run_command(command)


@cli.command()
@click.option(
    "--profile",
    nargs=1,
    show_default=True,
    help="set this option value as the aws profile name",
)
@click.option(
    "--region",
    nargs=1,
    show_default=True,
    help="set this option value as the aws region name",
)
@click.option(
    "--cluster",
    nargs=1,
    show_default=True,
    help="set this option value as the aws eks cluster name",
)
def add_aws_eks_kubeconfig(profile: str, region: str, cluster: str):
    """
    This is a command to update the kubeconfig of the aws eks cluster
    """
    command = (
        f"source ~/.zshrc && export-aws-credentials --profile {profile} && "
        f"AWS_PROFILE={profile} aws eks --region {region} "
        f"update-kubeconfig --name {cluster}"
    )
    run_command(command)
    current_context_command = "kubectl config current-context"
    current_context_command_output = run_command(
        current_context_command, [], capture_output=True, text=True
    )
    current_context = current_context_command_output.stdout.strip()
    rename_kube_context_command = (
        f"kubectl config rename-context {current_context} {profile}-{cluster}"
    )
    run_command(rename_kube_context_command)


@cli.command()
def append_aliases_to_zshrc():
    """
    This is a command to append shell aliases to the zshrc file defined in the shell_routine_alias module
    """
    shell_function = ""
    home_dir = os.path.expanduser("~")
    zshrc_path = os.path.join(home_dir, ".zshrc_aliases")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Current directory:", current_dir)

    # Load the module dynamically
    module_name = "shell_routine_alias.shell_routine_alias"
    spec = importlib.util.find_spec(module_name)
    mymodule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mymodule)

    # Get all members (functions, classes, etc.) of the module shell_routine_alias.shell_routine_alias
    members = vars(mymodule).items()
    with open(zshrc_path, "w") as file:
        # Iterate over the members and filter out functions
        for name, member in members:
            if (
                callable(member)
                and hasattr(member, "__module__")
                and member.__module__ == mymodule.__name__
            ):
                # Check if the member is a function and belongs to the specified module
                print(f"Calling function: {name}")

                shell_function = member(current_dir)
                print(f"Result: {shell_function}")
                print("=" * 50)

                file.write("\n")
                file.write(shell_function.strip())
                file.write("\n")


@cli.command()
def update_zsh_profile_env_files_in_routine_project():
    """
    This is a command to update the zsh profile env files in the routine project
    """
    home_dir = os.path.expanduser("~")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    command = (
        f"cp {home_dir}/.zshrc {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc && "
        f"cp {home_dir}/.zshrc_path_variables {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_path_variables && "
        f"cp {home_dir}/.zshrc_config_variables {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_config_variables &&"
        f"cp {home_dir}/.zshrc_aliases {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_aliases"
    )
    run_command(command)


@cli.command()
def setup_zsh_profile_env_files_in_home_directory():
    """
    This is a command to update the zsh profile env files in the routine project
    """
    home_dir = os.path.expanduser("~")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    command = (
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc {home_dir}/.zshrc1 && "
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_path_variables {home_dir}/.zshrc_path_variables1 && "
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_config_variables {home_dir}/.zshrc_config_variables1 &&"
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_aliases {home_dir}/.zshrc_aliases1"
    )
    run_command(command)


if __name__ == "__main__":
    cli()
