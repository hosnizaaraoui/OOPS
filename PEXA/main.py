import asyncio
import os

from collectors.passwd import filter_human_users
from collectors.expiration import get_password_expiration
from reports.console import print_report
from hosts.local import LocalHost
from hosts.ssh import SSHHost


async def main():
    host1 = SSHHost("172.17.0.2", 'oopser')
    hosts = [LocalHost(), host1]
    full_register = []
    for host in hosts:
        users = filter_human_users(await host.load_file("/etc/passwd"))
        for user in users:
            user.host = host.hostname
            user.expires = await get_password_expiration(host, user.username)
            full_register.append(user)
    print_report(full_register)


if __name__ == "__main__":
    asyncio.run(main())
