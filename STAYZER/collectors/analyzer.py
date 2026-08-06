from time import perf_counter

from models.sshkey import SSHKey
from collectors.passwd import filter_human_users
from filters.parser import parse_filter_expression
from models.host import HostModel
from utils.logger import logger


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
                f"Failed to read /etc/passwd from '{host.hostname}': {e}"
            )
            continue

        users = filter_human_users(passwd_content)

        logger.success(
            f"Found {len(users)} human user(s) on '{host.hostname}'."
        )

        # Apply user filters if provided
        # users = apply_filters(users, filters)

        host_result = HostModel(hostname=host.hostname)

        for user in users:

            logger.info(
                f"Inspecting authorized_keys for '{user.username}'."
            )

            try:
                authorized_keys = await host.read_file(
                    f"/home/{user.username}/.ssh/authorized_keys"
                )

                # TODO:
                # Iterate over every authorized key instead of only the first.
                # Each user may have multiple authorized public keys.
                logger.success(
                    f"Found {len(authorized_keys)} SSH Authorized Keys")
                for authorized_key in authorized_keys:
                    fields = authorized_key.split()

                    type = fields[0]
                    fingerprint = fields[1]
                    comment = (
                        " ".join(fields[2:]) if len(fields) > 2 else ""
                    )
                    ssh_key = SSHKey(fingerprint=fingerprint,
                                     type=type, comment=comment)

                    user.ssh_keys.append(ssh_key)
                    logger.success(user)

                    host_result.users.append(user)

            except FileNotFoundError:
                logger.info(
                    f"User '{user.username}' has no SSH authorized keys."
                )
                continue

            except PermissionError:
                logger.warning(
                    f"Permission denied while reading SSH keys for "
                    f"'{user.username}'."
                )
                continue

            except Exception as e:
                logger.error(
                    f"Failed to analyze SSH trust for "
                    f"'{user.username}': {e}"
                )
                continue

        trust_results.append(host_result)

    elapsed = perf_counter() - start_time

    return trust_results, elapsed
