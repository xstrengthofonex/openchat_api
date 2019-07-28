from typing import List

from aiohttp import web

from openchat.domain.users.entities import User
from openchat.domain.users.requests import Following
from openchat.domain.users.services import UserService, FollowingAlreadyExists


class FollowingAPI:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def create_following(self, request: web.Request) -> web.Response:
        following = await self.following_from(request)
        try:
            await self.user_service.add_following(following)
        except FollowingAlreadyExists:
            return web.HTTPBadRequest(text="Following already exists.")
        return web.json_response(status=201)

    async def get_followees(self, request: web.Request) -> web.Response:
        follower_id = request.match_info.get("follower_id")
        followees = await self.user_service.followees_for(follower_id)
        return web.json_response(self.followees_response_from(followees))

    @staticmethod
    def followees_response_from(followees: List[User]):
        return [dict(
            id=f.id,
            username=f.username,
            about=f.about)
            for f in followees]

    @staticmethod
    async def following_from(request):
        data = await request.json()
        return Following(
            follower_id=data.get("followerId", ""),
            followee_id=data.get("followeeId", ""))
