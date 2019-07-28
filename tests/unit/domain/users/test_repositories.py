from asynctest import TestCase

from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.requests import UserCredentials
from tests.unit.infrastructure.builders import UserBuilder


class UserRepositoryShould(TestCase):
    ALICE = UserBuilder(username="Alice").build()
    CHARLIE = UserBuilder(username="Charlie").build()
    ALICE_CREDENTIALS = UserCredentials(
        username=ALICE.username, password=ALICE.password)
    CHARLIE_CREDENTIALS = UserCredentials(
        username=CHARLIE.username, password=CHARLIE.password)
    UNKNOWN_CREDENTIALS = UserCredentials(
        username="unknown", password="unknown")

    async def setUp(self):
        self.user_repository = UserRepository()

    async def test_informs_when_a_username_is_already_taken(self):
        await self.user_repository.add(self.ALICE)

        self.assertTrue(await self.user_repository.is_username_taken("Alice"))
        self.assertFalse(await self.user_repository.is_username_taken("Charlie"))

    async def test_return_user_matching_valid_credentials(self):
        await self.user_repository.add(self.ALICE)
        await self.user_repository.add(self.CHARLIE)

        self.assertEqual(await self.user_repository.user_for(self.ALICE_CREDENTIALS), self.ALICE)
        self.assertEqual(await self.user_repository.user_for(self.CHARLIE_CREDENTIALS), self.CHARLIE)
        self.assertIsNone(await self.user_repository.user_for(self.UNKNOWN_CREDENTIALS))

    async def test_returns_all_users(self):
        await self.user_repository.add(self.ALICE)
        await self.user_repository.add(self.CHARLIE)

        result = await self.user_repository.all()

        self.assertEqual(result, [self.ALICE, self.CHARLIE])
