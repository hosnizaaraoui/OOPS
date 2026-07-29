import asyncssh

from .base import Host


class SSHHost(Host):

    def __init__(self, hostname: str, username: str):
        self.hostname = hostname
        self.username = username

    async def execute(self, command) -> str:
        try:
            async with asyncssh.connect(
                self.hostname,
                username=self.username,
                known_hosts=None
            ) as conn:
                result = await conn.run(
                    " ".join(command),
                    check=True
                )
                return (result.stdout)

        except:
            raise

    async def load_file(self, file: str):
        try:
            async with asyncssh.connect(
                self.hostname,
                username=self.username,
                known_hosts=None
            ) as conn:
                result = await conn.run(
                    f" cat {file}",
                    check=True
                )
            return result.stdout.splitlines()

        except:
            raise
