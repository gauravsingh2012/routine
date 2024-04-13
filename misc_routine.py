import os
import click
from utils import run_command


@click.command()
def get_terminal_size():
    """
    This is a command to get the terminal size
    """
    command = "stty size"
    run_command(command)


@click.command()
@click.option(
    "--profile-name",
    nargs=1,
    required=True,
    show_default=True,
    help="set profile name",
)
@click.option(
    "--aws-account-id",
    nargs=1,
    required=True,
    show_default=True,
    help="set aws account id",
)
@click.option(
    "--sso-start-url",
    nargs=1,
    default="https://sso-<aws-account-name>.awsapps.com/start",
    show_default=True,
    help="set sso start url",
)
@click.option(
    "--role-name",
    nargs=1,
    default="Administrator",
    show_default=True,
    help="set role name",
)
@click.option(
    "--region",
    nargs=1,
    default="us-east-1",
    show_default=True,
    help="set aws default region",
)
@click.option(
    "--sso-region",
    nargs=1,
    default="us-east-1",
    show_default=True,
    help="set sso region",
)
def add_aws_config_profile(
    profile_name: str,
    aws_account_id: str,
    sso_start_url: str,
    role_name: str,
    region: str,
    sso_region: str,
):
    """
    This is a command to add an aws profile to ~/.aws/config
    """
    profile_config = f"""
[profile {profile_name}]
credential_process = aws-sso-util credential-process --profile {profile_name}
sso_start_url = {sso_start_url}
sso_account_id = {aws_account_id}
sso_role_name = {role_name}
region = {region}
output = json
sso_region = {sso_region}
sso_registration_scopes = sso:account:access
    """

    # Get the home directory
    home_dir = os.path.expanduser("~")
    aws_config_path = os.path.join(home_dir, ".aws", "config")

    # Append the profile configuration to the config file
    with open(aws_config_path, "a") as config_file:
        config_file.write(profile_config)
