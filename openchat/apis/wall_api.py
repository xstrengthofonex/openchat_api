from typing import List

from aiohttp import web

from openchat.domain.posts.entities import Post
from openchat.domain.posts.services import WallService


class WallAPI:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, wall_service: WallService) -> None:
        self.wall_service = wall_service

    async def wall_by_user(self, request: web.Request) -> web.Response:
        user_id = request.match_info.get("user_id")
        wall_posts = await self.wall_service.wall_for(user_id)
        return web.json_response(self.wall_data_from(wall_posts))

    def post_data_from(self, post: Post) -> dict:
        return dict(
            postId=post.post_id,
            userId=post.user_id,
            text=post.text,
            dateTime=post.date_time.strftime(self.DATE_FORMAT))

    def wall_data_from(self, posts: List[Post]) -> List[dict]:
        return [self.post_data_from(p) for p in posts]