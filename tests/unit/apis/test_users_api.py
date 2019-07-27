import json
from typing import Dict
from uuid import uuid4

from aiohttp.web import Request
from asynctest import TestCase, Mock

from openchat.apis.users_api import UsersAPI
from openchat.domain.users import UserService, RegistrationData, User
from tests.unit.infrastructure.builders import UserBuilder


class UsersAPIShould(TestCase):
    USERNAME = "Alice"
    PASSWORD = "1234567"
    ABOUT = "About Alice"
    USER_ID = str(uuid4())
    REGISTRATION_DATA = RegistrationData(
        username=USERNAME,
        password=PASSWORD,
        about=ABOUT)
    USER = UserBuilder(
        id=USER_ID,
        username=USERNAME,
        password=PASSWORD,
        about=ABOUT).build()

    def setUp(self) -> None:
        self.user_service = Mock(UserService)
        self.request = Mock(Request)
        self.users_api = UsersAPI(self.user_service)
        self.request.json.return_value = self.registration_request_containing(self.REGISTRATION_DATA)
        self.user_service.create_user.return_value = self.USER

    async def test_create_a_new_user(self):
        await self.users_api.create_user(self.request)

        self.user_service.create_user.assert_called_with(self.REGISTRATION_DATA)

    async def test_return_json_representing_a_created_user(self):
        result = await self.users_api.create_user(self.request)

        self.user_service.create_user.assert_called_with(self.REGISTRATION_DATA)
        self.assertEqual(201, result.status)
        self.assertEqual("application/json", result.content_type)
        self.assertEqual(self.registration_response_containing(self.USER), json.loads(result.text))

    @staticmethod
    def registration_request_containing(registration_data: RegistrationData) -> Dict[str, str]:
        return dict(
            username=registration_data.username,
            password=registration_data.password,
            about=registration_data.about)

    @staticmethod
    def registration_response_containing(user: User) -> Dict[str, str]:
        return dict(
            id=user.id,
            username=user.username,
            about=user.about)
