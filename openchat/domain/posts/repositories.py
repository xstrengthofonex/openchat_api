from collections import defaultdict
from typing import List, Dict

from openchat.domain.posts.entities import Post


class PostRepository:
    def __init__(self):
        self.posts: Dict[str, List[Post]] = defaultdict(list)

    async def add(self, post: Post) -> None:
        self.posts[post.user_id].append(post)

    async def posts_by(self, user_id: str) -> List[Post]:
        return list(sorted(self.posts.get(user_id, []), key=lambda p: p.date_time, reverse=True))

    async def posts_for(self, user_ids: List[str]) -> List[Post]:
        result = []
        for user_id in user_ids:
            result.extend(self.posts.get(user_id, []))
        return list(sorted(result, key=lambda p: p.date_time, reverse=True))

