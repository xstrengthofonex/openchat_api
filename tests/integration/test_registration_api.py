from tests.integration.api_test_suite import APITestSuite


class TestITRegistrationAPI(APITestSuite):
    async def test_register_a_new_user(self):
        response = await self.client.post("/users", json=dict(
            username="Lucy",
            password="alki342d",
            about="About Lucy"))

        self.assertEqual(201, response.status)
        self.assertEqual(self.JSON, response.content_type)
        body = await response.json()
        self.assertRegex(body.get("id"), self.UUID_PATTERN)
        self.assertEqual("Lucy", body.get("username"))
        self.assertEqual("About Lucy", body.get("about"))

