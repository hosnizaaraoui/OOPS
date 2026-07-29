from models.user import User


def filter_human_users(lines: list[str]) -> list[User]:
    users = []

    for line in lines:
        fields = line.strip().split(":")
        uid = int(fields[2])

        if 1000 <= uid < 60000:
            users.append(
                User(
                    username=fields[0],
                    uid=uid
                )
            )

    return users
