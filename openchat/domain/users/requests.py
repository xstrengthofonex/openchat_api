from dataclasses import dataclass


@dataclass(frozen=True)
class RegistrationData:
    username: str
    password: str
    about: str
