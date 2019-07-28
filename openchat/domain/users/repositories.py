from typing import Dict, Optional, List

from openchat.domain.users.entities import User
from openchat.domain.users.requests import UserCredentials


class UserRepository:
    def __init__(self):
        self.users: Dict[str, User] = dict()

    async def add(self, user: User) -> None:
        self.users[user.id] = user

    async def all(self) -> List[User]:
        return list(self.users.values())

    async def is_username_taken(self, username: str) -> bool:
        return any(u.username == username for u in self.users.values())

    async def user_for(self, credentials: UserCredentials) -> Optional[User]:
        return next((u for u in self.users.values() if credentials.matches(u)), None)

