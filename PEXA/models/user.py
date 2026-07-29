from dataclasses import dataclass


@dataclass
class User:
    username: str
    uid: int
    expires: str = "Unknown"
    host: str = ""
