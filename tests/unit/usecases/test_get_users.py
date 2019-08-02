from asynctest import TestCase

from openchat.usecases.context import usecase_context
from openchat.usecases.get_users import GetUsers
from tests.unit.builders import UserBuilder


class GetUsersTest(TestCase):
    async def setUp(self) -> None:
        usecase_context.initialize()
        self.get_users = GetUsers()

    async def test_can_get_all_users(self):
        user = UserBuilder(username="Bob").build()
        await usecase_context.repository.add_user(user)
        users = await self.get_users.get()
        self.assertEqual((user,), users)
