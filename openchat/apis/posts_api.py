from aiohttp import web

from openchat.domain.posts.entities import Post
from openchat.domain.posts.exceptions import InappropriateLanguage
from openchat.domain.posts.services import PostService


class PostsAPI:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, post_service: PostService) -> None:
        self.post_service = post_service

    async def create_post(self, request: web.Request) -> web.Response:
        user_id = request.match_info.get("user_id")
        text = await self.post_text_from(request)
        try:
            post = await self.post_service.create_post(user_id, text)
            return web.json_response(self.create_post_response_from(post), status=201)
        except InappropriateLanguage:
            return web.HTTPBadRequest(text="Post contains inappropriate language.")

    @staticmethod
    async def post_text_from(request: web.Request) -> str:
        data = await request.json()
        return data.get("text", "")

    def create_post_response_from(self, post: Post) -> dict:
        return dict(
            postId=post.post_id,
            userId=post.user_id,
            text=post.text,
            dateTime=post.date_time.strftime(self.DATE_FORMAT))
