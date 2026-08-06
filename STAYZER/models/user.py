from dataclasses import dataclass, field
from .sshkey import SSHKey


@dataclass
class User:
    username: str
    uid: int
    ssh_keys: list[SSHKey] = field(default_factory=list)
