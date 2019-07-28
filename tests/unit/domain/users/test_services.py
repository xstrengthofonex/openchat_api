from uuid import uuid4

from asynctest import TestCase, Mock

from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.requests import RegistrationData, Following
from openchat.domain.users.services import UserService, UsernameAlreadyInUse, FollowingAlreadyExists
from openchat.infrastructure.generators import IdGenerator
from tests.unit.infrastructure.builders import UserBuilder


class UserServiceShould(TestCase):
    USER = UserBuilder().build()
    REGISTRATION_DATA = RegistrationData(
        username=USER.username,
        password=USER.password,
        about=USER.about)
    USERS = [USER]
    FOLLOWEE_ID = str(uuid4())
    FOLLOWER_ID = str(uuid4())
    FOLLOWING = Following(follower_id=FOLLOWER_ID, followee_id=FOLLOWEE_ID)
    FOLLOWEE = UserBuilder(id=FOLLOWEE_ID).build()
    FOLLOWEES = [FOLLOWEE]

    async def setUp(self) -> None:
        self.user_repository = Mock(UserRepository)
        self.id_generator = Mock(IdGenerator)
        self.user_service = UserService(self.user_repository, self.id_generator)
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

    async def test_get_all_users(self):
        self.user_repository.all.return_value = self.USERS

        result = await self.user_service.all_users()

        self.assertEqual(self.USERS, result)

    async def test_register_a_following(self):
        self.user_repository.has_following.return_value = False

        await self.user_service.add_following(self.FOLLOWING)

        self.user_repository.add_following.assert_called_with(self.FOLLOWING)

    async def test_raises_error_when_creating_existing_following(self):
        with self.assertRaises(FollowingAlreadyExists):
            self.user_repository.has_following.return_value = True
            await self.user_service.add_following(self.FOLLOWING)
        self.user_repository.has_following.assert_called_with(self.FOLLOWING)

    async def test_returns_users_followed_by_given_user(self):
        self.user_repository.followees_by.return_value = self.FOLLOWEES

        result = await self.user_service.followees_for(self.FOLLOWER_ID)

        self.user_repository.followees_by.assert_called_with(self.FOLLOWER_ID)
        self.assertEqual(self.FOLLOWEES, result)
