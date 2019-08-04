from typing import Optional

from openchat.entities.users import User
from openchat.usecases.context import usecase_context


class Login:
    @staticmethod
    async def execute(username: str, password: str) -> Optional[User]:
        user = await usecase_context.repository.get_user(username)
        if user and user.password == password:
            return user
        return None
