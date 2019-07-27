from openchat.domain.users.entities import User
from openchat.domain.users.requests import RegistrationData


class UserService:
    async def create_user(self, registration_data: RegistrationData) -> User:
        raise NotImplementedError

