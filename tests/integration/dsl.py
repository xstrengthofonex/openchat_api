import logging
from dataclasses import dataclass
from uuid import uuid4

from tests.integration.api_test_suite import APITestSuite


@dataclass(frozen=True)
class ITUser:
    id: str
    username: str
    password: str
    about: str


@dataclass(frozen=True)
class ITUserBuilder:
    id: str = None
    username: str = "Alice"
    password: str = "12345678"
    about: str = "About Alice"

    def build(self) -> ITUser:
        return ITUser(
            id=self.id or str(uuid4()),
            username=self.username,
            password=self.password,
            about=self.about)


class OpenChatTestDSL(APITestSuite):
    logger = logging.getLogger("OpenChatTestDSL")
    logger.setLevel(level=logging.INFO)

    async def register(self, user: ITUser):
        self.logger.info(f"Register User: {user}")
        response = await self.client.post("/users", json=dict(
            username=user.username,
            password=user.password,
            about=user.about))
        body = await response.json()
        self.logger.info(f"Registration response: {str(body)}")
        user_id = body.get("id")
        registered_user = ITUserBuilder(
            id=user_id,
            username=user.username,
            password=user.password,
            about=user.about).build()
        self.logger.info(f"Registration done. User: {registered_user}")
        return registered_user

