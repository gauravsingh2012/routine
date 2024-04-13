from importlib import util
import os
import subprocess


def run_command(
    command: str,
    msg_format_list: list = [],
    capture_output: bool = False,
    text: bool = False,
    cwd: str = None,
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
        cwd=cwd,
    )
    return process


def setup_zsh_profile_env_files_in_home_directory_utility():
    home_dir = os.path.expanduser("~")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    command = (
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc {home_dir}/.zshrc && "
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_aws_variables {home_dir}/.zshrc_aws_variables && "
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_path_variables {home_dir}/.zshrc_path_variables && "
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_config_variables {home_dir}/.zshrc_config_variables &&"
        f"cp {current_dir}/zsh_profile_env_files/zsh_profile_env_files.zshrc_aliases {home_dir}/.zshrc_aliases && "
        f"cp {current_dir}/zsh_profile_env_files/starship.toml {home_dir}/.config/starship.toml"
    )
    run_command(command)


def append_aliases_to_zshrc_utility():
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
        file.write("# shell aliases")
        file.write("\n")
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
