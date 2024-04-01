import click
from utils import run_command


@click.command()
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


@click.command()
def get_disk_usage_in_current_dir():
    """
    This is a command to get disk usage of current directory
    """
    command = "du -h -d 0"
    run_command(command)
