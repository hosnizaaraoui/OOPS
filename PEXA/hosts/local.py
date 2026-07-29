import subprocess

from .base import Host


class LocalHost(Host):

    def execute(self, command: list[str]) -> str:
        return subprocess.check_output(
            command,
            text=True
        )
