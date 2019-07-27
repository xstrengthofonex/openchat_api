import re

from aiohttp.test_utils import TestClient, TestServer
from asynctest import TestCase

from openchat.app import OpenChat


class APITestSuite(TestCase):
    JSON = "application/json"
    UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)

    async def setUp(self):
        self.openchat = OpenChat()
        self.app = await self.openchat.create_app()
        self.client = TestClient(TestServer(self.app), loop=self.loop)
        await self.client.start_server()

    async def tearDown(self) -> None:
        await self.client.close()

