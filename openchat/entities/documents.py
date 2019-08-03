from dataclasses import dataclass

from datetime import datetime


@dataclass(frozen=True)
class Document:
    id: int
    username: str
    text: str
    date_time: datetime
