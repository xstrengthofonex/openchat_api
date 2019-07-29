from uuid import uuid4

from asynctest import TestCase
from datetime import datetime, timedelta

from openchat.domain.posts.repositories import PostRepository
from tests.unit.infrastructure.builders import PostBuilder


class PostRepositoryShould(TestCase):
    ALICE_ID = str(uuid4())
    CHARLIE_ID = str(uuid4())
    NOW = datetime.now()
    YESTERDAY = NOW - timedelta(days=1)
    TWENTY_MINUTES_AGO = NOW - timedelta(minutes=20)

    ALICE_POST_1 = PostBuilder(user_id=ALICE_ID, date_time=YESTERDAY).build()
    CHARLIE_POST_1 = PostBuilder(user_id=CHARLIE_ID, date_time=TWENTY_MINUTES_AGO).build()
    ALICE_POST_2 = PostBuilder(user_id=ALICE_ID, date_time=NOW).build()

    async def setUp(self) -> None:
        self.post_repository = PostRepository()
        await self.post_repository.add(self.ALICE_POST_1)
        await self.post_repository.add(self.CHARLIE_POST_1)
        await self.post_repository.add(self.ALICE_POST_2)

    async def test_return_posts_for_given_user_in_reverse_chronological_order(self):
        result = await self.post_repository.posts_by(self.ALICE_ID)

        self.assertEqual(result, [self.ALICE_POST_2, self.ALICE_POST_1])

    async def test_return_a_list_of_posts_for_a_list_of_users(self):
        result = await self.post_repository.posts_for([self.CHARLIE_ID, self.ALICE_ID])

        self.assertEqual(result, [self.ALICE_POST_2, self.CHARLIE_POST_1, self.ALICE_POST_1])
