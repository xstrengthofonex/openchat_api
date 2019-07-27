
from dataclasses import dataclass
from uuid import uuid4

from openchat.domain.users import User


@dataclass(frozen=True)
class UserBuilder:
    id: str = str(uuid4())
    username: str = "Username"
    password: str = "password"
    about: str = "About"

    def build(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            password=self.password,
            about=self.about)
