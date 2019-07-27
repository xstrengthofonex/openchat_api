from asynctest import TestCase, Mock

from openchat.domain.user_repositories import UserRepository
from openchat.domain.user_requests import RegistrationData
from openchat.domain.user_services import UserService
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

    async def test_create_user(self):
        self.id_generator.next_id.return_value = self.USER.id
        result = await self.user_service.create_user(self.REGISTRATION_DATA)

        self.user_repository.add.assert_called_with(self.USER)
        self.assertEqual(self.USER, result)
