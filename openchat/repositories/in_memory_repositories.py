from typing import Dict, Tuple

from openchat.entities.users import User
from openchat.usecases.repositories import Repository


class InMemoryRepository(Repository):
    def __init__(self):
        self._users: Dict[str, User] = dict()

    async def add_user(self, user: User) -> None:
        self._users[user.username] = user

    async def get_user(self, username: str) -> User:
        return self._users.get(username)

    async def get_all_users(self) -> Tuple[User]:
        return tuple(self._users.values())
