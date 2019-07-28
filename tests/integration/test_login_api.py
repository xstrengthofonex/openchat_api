from tests.integration.dsl import OpenChatTestDSL, ITUserBuilder


class TestITLoginAPI(OpenChatTestDSL):
    ANTONY = ITUserBuilder(username="Antony").build()

    async def setUp(self):
        await super().setUp()
        self.user = await self.register(self.ANTONY)

    async def test_perform_login(self):
        response = await self.client.post("/login", json=dict(
            username=self.ANTONY.username, password=self.ANTONY.password))

        self.assertEqual(200, response.status)
        self.assertEqual(self.JSON, response.content_type)
        body = await response.json()
        self.assertEqual(self.ANTONY.id, body.get("id"), )
        self.assertEqual(self.ANTONY.username, body.get("username"))
        self.assertEqual(self.ANTONY.about, body.get("about"))
