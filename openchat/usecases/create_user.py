from dataclasses import dataclass

from openchat.entities.users import User
from openchat.usecases.context import usecase_context
from openchat.usecases.repositories import DuplicateUser


@dataclass(frozen=True)
class CreateUserRequest:
    username: str = ""
    password: str = ""
    about: str = ""


class CreateUser:
    async def execute(self, request: CreateUserRequest) -> User:
        if await usecase_context.repository.get_user(request.username):
            raise DuplicateUser
        user = self.make_user(request)
        await usecase_context.repository.add_user(user)
        return user

    @staticmethod
    def make_user(request):
        return User(
            username=request.username,
            password=request.password,
            about=request.about)
