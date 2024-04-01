import click
from utils import run_command


@click.command()
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
