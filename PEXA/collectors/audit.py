from utils.logger import logger
from collectors.expiration import get_password_expiration
from collectors.passwd import filter_human_users
from models.host import HostModel
from filters.parser import parse_filter_expression, apply_filters
from time import perf_counter


async def run_password_expiration_audit(
    target_hosts: list,
    filter_expression: str,
    verbose: bool
):
    """Execute the password expiration audit."""
    logger.verbose = verbose
    start_time = perf_counter()

    audit_results: list[HostModel] = []

    filters = parse_filter_expression(filter_expression)

    logger.info(
        f"Starting password expiration audit on {len(target_hosts)} host(s)."
    )

    for host in target_hosts:

        logger.info(f"Auditing host '{host.hostname}'.")

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

        host_result = HostModel(hostname=host.hostname)

        for user in users:

            logger.info(
                f"Checking password expiration for '{user.username}'."
            )

            try:
                expires_date, expires_in_days = await get_password_expiration(
                    host,
                    user.username,
                )

            except Exception as e:
                logger.error(
                    f"Unable to check '{user.username}': {e}"
                )
                continue

            user.expires_date = expires_date
            user.expires_in_days = expires_in_days

            if expires_in_days is None:
                logger.info(
                    f"Password never expires."
                )
            else:
                if expires_in_days < 0:
                    user.status = "EXPIRED"
                    logger.info(
                        f"Password expired {expires_in_days} day(s) ago."
                    )
                elif expires_in_days <= 7:
                    user.status = "WARNING"

                    logger.info(
                        f"Password expires in {expires_in_days} day(s)."
                    )
                else:

                    logger.info(
                        f"Password expires in {expires_in_days} day(s)."
                    )
            if filters and not apply_filters(user, host, filters):
                logger.warning(
                    f"'{user.username}' skipped by active filters."
                )
                continue

            host_result.users.append(user)

            logger.success(
                f"Added '{user.username}' to report."
            )

        if host_result.users:
            audit_results.append(host_result)

            logger.success(
                f"Host '{host.hostname}' completed with "
                f"{len(host_result.users)} matching user(s)."
            )
        else:
            logger.warning(
                f"No matching users found on '{host.hostname}'."
            )

    logger.success(
        f"Audit completed successfully. "
        f"{len(audit_results)} host(s) included in the final report."
    )
    elapsed = perf_counter() - start_time

    return audit_results, elapsed
