import json
from typing import List
from uuid import uuid4

from aiohttp import web
from asynctest import TestCase, Mock

from openchat.apis.wall_api import WallAPI
from openchat.domain.posts.entities import Post
from openchat.domain.posts.services import WallService
from tests.unit.infrastructure.builders import PostBuilder


class WallAPIShould(TestCase):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    USER_ID = str(uuid4())
    WALL_POSTS = [PostBuilder().build()]

    async def setUp(self) -> None:
        self.wall_service = Mock(WallService)
        self.request = Mock(web.Request)
        self.wall_api = WallAPI(self.wall_service)

    async def test_returns_posts_from_user_and_all_users_followees(self):
        self.request.match_info.get.return_value = self.USER_ID
        self.wall_service.wall_for.return_value = self.WALL_POSTS

        result = await self.wall_api.wall_by_user(self.request)

        self.wall_service.wall_for.assert_called_with(self.USER_ID)
        self.assertEqual(200, result.status)
        self.assertEqual("application/json", result.content_type)
        self.assertEqual(self.wall_data_from(self.WALL_POSTS), json.loads(result.text))

    def post_data_from(self, post: Post) -> dict:
        return dict(
            postId=post.post_id,
            userId=post.user_id,
            text=post.text,
            dateTime=post.date_time.strftime(self.DATE_FORMAT))

    def wall_data_from(self, posts: List[Post]) -> List[dict]:
        return [self.post_data_from(p) for p in posts]