from typing import List

from openchat.domain.posts.entities import Post
from openchat.domain.posts.exceptions import InappropriateLanguage
from openchat.domain.posts.repositories import PostRepository
from openchat.infrastructure.clock import Clock
from openchat.infrastructure.generators import IdGenerator


class LanguageService:
    inappropriate_words = ["ELEPHANT", "ORANGE", "ICE CREAM"]

    async def is_inappropriate(self, text: str) -> bool:
        return any(w in text.upper() for w in self.inappropriate_words)


class PostService:
    def __init__(self, post_repository: PostRepository,
                 language_service: LanguageService,
                 id_generator: IdGenerator, clock: Clock) -> None:
        self.post_repository = post_repository
        self.language_service = language_service
        self.id_generator = id_generator
        self.clock = clock

    async def create_post(self, user_id: str, text: str) -> Post:
        await self.validate(text)
        post = Post(
            post_id=self.id_generator.next_id(),
            user_id=user_id,
            text=text,
            date_time=self.clock.now())
        await self.post_repository.add(post)
        return post

    async def posts_by(self, user_id: str) -> List[Post]:
        return await self.post_repository.posts_by(user_id)

    async def validate(self, text):
        if await self.language_service.is_inappropriate(text):
            raise InappropriateLanguage

