from asynctest import TestCase, Mock

from openchat.domain.users.exceptions import UsernameAlreadyInUse
from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.requests import RegistrationData
from openchat.domain.users.services import UserService
from openchat.infrastructure.generators import IdGenerator
from tests.unit.infrastructure.builders import UserBuilder


class UserServiceShould(TestCase):
    USER = UserBuilder().build()
    REGISTRATION_DATA = RegistrationData(
        username=USER.username,
        password=USER.password,
        about=USER.about)

    async def setUp(self) -> None:
        self.user_repository = Mock(UserRepository)
        self.id_generator = Mock(IdGenerator)
        self.user_service = UserService(self.user_repository)
        self.user_service.id_generator = self.id_generator
        self.id_generator.next_id.return_value = self.USER.id
        self.user_repository.is_username_taken.return_value = False

    async def test_create_user(self):
        result = await self.user_service.create_user(self.REGISTRATION_DATA)

        self.user_repository.add.assert_called_with(self.USER)
        self.assertEqual(self.USER, result)

    async def test_raises_error_when_creating_a_duplicate_user(self):
        with self.assertRaises(UsernameAlreadyInUse):
            self.user_repository.is_username_taken.return_value = True

            await self.user_service.create_user(self.REGISTRATION_DATA)

            self.user_repository.is_username_taken.assert_called_with(self.USER.username)