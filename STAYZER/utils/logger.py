import click
from datetime import datetime


class Logger:

    def __init__(self):
        self.verbose = False

    def configure(self, verbose: bool):
        self.verbose = verbose

    def _log(self, level: str, color: str, message: str):
        if not self.verbose:
            return

        now = datetime.now().strftime("%H:%M:%S")
        click.secho(
            f"[{now}] {level:<7} {message}",
            fg=color,
        )

    def info(self, message: str):
        self._log("INFO", "blue", message)

    def success(self, message: str):
        self._log("SUCCESS", "green", message)

    def warning(self, message: str):
        self._log("WARNING", "yellow", message)

    def error(self, message: str):
        self._log("ERROR", "red", message)


logger = Logger()
