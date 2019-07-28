import json
from uuid import uuid4

from aiohttp import web
from asynctest import TestCase, Mock
from datetime import datetime

from openchat.apis.posts_api import PostsAPI
from openchat.domain.posts.entities import Post
from openchat.domain.posts.exceptions import InappropriateLanguage
from openchat.domain.posts.services import PostService


class PostsAPIShould(TestCase):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    USER_ID = str(uuid4())
    POST_TEXT = "Some Text"
    INAPPROPRIATE_TEXT = "Inappropriate Text"
    TODAY = datetime.now()
    POST_ID = str(uuid4())
    POST = Post(post_id=POST_ID,
                user_id=USER_ID,
                text=POST_TEXT,
                date_time=TODAY)

    async def setUp(self) -> None:
        self.request = Mock(web.Request)
        self.post_service = Mock(PostService)
        self.posts_api = PostsAPI(self.post_service)

    async def test_create_a_post(self):
        self.request.match_info.get.return_value = self.USER_ID
        self.request.json.return_value = dict(text=self.POST_TEXT)
        self.post_service.create_post.return_value = self.POST

        await self.posts_api.create_post(self.request)

        self.post_service.create_post.assert_called_with(self.USER_ID, self.POST_TEXT)

    async def test_returns_created_post(self):
        self.request.match_info.get.return_value = self.USER_ID
        self.request.json.return_value = dict(text=self.POST_TEXT)
        self.post_service.create_post.return_value = self.POST

        result = await self.posts_api.create_post(self.request)

        self.post_service.create_post.assert_called_with(self.USER_ID, self.POST_TEXT)
        self.assertEqual(201, result.status)
        self.assertEqual("application/json", result.content_type)
        self.assertEqual(self.create_post_response_from(self.POST), json.loads(result.text))

    async def test_returns_error_when_creating_post_with_inappropriate_language(self):
        self.request.match_info.get.return_value = self.USER_ID
        self.request.json.return_value = dict(text=self.INAPPROPRIATE_TEXT)
        self.post_service.create_post.side_effect = InappropriateLanguage

        result = await self.posts_api.create_post(self.request)

        self.post_service.create_post.assert_called_with(self.USER_ID, self.INAPPROPRIATE_TEXT)
        self.assertEqual(400, result.status)
        self.assertEqual("Post contains inappropriate language.", result.text)

    def create_post_response_from(self, post: Post) -> dict:
        return dict(
            postId=post.post_id,
            userId=post.user_id,
            text=post.text,
            dateTime=post.date_time.strftime(self.DATE_FORMAT))

