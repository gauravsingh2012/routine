import subprocess


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
