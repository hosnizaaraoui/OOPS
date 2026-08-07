import json
from dataclasses import asdict

from utils.logger import logger
from models.host import HostModel


def export_json(output: str, trust_results: list[HostModel]):
    """Export audit results to a JSON file."""
    logger.verbose = True

    if not output.endswith(".json"):
        output += ".json"

    with open(output, "w") as file:
        json.dump(
            [asdict(host) for host in trust_results],
            file,
            indent=4,
            default=str,
        )

    logger.success(f"JSON report written to '{output}'")
