from typing import Dict, Tuple, Optional

from openchat.entities.documents import Document
from openchat.entities.users import User
from openchat.usecases.repositories import Repository


class InMemoryRepository(Repository):
    def __init__(self):
        self._users: Dict[str, User] = dict()
        self._documents: Dict[int, Document] = dict()

    async def add_user(self, user: User) -> None:
        self._users[user.username] = user

    async def add_document(self, document: Document) -> None:
        self._documents[document.id] = document

    async def get_user(self, username: str) -> Optional[User]:
        return self._users.get(username)

    async def get_all_users(self) -> Tuple[User]:
        return tuple(self._users.values())

    async def get_document(self, document_id: int) -> Optional[Document]:
        return self._documents.get(document_id)

    async def get_next_document_id(self) -> int:
        return len(self._documents) + 1
