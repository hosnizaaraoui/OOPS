from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    username: str
    uid: int
    expires_date: date | None = None
    expires_in_days: int | None = None
    status: str = "SAFE"
