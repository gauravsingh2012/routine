from importlib import util
import os
import click
from utils import run_command


@click.command()
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
    spec = util.find_spec(module_name)
    mymodule = util.module_from_spec(spec)
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


@click.command()
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


@click.command()
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
