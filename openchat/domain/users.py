from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    username: str
    password: str
    about: str


@dataclass(frozen=True)
class RegistrationData:
    username: str
    password: str
    about: str


class UserService:
    async def create_user(self, registration_data: RegistrationData) -> User:
        raise NotImplementedError
