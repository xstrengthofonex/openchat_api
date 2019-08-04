from typing import List

from openchat.entities.users import User
from openchat.usecases.context import usecase_context


class GetUsers:
    async def execute(self) -> List[User]:
        return await usecase_context.repository.get_all_users()
