from typing import Tuple

from openchat.entities.documents import Document
from openchat.usecases.context import usecase_context


class GetPostsForUser:
    async def execute(self, username: str) -> Tuple[Document]:
        return await usecase_context.repository.get_documents_for_user(username)
