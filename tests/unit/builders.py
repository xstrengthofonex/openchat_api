from dataclasses import dataclass
from datetime import datetime

from openchat.entities.documents import Document
from openchat.entities.users import User


@dataclass
class UserBuilder:
    username: str = "username"
    password: str = "password"
    about: str = "about"

    def build(self):
        return User(
            username=self.username,
            password=self.password,
            about=self.about)


@dataclass(frozen=True)
class DocumentBuilder:
    id: int = 1
    username: str = "Username"
    text: str = "Some text"
    date_time: datetime = None

    def build(self):
        return Document(
            id=self.id,
            username=self.username,
            text=self.text,
            date_time=self.date_time or datetime.now())