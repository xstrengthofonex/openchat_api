from abc import ABC, abstractmethod, ABCMeta
from typing import Tuple, Optional

from openchat.entities.documents import Document
from openchat.entities.users import User


class DuplicateUser(RuntimeError):
    pass


class Repository(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def get_user(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_all_users(self) -> Tuple[User]:
        pass

    @abstractmethod
    async def get_document(self, document_id: str) -> Optional[Document]:
        pass

    @abstractmethod
    async def add_document(self, document: Document) -> None:
        pass

    @abstractmethod
    async def get_next_document_id(self) -> int:
        pass
