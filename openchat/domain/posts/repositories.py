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
