from uuid import uuid4

from asynctest import TestCase
from datetime import datetime, timedelta

from openchat.domain.posts.repositories import PostRepository
from tests.unit.infrastructure.builders import PostBuilder


class PostRepositoryShould(TestCase):
    ALICE_ID = str(uuid4())
    CHARLIE_ID = str(uuid4())
    TODAY = datetime.now()
    YESTERDAY = TODAY - timedelta(days=1)
    ALICE_POST_1 = PostBuilder(user_id=ALICE_ID, date_time=YESTERDAY).build()
    ALICE_POST_2 = PostBuilder(user_id=ALICE_ID, date_time=TODAY).build()
    CHARLIE_POST_1 = PostBuilder(user_id=CHARLIE_ID, text="Alice Post 3").build()

    async def setUp(self) -> None:
        self.post_repository = PostRepository()

    async def test_return_posts_for_given_user_in_reverse_chronological_order(self):
        await self.post_repository.add(self.ALICE_POST_1)
        await self.post_repository.add(self.CHARLIE_POST_1)
        await self.post_repository.add(self.ALICE_POST_2)

        result = await self.post_repository.posts_by(self.ALICE_ID)

        self.assertEqual(result, [self.ALICE_POST_2, self.ALICE_POST_1])
