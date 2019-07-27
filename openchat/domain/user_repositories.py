from typing import Dict

from openchat.domain.user_entities import User


class UserRepository:
    def __init__(self):
        self.users: Dict[str, User] = dict()

    async def add(self, user: User) -> None:
        self.users[user.id] = user

    async def is_username_taken(self, username: str) -> bool:
        return any(u.username == username for u in self.users.values())
