from models.user import User


def print_report(users: list[User]):

    print(f"\nFound {len(users)} user(s)\n")

    print(
        f"{'Host':<20}"
        f"{'Username':<20}"
        f"{'UID':<10}"
        "Password Expires"
    )

    print("-" * 70)

    for user in users:
        print(
            f"{user.host:<20}"
            f"{user.username:<20}"
            f"{user.uid:<10}"
            f"{user.expires}"
        )
