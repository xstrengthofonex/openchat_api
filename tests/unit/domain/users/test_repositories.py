from asynctest import TestCase

from openchat.domain.users.repositories import UserRepository
from tests.unit.infrastructure.builders import UserBuilder


class UserRepositoryShould(TestCase):
    ALICE = UserBuilder(username="Alice").build()

    async def setUp(self):
        self.user_repository = UserRepository()

    async def test_informs_when_a_username_is_already_taken(self):
        await self.user_repository.add(self.ALICE)

        self.assertTrue(await self.user_repository.is_username_taken("Alice"))
        self.assertFalse(await self.user_repository.is_username_taken("Charlie"))