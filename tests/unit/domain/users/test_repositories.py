from asynctest import TestCase

from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.requests import UserCredentials, Following
from tests.unit.infrastructure.builders import UserBuilder


class UserRepositoryShould(TestCase):
    ALICE = UserBuilder(username="Alice").build()
    CHARLIE = UserBuilder(username="Charlie").build()
    BOB = UserBuilder(username="Bob").build()
    LUCY = UserBuilder(username="Lucy").build()

    ALICE_CREDENTIALS = UserCredentials(username=ALICE.username, password=ALICE.password)
    CHARLIE_CREDENTIALS = UserCredentials(username=CHARLIE.username, password=CHARLIE.password)
    UNKNOWN_CREDENTIALS = UserCredentials(username="unknown", password="unknown")

    ALICE_FOLLOWS_CHARLIE = Following(follower_id=ALICE.id, followee_id=CHARLIE.id)
    CHARLIE_FOLLOWS_ALICE = Following(follower_id=CHARLIE.id, followee_id=ALICE.id)
    ALICE_FOLLOWS_LUCY = Following(follower_id=ALICE.id, followee_id=LUCY.id)
    BOB_FOLLOWS_CHARLIE = Following(follower_id=BOB.id, followee_id=CHARLIE.id)
    LUCY_FOLLOWS_BOB = Following(follower_id=LUCY.id, followee_id=BOB.id)

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

    async def test_detects_a_following_already_exists(self):
        await self.user_repository.add_following(self.ALICE_FOLLOWS_CHARLIE)

        self.assertTrue(await self.user_repository.has_following(self.ALICE_FOLLOWS_CHARLIE))
        self.assertFalse(await self.user_repository.has_following(self.CHARLIE_FOLLOWS_ALICE))

    async def test_returns_followees_for_a_given_follower(self):
        await self.user_repository.add(self.ALICE)
        await self.user_repository.add(self.CHARLIE)
        await self.user_repository.add(self.BOB)
        await self.user_repository.add(self.LUCY)

        await self.user_repository.add_following(self.ALICE_FOLLOWS_CHARLIE)
        await self.user_repository.add_following(self.ALICE_FOLLOWS_LUCY)
        await self.user_repository.add_following(self.BOB_FOLLOWS_CHARLIE)
        await self.user_repository.add_following(self.LUCY_FOLLOWS_BOB)

        result = await self.user_repository.followees_by(self.ALICE.id)

        self.assertEqual([self.CHARLIE, self.LUCY], result)
