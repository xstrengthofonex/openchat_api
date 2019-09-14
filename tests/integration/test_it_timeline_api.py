from itertools import zip_longest
from typing import List

from tests.integration.dsl import (
    OpenChatTestDSL, ITUserBuilder, ITUser, ITPostBuilder, ITPost)


class TestITTimelineAPI(OpenChatTestDSL):
    DAVID = ITUserBuilder(username="David", about="About David").build()

    async def setUp(self) -> None:
        await super().setUp()
        self.DAVID = await self.register(self.DAVID)
        self.posts = await self.create_posts_for(self.DAVID, 2)
        self.timeline: List[dict] = []

    async def test_retrieve_a_timeline_with_all_posts_from_user_in_chronological_order(self):
        await self.given_david_posts(self.posts)

        await self.when_he_checks_his_timeline()

        await self.then_he_should_see(list(reversed(self.posts)))

    async def test_cannot_create_an_inappropriate_post(self):
        post = ITPostBuilder(user_id=self.DAVID.id, text="Orange").build()
        response = await self.client.post(f"/users/{post.user_id}/timeline", json=dict(
            text=post.text))
        self.assertEqual(400, response.status)
        self.assertEqual("Post contains inappropriate language.", await response.text())

    @staticmethod
    async def create_posts_for(user: ITUser, number: int) -> List[ITPost]:
        return [ITPostBuilder(user_id=user.id, text=f"Post {i+1}").build() for i in range(number)]

    async def given_david_posts(self, posts) -> None:
        for post in posts:
            await self.create(post)

    async def when_he_checks_his_timeline(self) -> None:
        response = await self.client.get(f"/users/{self.DAVID.id}/timeline")
        self.assertEqual(200, response.status)
        self.assertEqual("application/json", response.content_type)
        self.timeline.extend(await response.json())

    async def then_he_should_see(self, posts: List[ITPost]):
        for (result, expected) in zip_longest(self.timeline, posts):
            self.assert_result_matches_post(result, expected)
