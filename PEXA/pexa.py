import subprocess


def get_password_expiration(user: str) -> str:
    """Return the password expiration date for a given user."""

    output = subprocess.check_output(
        ["chage", "-l", user],
        text=True
    )

    for line in output.splitlines():
        if line.startswith("Password expires"):
            return line.split(":", 1)[1].strip()

    return "Unknown"


def filter_human_users(lines: list[str]) -> list[dict]:
    """Return only regular user accounts (UID >= 1000)."""

    users = []

    for line in lines:
        fields = line.strip().split(":")
        uid = int(fields[2])

        if 1000 <= uid < 60000:
            users.append({
                "username": fields[0],
                "uid": uid
            })

    return users


def collect_password_expirations(users: list[dict]) -> list[dict]:
    """Collect password expiration information for each user."""

    report = []

    for user in users:
        report.append({
            "username": user["username"],
            "uid": user["uid"],
            "expires": get_password_expiration(user["username"])
        })

    return report


def print_report(report: list[dict]) -> None:
    """Print a formatted password expiration report."""

    print(f"\nFound {len(report)} user(s)\n")

    print(f"{'Username':<20}{'UID':<10}{'Password Expires'}")
    print("-" * 60)

    for user in report:
        print(
            f"{user['username']:<20}"
            f"{user['uid']:<10}"
            f"{user['expires']}"
        )


def main():
    with open("/etc/passwd") as passwd_file:
        users = filter_human_users(passwd_file.readlines())

    report = collect_password_expirations(users)
    print_report(report)


if __name__ == "__main__":
    main()
