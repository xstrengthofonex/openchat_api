from abc import ABC, abstractmethod
from typing import List, Tuple

from openchat.entities.users import User


class DuplicateUser(RuntimeError):
    pass


class Repository(ABC):
    @abstractmethod
    async def get_user(self, username: str) -> User:
        pass

    @abstractmethod
    async def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_all_users(self) -> Tuple[User]:
        pass
