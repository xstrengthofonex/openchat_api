from openchat.domain.posts.entities import Post


class PostRepository:
    async def add(self, post: Post) -> None:
        raise NotImplementedError

