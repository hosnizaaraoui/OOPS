from datetime import datetime, date
from hosts.base import Host


async def get_password_expiration(host: Host, username: str) -> str:
    try:
        output = await host.execute(
            ["sudo", "chage", "-li", username])
        for line in output.splitlines():
            if line.startswith("Password expires"):

                expires = line.split(":", 1)[1].strip()

                if expires == "never":
                    return None, None

                today = date.today()
                exp = datetime.strptime(
                    expires,
                    "%Y-%m-%d"
                ).date()

                return exp, (exp - today).days

    except Exception:
        pass

    return "Unknown"
