from openchat.domain.posts.entities import Post


class PostService:
    async def create_post(self, user_id: str, text: str) -> Post:
        raise NotImplementedError

