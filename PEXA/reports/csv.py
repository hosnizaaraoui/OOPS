import csv

from utils.logger import logger
from models.host import HostModel


def export_csv(output: str, audit_results: list[HostModel]):
    """Export audit results to a CSV file."""
    logger.verbose = True
    if not output.endswith(".csv"):
        output += ".csv"

    with open(output, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Hostname",
            "Username",
            "UID",
            "Status",
            "Expires In Days",
            "Expiration Date",
        ])

        for host in audit_results:
            for user in host.users:
                writer.writerow([
                    host.hostname,
                    user.username,
                    user.uid,
                    user.status,
                    user.expires_in_days,
                    user.expires_date,
                ])
    logger.success(f"CSV report written to '{output}'")
