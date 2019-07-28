from tests.integration.dsl import OpenChatTestDSL, ITUserBuilder


class TestITFolloweeAPI(OpenChatTestDSL):
    VIVIAN = ITUserBuilder(username="Viviane").build()
    SAMUEL = ITUserBuilder(username="Samuel").build()
    OLIVIA = ITUserBuilder(username="Olivia").build()

    async def setUp(self):
        await super().setUp()
        self.VIVIAN = await self.register(self.VIVIAN)
        self.SAMUEL = await self.register(self.SAMUEL)
        self.OLIVIA = await self.register(self.OLIVIA)

    async def test_returns_all_followees_for_a_given_user(self):
        await self.given_viviane_follows(self.SAMUEL, self.OLIVIA)

        response = await self.client.get(f"/followings/{self.VIVIAN.id}/followees")

        await self.assert_all_users_are_returned(response, [self.SAMUEL, self.OLIVIA])

    async def given_viviane_follows(self, *users):
        for user in users:
            await self.create_following(self.VIVIAN, user)
