from uuid import uuid4

from aiohttp import web
from asynctest import TestCase, Mock

from openchat.apis.following_api import FollowingAPI
from openchat.domain.users.requests import Following
from openchat.domain.users.services import UserService


class FollowingAPIShould(TestCase):
    FOLLOWER_ID = str(uuid4())
    FOLLOWEE_ID = str(uuid4())
    FOLLOWING = Following(follower_id=FOLLOWER_ID, followee_id=FOLLOWEE_ID)

    async def setUp(self) -> None:
        self.request = Mock(web.Request)
        self.user_service = Mock(UserService)
        self.following_api = FollowingAPI(self.user_service)

    async def test_register_a_following(self):
        self.request.json.return_value = self.following_data_from(self.FOLLOWING)

        result = await self.following_api.create_following(self.request)

        self.user_service.add_following.assert_called_with(self.FOLLOWING)
        self.assertEqual(201, result.status)

    @staticmethod
    def following_data_from(following):
        return dict(
            followerId=following.follower_id,
            followeeId=following.followee_id)
