import shlex
from datetime import datetime


def parse_filter_expression(expression: str) -> list[tuple[str, str, str]]:
    """
    Parse expressions like:
        username=hosni days<=7 host=web01 never=true

    Returns a list of tuples:
        [(field, operator, value)]
    """

    if not expression:
        return []

    operators = ["<=", ">=", "!=", "<", ">", "="]

    filters = []

    for token in shlex.split(expression):
        for op in operators:
            if op in token:
                field, value = token.split(op, 1)
                filters.append((field.strip(), op, value.strip()))
                break
        else:
            raise ValueError(f"Invalid filter token: {token}")

    return filters


def apply_filters(user, host, filters: list[tuple[str, str, str]]) -> bool:
    """Return True if the user matches all filters."""

    for field, op, value in filters:

        # -----------------------------
        # Username
        # -----------------------------
        if field == "username":
            current = user.username

        # -----------------------------
        # Hostname
        # -----------------------------
        elif field == "host":
            current = host.hostname

        # -----------------------------
        # Remaining days
        # -----------------------------
        elif field == "days":
            if user.expires_in_days is None:
                return False

            current = user.expires_in_days
            value = int(value)

        # -----------------------------
        # Exact expiration date
        # -----------------------------
        elif field == "date":
            if user.expires_date is None:
                return False

            current = user.expires_date
            value = datetime.strptime(value, "%Y-%m-%d").date()

        # -----------------------------
        # Never expires
        # -----------------------------
        elif field == "never":
            current = user.expires_in_days is None
            value = value.lower() == "true"

        else:
            raise ValueError(f"Unknown filter field: {field}")

        # -----------------------------
        # Comparison logic
        # -----------------------------
        if op == "=" and current != value:
            return False
        elif op == "!=" and current == value:
            return False
        elif op == "<" and current >= value:
            return False
        elif op == "<=" and current > value:
            return False
        elif op == ">" and current <= value:
            return False
        elif op == ">=" and current < value:
            return False

    return True
