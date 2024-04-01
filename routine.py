from brew_routine import run_brew_update_upgrade_and_cleanup
import click
from disk_routine import find_files_taking_disk_space, get_disk_usage_in_current_dir
from docker_routine import (
    docker_prune_everything,
    go_inside_docker_container,
    list_ip_address_of_all_running_containers,
    remove_multiple_docker_images,
    stop_and_remove_docker_container,
    stop_and_remove_multiple_docker_containers,
)
from git_routine import clone_all_git_lab_projects
from kubernetes_routine import (
    add_aws_eks_kubeconfig,
    delete_kube_context,
    get_all_kube_contexts,
    rename_kube_context,
    switch_kube_context,
)
from python_routine import create_virtual_env_and_python_version_with_pyenv

from zsh_routine import (
    append_aliases_to_zshrc,
    setup_zsh_profile_env_files_in_home_directory,
    update_zsh_profile_env_files_in_routine_project,
)


@click.group()
@click.option(
    "--debug/--no-debug", default=False, show_default=True, help="set debug mode"
)
def cli(debug: bool):
    if debug:
        click.echo("Debug mode is %s" % ("on" if debug else "off"))


def add_click_commands():
    cli.add_command(append_aliases_to_zshrc)
    cli.add_command(add_aws_eks_kubeconfig)
    cli.add_command(clone_all_git_lab_projects)
    cli.add_command(delete_kube_context)
    cli.add_command(docker_prune_everything)
    cli.add_command(find_files_taking_disk_space)
    cli.add_command(get_all_kube_contexts)
    cli.add_command(get_disk_usage_in_current_dir)
    cli.add_command(go_inside_docker_container)
    cli.add_command(list_ip_address_of_all_running_containers)
    cli.add_command(remove_multiple_docker_images)
    cli.add_command(rename_kube_context)
    cli.add_command(run_brew_update_upgrade_and_cleanup)
    cli.add_command(setup_zsh_profile_env_files_in_home_directory)
    cli.add_command(stop_and_remove_docker_container)
    cli.add_command(stop_and_remove_multiple_docker_containers)
    cli.add_command(switch_kube_context)
    cli.add_command(update_zsh_profile_env_files_in_routine_project)
    cli.add_command(create_virtual_env_and_python_version_with_pyenv)


add_click_commands()

if __name__ == "__main__":
    cli()
