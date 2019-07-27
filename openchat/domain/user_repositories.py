from openchat.domain.user_entities import User


class UserRepository:
    async def add(self, user: User) -> None:
        raise NotImplementedError

