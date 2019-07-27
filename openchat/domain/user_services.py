from openchat.domain.user_entities import User
from openchat.domain.user_exceptions import UsernameAlreadyInUse
from openchat.domain.user_repositories import UserRepository
from openchat.domain.user_requests import RegistrationData
from openchat.infrastructure.generators import IdGenerator


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.id_generator = IdGenerator()
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
