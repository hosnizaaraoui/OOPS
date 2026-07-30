from dataclasses import dataclass, field

from .user import User


@dataclass
class HostModel:
    hostname: str = "Unknown"
    users: list[User] = field(default_factory=list)
