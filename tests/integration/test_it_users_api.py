from tests.integration.dsl import OpenChatTestDSL, ITUserBuilder


class TestITUsersAPI(OpenChatTestDSL):
    SANDRO = ITUserBuilder(username="Sandro").build()
    MASH = ITUserBuilder(username="Mash").build()
    STEVE = ITUserBuilder(username="Steve").build()
    PEDRO = ITUserBuilder(username="Pedro").build()

    async def test_returns_all_users(self):
        self.SANDRO = await self.register(self.SANDRO)
        self.MASH = await self.register(self.MASH)
        self.STEVE = await self.register(self.STEVE)
        self.PEDRO = await self.register(self.PEDRO)

        response = await self.client.get("/users")

        await self.assert_all_users_are_returned(response, [
            self.SANDRO, self.MASH, self.STEVE, self.PEDRO])

    async def test_returns_empty_when_no_users(self):
        response = await self.client.get("/users")

        await self.assert_all_users_are_returned(response, [])
