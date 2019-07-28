import json

from aiohttp import web
from asynctest import TestCase, Mock

from openchat.apis.login_api import LoginAPI
from openchat.domain.users.entities import User
from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.requests import UserCredentials
from tests.unit.infrastructure.builders import UserBuilder


class LoginAPIShould(TestCase):
    USER = UserBuilder().build()
    USER_CREDENTIALS = UserCredentials(
        username=USER.username,
        password=USER.password)

    async def setUp(self) -> None:
        self.request = Mock(web.Request)
        self.user_repository = Mock(UserRepository)
        self.login_api = LoginAPI(self.user_repository)

    async def test_returns_a_valid_user(self):
        self.user_repository.user_for.return_value = self.USER
        self.request.json.return_value = self.login_request_containing(self.USER_CREDENTIALS)

        result = await self.login_api.login(self.request)

        self.user_repository.user_for.assert_called_with(self.USER_CREDENTIALS)
        self.assertEqual(200, result.status)
        self.assertEqual("application/json", result.content_type)
        self.assertEqual(self.login_response_containing(self.USER), json.loads(result.text))

    async def test_return_an_error_when_credentials_are_invalid(self):
        self.user_repository.user_for.return_value = None
        self.request.json.return_value = self.login_request_containing(self.USER_CREDENTIALS)

        result = await self.login_api.login(self.request)

        self.user_repository.user_for.assert_called_with(self.USER_CREDENTIALS)
        self.assertEqual(404, result.status)
        self.assertEqual("Invalid credentials.", result.text)

    @staticmethod
    def login_request_containing(user_credentials: UserCredentials) -> dict:
        return dict(
            username=user_credentials.username,
            password=user_credentials.password)

    @staticmethod
    def login_response_containing(user: User) -> dict:
        return dict(
            id=user.id,
            username=user.username,
            about=user.about)

