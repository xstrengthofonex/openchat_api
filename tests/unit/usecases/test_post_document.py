from asynctest import TestCase

from openchat.usecases.context import usecase_context
from openchat.usecases.post_document import PostDocument, InappropriateLanguage


class PostDocumentTest(TestCase):
    async def setUp(self) -> None:
        usecase_context.initialize()
        self.post_document = PostDocument()

    async def test_can_any_post_document(self):
        created_document = await self.post_document.post("username", "text")
        fetched_document = await usecase_context.repository.get_document(created_document.id)
        self.assertEqual(created_document, fetched_document)

    async def test_can_post_document_with_appropriate_language(self):
        created_document = await self.post_document.post_only_appropriate_document("username", "text")
        fetched_document = await usecase_context.repository.get_document(created_document.id)
        self.assertEqual(created_document, fetched_document)

    async def test_cannot_post_document_with_inappropriate_language(self):
        for text in ["orange", "OrangE", "ORANge", "Elephant", "ELEPHANT","Ice Cream", "ice cream"]:
            with self.assertRaises(InappropriateLanguage):
                await self.post_document.post_only_appropriate_document("username", text)
