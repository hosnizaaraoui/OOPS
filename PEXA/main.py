import os

from collectors.passwd import filter_human_users
from collectors.expiration import get_password_expiration
from reports.console import print_report
from hosts.local import LocalHost


def main():
    hosts = [LocalHost()]
    for host in hosts:
        with open("/etc/passwd") as f:
            users = filter_human_users(f.readlines())

        hostname = os.uname().nodename

        for user in users:
            user.host = hostname
            user.expires = get_password_expiration(host, user.username)

        print_report(users)


if __name__ == "__main__":
    main()
