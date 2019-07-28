import json
from typing import List
from uuid import uuid4

from aiohttp import web
from asynctest import TestCase, Mock

from openchat.apis.following_api import FollowingAPI
from openchat.domain.users.entities import User
from openchat.domain.users.requests import Following
from openchat.domain.users.services import UserService, FollowingAlreadyExists
from tests.unit.infrastructure.builders import UserBuilder


class FollowingAPIShould(TestCase):
    FOLLOWER_ID = str(uuid4())
    FOLLOWEE_ID = str(uuid4())
    FOLLOWING = Following(follower_id=FOLLOWER_ID, followee_id=FOLLOWEE_ID)
    FOLLOWEE = UserBuilder(id=FOLLOWEE_ID).build()
    FOLLOWEES = [FOLLOWEE]

    async def setUp(self) -> None:
        self.request = Mock(web.Request)
        self.user_service = Mock(UserService)
        self.following_api = FollowingAPI(self.user_service)

    async def test_register_a_following(self):
        self.request.json.return_value = self.following_data_from(self.FOLLOWING)

        result = await self.following_api.create_following(self.request)

        self.user_service.add_following.assert_called_with(self.FOLLOWING)
        self.assertEqual(201, result.status)

    async def test_returns_error_if_following_already_exists(self):
        self.user_service.add_following.side_effect = FollowingAlreadyExists

        result = await self.following_api.create_following(self.request)

        self.assertEqual(400, result.status)
        self.assertEqual("Following already exists.", result.text)

    async def test_returns_all_users_followed_by_given_user(self):
        self.request.match_info.get.return_value = self.FOLLOWER_ID
        self.user_service.followees_for.return_value = self.FOLLOWEES

        result = await self.following_api.get_followees(self.request)

        self.user_service.followees_for.assert_called_with(self.FOLLOWER_ID)
        self.assertEqual(200, result.status)
        self.assertEqual("application/json", result.content_type)
        self.assertEqual(self.followees_response_from(self.FOLLOWEES), json.loads(result.text))

    @staticmethod
    def following_data_from(following):
        return dict(
            followerId=following.follower_id,
            followeeId=following.followee_id)

    @staticmethod
    def followees_response_from(followees: List[User]):
        return [dict(id=f.id, username=f.username, about=f.about) for f in followees]
