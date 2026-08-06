import click

from models.host import HostModel


def print_report(hosts: list[HostModel], duration, generation_time):
    """Print a formatted password expiration audit report."""

    total_users = sum(len(host.users) for host in hosts)

    safe_count = 0
    warning_count = 0
    expired_count = 0
    never_count = 0

    click.secho("\n" + "=" * 72, fg="cyan")
    click.secho(" PEXA - Password Expiration Audit Report",
                fg="cyan", bold=True)
    click.secho("=" * 72, fg="cyan")
    click.echo(f"Generated On....: {generation_time}")
    click.echo(f"Duration........: {duration}\n")
    click.echo(f"Hosts Audited...: {len(hosts)}")
    click.echo(f"Users Audited...: {total_users}")

    click.secho("=" * 72, fg="cyan")

    for host in hosts:

        click.echo()
        click.secho(f"Host: {host.hostname}", fg="blue", bold=True)
        click.echo(f"Matching Users : {len(host.users)}")

        click.echo("-" * 72)

        click.echo(
            f"{'Username':<20}"
            f"{'UID':<10}"
            f"{'STATUS':<12}"
            f"{'Password Expires':<20}"
        )

        click.echo("-" * 72)

        for user in host.users:

            if user.expires_in_days is None:
                expires = "Never"
                never_count += 1
                safe_count += 1

                click.secho(
                    f"{user.username:<20}"
                    f"{user.uid:<10}"
                    f"{user.status:<12}"
                    f"{expires:<20}",
                    fg="green",
                )

            elif user.expires_in_days < 0:
                expires = f"Expired ({abs(user.expires_in_days)} day(s) ago)"
                expired_count += 1

                click.secho(
                    f"{user.username:<20}"
                    f"{user.uid:<10}"
                    f"{user.status:<12}"
                    f"{expires:<20}",
                    fg="red",
                    bold=True,
                )

            elif user.expires_in_days <= 7:
                if user.expires_in_days == 0:
                    expires = f"Expires Today"
                else:
                    expires = f"{user.expires_in_days} day(s)"

                warning_count += 1

                click.secho(
                    f"{user.username:<20}"
                    f"{user.uid:<10}"
                    f"{user.status:<12}"
                    f"{expires:<20}",
                    fg="yellow",
                    bold=True,
                )

            else:
                expires = f"{user.expires_in_days} day(s)"

                safe_count += 1

                click.echo(
                    f"{user.username:<20}"
                    f"{user.uid:<10}"
                    f"{user.status:<12}"
                    f"{expires:<20}"
                )

        click.echo("-" * 72)
    click.secho("\nSummary", fg="cyan", bold=True)
    click.echo("-" * 72)

    click.secho(f"Safe Accounts...........: {safe_count}", fg="green")
    click.secho(f"Warning Accounts........: {warning_count}", fg="yellow")
    click.secho(f"Expired Accounts........: {expired_count}\n", fg="red")

    click.secho(f"Passwords Never Expire..: {never_count}\n", fg="green")

    if expired_count:
        click.secho(f"Overall Result........: CRITICAL", fg="red")
    elif warning_count:
        click.secho(f"Overall Result........: ATTENTION REQUIRED", fg="yellow")
    else:
        click.secho(f"Overall Result........: HEALTHY", fg="red")

    click.secho("\nAudit completed successfully.\n", fg="green", bold=True)
