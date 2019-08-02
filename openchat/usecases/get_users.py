from typing import List

from openchat.entities.users import User
from openchat.usecases.context import usecase_context


class GetUsers:
    async def get(self) -> List[User]:
        return await usecase_context.repository.get_users()
