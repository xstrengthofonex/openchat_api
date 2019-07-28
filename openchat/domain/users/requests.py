from dataclasses import dataclass

from openchat.domain.users.entities import User


@dataclass(frozen=True)
class RegistrationData:
    username: str
    password: str
    about: str


@dataclass(frozen=True)
class UserCredentials:
    username: str
    password: str

    def matches(self, user: User) -> bool:
        return user.username == self.username and user.password == self.password
