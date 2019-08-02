from dataclasses import dataclass

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
