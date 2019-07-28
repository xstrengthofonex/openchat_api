import logging
from dataclasses import dataclass
from typing import List
from uuid import uuid4

from datetime import datetime

from tests.integration.api_test_suite import APITestSuite


DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


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


@dataclass(frozen=True)
class ITPost:
    post_id: str
    user_id: str
    text: str
    date_time: datetime


@dataclass(frozen=True)
class ITPostBuilder:
    post_id: str = None
    user_id: str = None
    text: str = "Some Text"
    date_time: datetime = None

    def build(self):
        return ITPost(
            post_id=self.post_id or str(uuid4()),
            user_id=self.user_id or str(uuid4()),
            text=self.text,
            date_time=self.date_time or datetime.now())


class OpenChatTestDSL(APITestSuite):
    logger = logging.getLogger("OpenChatTestDSL")
    logger.setLevel(level=logging.INFO)

    async def register(self, user: ITUser) -> ITUser:
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

    async def create(self, post: ITPost):
        self.logger.info(f"Create post: {post}")
        response = await self.client.post(f"/users/{post.user_id}/timeline", json=dict(
            text=post.text))
        self.assertEqual(201, response.status)
        self.assertEqual("application/json", response.content_type)
        body = await response.json()
        self.assertRegex(body.get("postId"), self.UUID_PATTERN)
        self.assertEqual(post.user_id, body.get("userId"))
        self.assertEqual(post.text, body.get("text"))
        self.assertIsNotNone(body.get("dateTime"))
        self.logger.info("Post created.")

    def assert_timeline_matches_post(self, result: dict, post: ITPost) -> None:
        self.assertRegex(result.get("postId"), self.UUID_PATTERN)
        self.assertRegex(result.get("userId"), self.UUID_PATTERN)
        self.assertEqual(post.text, result.get("text"))
        self.assertIsNotNone(result.get("dateTime"))

    async def assert_all_users_are_returned(self, response, users: List[ITUser]) -> None:
        self.assertEqual(200, response.status)
        self.assertEqual("application/json", response.content_type)
        body = await response.json()
        assert all(self.user_response_from(u) in body for u in users)

    @staticmethod
    def user_response_from(user: ITUser) -> dict:
        return dict(
            id=user.id,
            username=user.username,
            about=user.about)
