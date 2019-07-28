from aiohttp import web

from openchat.domain.users.requests import Following
from openchat.domain.users.services import UserService


class FollowingAPI:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def create_following(self, request: web.Request) -> web.Response:
        following = await self.following_from(request)
        await self.user_service.add_following(following)
        return web.json_response(status=201)

    @staticmethod
    async def following_from(request):
        data = await request.json()
        return Following(
            follower_id=data.get("followerId", ""),
            followee_id=data.get("followeeId", ""))
