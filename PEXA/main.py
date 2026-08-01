import asyncio

import click

from reports.csv import export_csv
from reports.html import export_html
from reports.json import export_json
from collectors.audit import run_password_expiration_audit
from hosts.local import LocalHost
from hosts.ssh import SSHHost
from datetime import datetime
from reports.console import print_report


def _build_target_hosts(
    hosts: tuple[str],
    inventory: str | None,
    username: str,
    exclude_localhost: bool,
):
    """Build the list of hosts to audit."""

    target_hosts = []

    if hosts and inventory:
        raise click.UsageError(
            "Use either --host or --inventory, not both."
        )

    if hosts:
        for hostname in hosts:
            target_hosts.append(
                SSHHost(hostname, username)
            )

    elif inventory:
        with open(inventory) as file:
            for line in file:
                parts = line.strip().split(">", 1)
                hostname = parts[0]
                host_user = parts[1] if len(
                    parts) > 1 and parts[1] else username

                if hostname:
                    target_hosts.append(
                        SSHHost(hostname, host_user)
                    )

    if not exclude_localhost:
        target_hosts.append(LocalHost())

    return target_hosts


def _format_duration(seconds: float):
    if seconds < 60:
        duration = f"{seconds:.2f} second(s)"
    elif seconds < 3600:
        duration = f"{seconds / 60:.2f} minute(s)"
    else:
        duration = f"{seconds / 3600:.2f} hour(s)"
    return duration


@click.group()
def cli():
    """PEXA - Python Expiration Auditor."""
    pass


@cli.command(
    help="Audit password expiration on Linux hosts."
)
@click.option(
    "-s",
    "--host",
    multiple=True,
    help="Remote host to audit. Can be specified multiple times.",
)
@click.option(
    "-i",
    "--inventory",
    type=click.Path(exists=True),
    help="Inventory file containing one host per line.",
)
@click.option(
    "-u",
    "--user",
    default="oopser",
    show_default=True,
    help="SSH username.",
)
@click.option(
    "--exclude-localhost",
    is_flag=True,
    help="Skip auditing the local machine.",
)
@click.option(
    "-f",
    "--filter",
    "filter_expression",
    help=(
        "Filter expression. Examples: "
        "'username=hosni days<=7', "
        "'host=web01 never=true'"
    ),
)
@click.option(
    "-e",
    "--export",
    multiple=True,
    type=click.Choice(["json", "csv", "html"], case_sensitive=False),
    help="Export the audit report to the specified format."
)
@click.option(
    "-o",
    "--output",
    default="audit_report",
    show_default=True,
    help="Output filename without extension. Used with --export."
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show detailed execution information."
)
def audit(
    host,
    inventory,
    user,
    exclude_localhost,
    filter_expression,
    export,
    output,
    verbose
):

    target_hosts = _build_target_hosts(
        hosts=host,
        inventory=inventory,
        username=user,
        exclude_localhost=exclude_localhost,
    )

    audit_results, elapsed = asyncio.run(
        run_password_expiration_audit(target_hosts,
                                      filter_expression, verbose)
    )
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print_report(audit_results, _format_duration(elapsed), generated_at)

    if "json" in export:
        export_json(output, audit_results)

    if "csv" in export:
        export_csv(output, audit_results)

    if "html" in export:
        export_html(
            output,
            audit_results,
            _format_duration(elapsed),
            generated_at,
        )


if __name__ == "__main__":
    cli()
