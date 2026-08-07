import click
from time import perf_counter

from collectors.passwd import filter_human_users
from filters.parser import parse_filter_expression
from models.host import HostModel
from models.sshkey import SSHKey
from utils.logger import logger


def check_duplications(trust_results: list[HostModel]):
    """Detect SSH keys that are authorized on multiple accounts."""

    fingerprints: dict[str, list[tuple[str, str]]] = {}

    for host in trust_results:
        for user in host.users:
            for key in user.ssh_keys:
                fingerprints.setdefault(key.fingerprint, []).append(
                    (host.hostname, user.username)
                )

    for fingerprint, occurrences in fingerprints.items():

        if len(occurrences) < 2:
            continue

        logger.warning(
            f"Duplicate SSH key detected ({len(occurrences)} occurrences)"
        )

        click.secho(
            f".... Fingerprint : SHA256:{fingerprint}",
            fg="yellow",
        )

        click.secho(
            ".... Locations:",
            fg="yellow",
        )

        for hostname, username in occurrences:
            click.secho(
                f"    - {hostname}\n"
                f"      User : {username}",
                fg="yellow",
            )

        print()


async def analyze_ssh_trust(
    target_hosts: list,
    filter_expression: str,
    verbose: bool,
):
    """Execute the SSH trust analysis."""

    logger.verbose = verbose
    start_time = perf_counter()

    trust_results: list[HostModel] = []

    filters = parse_filter_expression(filter_expression)

    logger.info(
        f"Starting SSH trust analysis on {len(target_hosts)} host(s)."
    )

    for host in target_hosts:

        logger.info(f"Analyzing host '{host.hostname}'.")

        try:
            passwd_content = await host.read_file("/etc/passwd")
        except Exception as e:
            logger.error(
                f"Failed to read /etc/passwd from "
                f"'{host.hostname}': {e}"
            )
            continue

        users = filter_human_users(passwd_content)

        logger.success(
            f"Found {len(users)} human user(s) on '{host.hostname}'."
        )

        # users = apply_filters(users, filters)

        host_result = HostModel(hostname=host.hostname)

        for user in users:

            logger.info(
                f"Inspecting authorized_keys for "
                f"'{user.username}'."
            )

            try:

                await host.read_file(
                    f"/home/{user.username}/.ssh/authorized_keys"
                )

                output = await host.execute(
                    "sudo ssh-keygen "
                    f"-lf /home/{user.username}/.ssh/authorized_keys "
                    "-E sha256"
                )

                for line in output.splitlines():

                    fields = line.split()

                    ssh_key = SSHKey(
                        fingerprint=fields[1],
                        type=fields[3],
                        comment=" ".join(fields[2:-1]),
                    )

                    user.ssh_keys.append(ssh_key)

                key_count = len(user.ssh_keys)
                key_label = "Key" if key_count == 1 else "Keys"

                logger.success(
                    f"User: {user.username}\n"
                    f".... SSH Keys : {key_count} {key_label}"
                )

                if logger.verbose:

                    for index, key in enumerate(user.ssh_keys, start=1):

                        click.secho(
                            f".... Key #{index}",
                            fg="green",
                        )

                        click.secho(
                            f"       Type        : {key.type}",
                            fg="green",
                        )

                        click.secho(
                            f"       Fingerprint : "
                            f"{key.fingerprint}",
                            fg="green",
                        )

                        click.secho(
                            f"       Comment     : "
                            f"{key.comment}",
                            fg="green",
                        )

                    print()

                host_result.users.append(user)

            except FileNotFoundError:
                logger.info(
                    f"User '{user.username}' has no SSH "
                    f"authorized keys."
                )

            except PermissionError:
                logger.warning(
                    f"Permission denied while reading SSH "
                    f"keys for '{user.username}'."
                )

            except Exception as e:
                logger.error(
                    f"Failed to analyze SSH trust for "
                    f"'{user.username}': {e}"
                )

        trust_results.append(host_result)

    elapsed = perf_counter() - start_time

    return trust_results, elapsed
