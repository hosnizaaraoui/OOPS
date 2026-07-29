from datetime import datetime, date
import subprocess

from hosts.local import LocalHost


def get_password_expiration(host: LocalHost, username: str) -> str:
    try:
        output = host.execute(
            ["chage", "-li", username])

        for line in output.splitlines():
            if line.startswith("Password expires"):

                expires = line.split(":", 1)[1].strip()

                if expires == "never":
                    return expires

                today = date.today()
                exp = datetime.strptime(
                    expires,
                    "%Y-%m-%d"
                ).date()

                return f"{(exp - today).days} day(s)"

    except Exception:
        pass

    return "Unknown"
