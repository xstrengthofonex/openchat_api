from openchat.domain.user_entities import User


class UserRepository:
    async def add(self, user: User) -> None:
        raise NotImplementedError

    async def is_username_taken(self, username: str) -> bool:
        raise NotImplementedError
