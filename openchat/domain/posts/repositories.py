from typing import List

from openchat.domain.posts.entities import Post


class PostRepository:
    async def add(self, post: Post) -> None:
        pass

    async def posts_by(self, user_id: str) -> List[Post]:
        pass
