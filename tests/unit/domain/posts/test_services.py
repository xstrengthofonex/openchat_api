from uuid import uuid4

from asynctest import TestCase, Mock
from datetime import datetime

from openchat.domain.posts.entities import Post
from openchat.domain.posts.repositories import PostRepository
from openchat.domain.posts.services import PostService, LanguageService, InappropriateLanguage
from openchat.infrastructure.clock import Clock
from openchat.infrastructure.generators import IdGenerator


class PostServiceShould(TestCase):
    POST_ID = str(uuid4())
    USER_ID = str(uuid4())
    TEXT = "Post Text"
    INAPPROPRIATE_TEXT = "Inappropriate language"
    TODAY = datetime.now()
    POST = Post(
        post_id=POST_ID,
        user_id=USER_ID,
        text=TEXT,
        date_time=TODAY)
    POSTS = [POST]

    async def setUp(self) -> None:
        self.post_repository = Mock(PostRepository)
        self.id_generator = Mock(IdGenerator)
        self.clock = Mock(Clock)
        self.language_service = Mock(LanguageService)
        self.post_service = PostService(
            self.post_repository, self.language_service,
            self.id_generator, self.clock)

    async def test_create_a_post(self):
        self.language_service.is_inappropriate.return_value = False
        self.id_generator.next_id.return_value = self.POST_ID
        self.clock.now.return_value = self.TODAY

        result = await self.post_service.create_post(self.USER_ID, self.TEXT)

        self.post_repository.add.assert_called_with(self.POST)
        self.assertEqual(self.POST, result)

    async def test_raises_error_when_creating_post_with_inappropriate_language(self):
        self.language_service.is_inappropriate.return_value = True
        with self.assertRaises(InappropriateLanguage):
            await self.post_service.create_post(self.USER_ID, self.INAPPROPRIATE_TEXT)
        self.language_service.is_inappropriate.assert_called_with(self.INAPPROPRIATE_TEXT)

    async def test_returns_posts_for_given_user(self):
        self.post_repository.posts_by.return_value = self.POSTS

        result = await self.post_service.posts_by(self.USER_ID)

        self.post_repository.posts_by.assert_called_with(self.USER_ID)
        self.assertEqual(self.POSTS, result)


class LanguageServiceShould(TestCase):
    INAPPROPRIATE_TEXTS = [
        "Elephant", "elephant", "eLePhant", "big ELEphant",
        "Orange", "orange", "ORANGE", "small orange",
        "Ice cream", "ice cream", "cold ice cream"]
    APPROPRIATE_TEXT = "Ok Text"

    async def setUp(self) -> None:
        self.language_service = LanguageService()

    async def test_determines_when_text_has_inappropriate_language(self):
        for text in self.INAPPROPRIATE_TEXTS:
            self.assertTrue(await self.language_service.is_inappropriate(text))

    async def test_determines_when_text_is_appropriate_language(self):
        self.assertFalse(await self.language_service.is_inappropriate(self.APPROPRIATE_TEXT))

