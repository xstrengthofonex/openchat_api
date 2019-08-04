from asynctest import TestCase

from openchat.usecases.context import usecase_context
from openchat.usecases.login import Login
from tests.unit.builders import UserBuilder


class LoginTest(TestCase):
    async def setUp(self) -> None:
        usecase_context.initialize()
        self.login = Login()

    async def test_login_with_valid_credentials(self):
        user = UserBuilder(username="Username", password="Password").build()
        await usecase_context.repository.add_user(user)
        result = await self.login.execute(user.username, user.password)
        self.assertEqual(user, result)

    async def test_login_with_invalid_credentials(self):
        result = await self.login.execute("InvalidUsername", "InvalidPassword")
        self.assertIsNone(result)

    async def test_login_with_invalid_password(self):
        user = UserBuilder(username="Username", password="Password").build()
        await usecase_context.repository.add_user(user)
        result = await self.login.execute(user.username, "InvalidPassword")
        self.assertIsNone(result)
