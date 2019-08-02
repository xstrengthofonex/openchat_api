from asynctest import TestCase

from openchat.usecases.create_user import CreateUserRequest, CreateUser
from openchat.usecases.repositories import DuplicateUser
from openchat.usecases.context import usecase_context


class CreateUserTest(TestCase):
    async def setUp(self) -> None:
        usecase_context.initialize()
        self.usecase = CreateUser()
        self.request = CreateUserRequest(
            username="username",
            password="password",
            about="about")
        self.user = await self.usecase.create_user(self.request)

    async def test_user_fields_are_correct(self):
        self.assertEqual("username", self.user.username)
        self.assertEqual("password", self.user.password)
        self.assertEqual("about", self.user.about)

    async def test_created_user_is_registered(self):
        result = await usecase_context.repository.get_user("username")
        self.assertEqual(self.user, result)

    async def test_raises_exception_when_duplicate_user_is_created(self):
        with self.assertRaises(DuplicateUser):
            await self.usecase.create_user(self.request)
