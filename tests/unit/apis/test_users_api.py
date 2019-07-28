import json
from typing import Dict, List
from uuid import uuid4

from aiohttp.web import Request
from asynctest import TestCase, Mock

from openchat.apis.users_api import UsersAPI
from openchat.domain.users.entities import User
from openchat.domain.users.services import UserService, UsernameAlreadyInUse
from openchat.domain.users.requests import RegistrationData
from tests.unit.infrastructure.builders import UserBuilder


class UsersAPIShould(TestCase):
    USERNAME = "Alice"
    PASSWORD = "1234567"
    ABOUT = "About Alice"
    USER_ID = str(uuid4())
    REGISTRATION_DATA = RegistrationData(username=USERNAME, password=PASSWORD, about=ABOUT)
    USER = UserBuilder(id=USER_ID, username=USERNAME, password=PASSWORD, about=ABOUT).build()
    USERS = [USER]

    def setUp(self) -> None:
        self.user_service = Mock(UserService)
        self.request = Mock(Request)
        self.users_api = UsersAPI(self.user_service)
        self.request.json.return_value = self.registration_data_from(self.REGISTRATION_DATA)
        self.user_service.create_user.return_value = self.USER

    async def test_create_a_new_user(self):
        await self.users_api.create_user(self.request)

        self.user_service.create_user.assert_called_with(self.REGISTRATION_DATA)

    async def test_return_json_representing_a_created_user(self):
        result = await self.users_api.create_user(self.request)

        self.user_service.create_user.assert_called_with(self.REGISTRATION_DATA)
        self.assertEqual(201, result.status)
        self.assertEqual("application/json", result.content_type)
        self.assertEqual(self.user_data_from(self.USER), json.loads(result.text))

    async def test_return_an_error_when_creating_a_user_with_an_existing_name(self):
        self.user_service.create_user.side_effect = UsernameAlreadyInUse

        result = await self.users_api.create_user(self.request)

        self.user_service.create_user.assert_called_with(self.REGISTRATION_DATA)
        self.assertEqual(400, result.status)
        self.assertEqual("Username already in use.", result.text)

    async def test_returns_all_users(self):
        self.user_service.all_users.return_value = self.USERS

        result = await self.users_api.all_users(self.request)

        self.assertEqual(self.users_data_from(self.USERS), json.loads(result.text))

    @staticmethod
    def registration_data_from(registration_data: RegistrationData) -> Dict[str, str]:
        return dict(
            username=registration_data.username,
            password=registration_data.password,
            about=registration_data.about)

    @staticmethod
    def user_data_from(user: User) -> Dict[str, str]:
        return dict(
            id=user.id,
            username=user.username,
            about=user.about)

    def users_data_from(self, users: List[User]) -> List[dict]:
        return [self.user_data_from(u) for u in users]
