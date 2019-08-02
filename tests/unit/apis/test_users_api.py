import json

from asynctest import TestCase

from openchat.apis.context import api_context
from openchat.apis.users_api import UsersAPI
from openchat.entities.users import User


class TestUsersAPI(TestCase):
    async def setUp(self) -> None:
        api_context.initialize()
        self.api = UsersAPI()
        self.user = User(username="Username", password="Password", about="About")

    async def test_can_make_request(self):
        cur = self.api.make_create_user_request(dict(
            username="Username",
            password="Password",
            about="About"))
        self.assertEqual("Username", cur.username)
        self.assertEqual("Password", cur.password)
        self.assertEqual("About", cur.about)

    async def test_makes_response_for_duplicate_user(self):
        response = self.api.make_duplicate_user_response()
        self.assertEqual(400, response.status)
        self.assertEqual("Username already in user.", response.text)

    async def test_makes_response_for_created_user(self):
        response = self.api.make_created_user_response(self.user)
        self.assertEqual(201, response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertEqual(self.created_user_dict_from_user(self.user),
                         json.loads(response.text))

    @staticmethod
    def created_user_dict_from_user(user: User):
        return dict(
            id=api_context.get_uuid_for_user(user.username),
            username=user.username,
            about=user.about)
