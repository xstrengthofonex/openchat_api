from typing import List

from tests.integration.dsl import (
    OpenChatTestDSL, ITUserBuilder, ITUser, ITPostBuilder, ITPost)


class TestITTimelineAPI(OpenChatTestDSL):
    DAVID = ITUserBuilder(username="David", about="About David").build()

    async def setUp(self) -> None:
        await super().setUp()
        self.user = await self.register(self.DAVID)
        self.posts = await self.create_posts_for(self.DAVID, 2)
        self.timeline = None

    async def test_retrieve_a_timeline_with_all_posts_from_user_in_chronological_order(self):
        await self.given_david_posts(self.posts)

        await self.when_he_checks_his_timeline()

        await self.then_he_should_see(list(reversed(self.posts)))

    @staticmethod
    async def create_posts_for(user: ITUser, number: int) -> List[ITPost]:
        return [ITPostBuilder(user_id=user.id, text=f"Post {i+1}").build() for i in range(number)]

    async def given_david_posts(self, posts) -> None:
        for post in posts:
            await self.create(post)

    async def when_he_checks_his_timeline(self) -> None:
        response = await self.client.get(f"/users/{self.user.id}/timeline")
        self.assertEqual(200, response.status)
        self.assertEqual("application/json", response.content_type)
        self.timeline = await response.json()

    async def then_he_should_see(self, posts: List[ITPost]):
        for i in range(len(posts)):
            self.assert_timeline_matches_post(self.timeline[i], self.posts[i])
