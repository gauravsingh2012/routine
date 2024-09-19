import click
from utils import run_command


@click.command()
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
        "source ~/.zshrc && unset-env-vars AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY "
        "AWS_SESSION_TOKEN AWS_EXPIRATION && "
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
        f"source ~/.zshrc && unset-env-vars AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY "
        f"AWS_SESSION_TOKEN AWS_EXPIRATION && "
        f"AWS_PROFILE={profile} kubectl config rename-context {current_context} {profile}-{cluster}"
    )
    run_command(rename_kube_context_command)


@click.command()
@click.argument("kube_context", default="", nargs=1)
def delete_kube_context(kube_context: str):
    """
    This is a command to delete kube context
    """
    command = f"kubectl config delete-context {kube_context}"
    run_command(command)


@click.command()
def get_all_kube_contexts():
    """
    This is a command to get all the kube contexts
    """
    command = "kubectl config get-contexts"
    run_command(command)


@click.command()
@click.argument("current_kube_context", default="", nargs=1)
@click.argument("new_kube_context", default="", nargs=1)
def rename_kube_context(current_kube_context: str, new_kube_context: str):
    """
    This is a command to rename kube context
    """
    command = f"kubectl config rename-context {current_kube_context} {new_kube_context}"
    run_command(command)


@click.command()
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


@click.command()
@click.option(
    "-n",
    "--namespace",
    nargs=1,
    required=True,
    show_default=True,
    help="set this option value as the namespace of the kube context to switch to",
)
@click.option(
    "-p",
    "--pod-name",
    nargs=1,
    required=True,
    show_default=True,
    help="set this option value as the name of the pod that you want to delete",
)
def force_delete_pod(namespace: str, pod_name: str):
    """
    This is a command to switch kube context
    """
    command = f"kubectl delete pod --grace-period=0 --force --namespace {namespace} {pod_name}"
    run_command(command)


@click.command()
@click.option(
    "-n",
    "--namespace",
    nargs=1,
    required=True,
    show_default=True,
    help="set this option value as the namespace of the kube context to switch to",
)
@click.option(
    "-d",
    "--deployment-name",
    nargs=1,
    required=True,
    show_default=True,
    help="set this option value as the deployment name of the pod",
)
@click.option(
    "-r",
    "--replica-count",
    nargs=1,
    required=True,
    show_default=True,
    help="set this option value as the number of replicas that you want to scale to",
)
def scale_deployment_replicas(namespace: str, deployment_name: str, replica_count: str):
    """
    This is a command to switch kube context
    """
    command = (
        f"kubectl -n {namespace} scale {deployment_name} --replicas={replica_count}"
    )
    run_command(command)
