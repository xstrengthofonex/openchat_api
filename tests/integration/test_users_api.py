from tests.integration.dsl import OpenChatTestDSL, ITUserBuilder


class TestITUsersAPI(OpenChatTestDSL):
    SANDRO = ITUserBuilder(username="Sandro").build()
    MASH = ITUserBuilder(username="Mash").build()
    STEVE = ITUserBuilder(username="Steve").build()
    PEDRO = ITUserBuilder(username="Pedro").build()

    async def test_returns_all_users(self):
        sandro = await self.register(self.SANDRO)
        mash = await self.register(self.MASH)
        steve = await self.register(self.STEVE)
        pedro = await self.register(self.PEDRO)

        response = await self.client.get("/users")

        await self.assert_all_users_are_returned(response, [sandro, mash, steve, pedro])
