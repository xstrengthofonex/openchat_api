from typing import List

from openchat.domain.users.entities import User
from openchat.domain.users.exceptions import UsernameAlreadyInUse
from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.requests import RegistrationData
from openchat.infrastructure.generators import IdGenerator


class UserService:
    def __init__(self, user_repository: UserRepository, id_generator: IdGenerator) -> None:
        self.id_generator = id_generator
        self.user_repository = user_repository

    async def create_user(self, registration_data: RegistrationData) -> User:
        await self._validate_username(registration_data.username)
        user = User(
            id=self.id_generator.next_id(),
            username=registration_data.username,
            password=registration_data.password,
            about=registration_data.about)
        await self.user_repository.add(user)
        return user

    async def _validate_username(self, username: str) -> None:
        if await self.user_repository.is_username_taken(username):
            raise UsernameAlreadyInUse

    async def all_users(self) -> List[User]:
        return await self.user_repository.all()
