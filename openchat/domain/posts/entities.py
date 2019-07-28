from dataclasses import dataclass

from datetime import datetime


@dataclass(frozen=True)
class Post:
    post_id: str
    user_id: str
    text: str
    date_time: datetime

