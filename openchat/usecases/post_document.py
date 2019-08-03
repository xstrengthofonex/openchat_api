from datetime import datetime

from openchat.entities.documents import Document
from openchat.usecases.context import usecase_context


class InappropriateLanguage(RuntimeError):
    pass


class PostDocument:
    inappropriate_words = ["ICE CREAM", "ORANGE", "ELEPHANT"]

    async def post(self, username: str, text: str) -> Document:
        document = Document(
            id=await usecase_context.repository.get_next_document_id(),
            username=username,
            text=text,
            date_time=datetime.now())
        await usecase_context.repository.add_document(document)
        return document

    async def post_only_appropriate_document(self, username: str, text: str) -> Document:
        if any(word in text.upper() for word in self.inappropriate_words):
            raise InappropriateLanguage
        return await self.post(username, text)
