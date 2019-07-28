
from dataclasses import dataclass
from uuid import uuid4

from openchat.domain.users.entities import User


@dataclass(frozen=True)
class UserBuilder:
    id: str = None
    username: str = "Username"
    password: str = "password"
    about: str = "About"

    def build(self) -> User:
        return User(
            id=self.id or str(uuid4()),
            username=self.username,
            password=self.password,
            about=self.about)
