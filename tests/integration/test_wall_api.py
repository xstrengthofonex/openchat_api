from itertools import zip_longest

from tests.integration.dsl import OpenChatTestDSL, ITUserBuilder, ITPostBuilder


class TestWallAPI(OpenChatTestDSL):
    ALICE = ITUserBuilder(username="Alice").build()
    BOB = ITUserBuilder(username="Bob").build()
    CHARLIE = ITUserBuilder(username="Charlie").build()
    JULIE = ITUserBuilder(username="Julie").build()

    async def setUp(self):
        await super().setUp()
        self.ALICE = await self.register(self.ALICE)
        self.BOB = await self.register(self.BOB)
        self.CHARLIE = await self.register(self.CHARLIE)
        self.JULIE = await self.register(self.JULIE)

        self.POST_1_ALICE = ITPostBuilder(user_id=self.ALICE.id, text="Post 1").build()
        self.POST_2_BOB = ITPostBuilder(user_id=self.BOB.id, text="Post 2").build()
        self.POST_3_CHARLIE = ITPostBuilder(user_id=self.CHARLIE.id, text="Post 3").build()
        self.POST_4_JULIE = ITPostBuilder(user_id=self.JULIE.id, text="Post 4").build()
        self.POST_5_ALICE = ITPostBuilder(user_id=self.ALICE.id, text="Post 5").build()
        self.POST_6_BOB = ITPostBuilder(user_id=self.BOB.id, text="Post 6").build()

        self.wall = []

    async def test_returns_a_wall_containing_posts_from_user_and_followees(self):
        await self.given_posts(
            self.POST_1_ALICE,
            self.POST_2_BOB,
            self.POST_3_CHARLIE,
            self.POST_4_JULIE,
            self.POST_5_ALICE,
            self.POST_6_BOB)
        await self.and_alice_follows(self.BOB, self.CHARLIE)

        await self.then_she_sees_the_posts(
            self.POST_6_BOB,
            self.POST_5_ALICE,
            self.POST_3_CHARLIE,
            self.POST_2_BOB,
            self.POST_1_ALICE)

    async def given_posts(self, *posts) -> None:
        for post in posts:
            await self.create(post)

    async def and_alice_follows(self, *followees):
        for followee in followees:
            await self.create_following(self.ALICE, followee)

    async def when_alice_checks_her_wall(self):
        response = await self.client.get(f"/users/{self.ALICE.id}/wall")
        self.assertEqual(200, response.status)
        self.assertEqual("application/json", response.content_type)
        self.wall.extend(await response.json())

    async def then_she_sees_the_posts(self, *posts):
        for (result, expected) in zip_longest(self.wall, posts):
            self.assert_result_matches_post(result, expected)
