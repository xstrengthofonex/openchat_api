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
        self.assertEqual(self.user.id, body.get("id"))
        self.assertEqual(self.user.username, body.get("username"))
        self.assertEqual(self.user.about, body.get("about"))

    async def test_attempt_with_unregistered_user(self):
        response = await self.client.post("/login", json=dict(
            username="unknownUsername", password="unknownPassword"))

        self.assertEqual(404, response.status)
        self.assertEqual("Invalid credentials.", await response.text())

    async def test_attempt_with_invalid_password(self):
        response = await self.client.post("/login", json=dict(
            username=self.ANTONY.username, password="InvalidPassword"))

        self.assertEqual(404, response.status)
        self.assertEqual("Invalid credentials.", await response.text())
