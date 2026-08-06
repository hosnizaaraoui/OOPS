from dataclasses import dataclass


@dataclass
class SSHKey:
    fingerprint: str = None
    type: str = None
    comment: str = None
