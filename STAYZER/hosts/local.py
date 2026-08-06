import os
import subprocess

from .base import Host


class LocalHost(Host):
    def __init__(self):
        self.hostname = os.uname().nodename

    async def execute(self, command: list[str]) -> str:
        return subprocess.check_output(
            command,
            text=True
        )

    async def read_file(self, file: str):
        with open(file) as f:
            return f.readlines()
