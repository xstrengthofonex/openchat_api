from aiohttp import web

from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.requests import UserCredentials


class LoginAPI:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def login(self, request: web.Request) -> web.Response:
        credentials = await self.user_credentials_from(request)
        user = await self.user_repository.user_for(credentials)
        if not user:
            return web.HTTPNotFound(text="Invalid credentials.")
        return web.json_response(self.user_to_login_response(user))

    @staticmethod
    def user_to_login_response(user):
        return dict(
            id=user.id,
            username=user.username,
            about=user.about)

    @staticmethod
    async def user_credentials_from(request: web.Request) -> UserCredentials:
        data = await request.json()
        return UserCredentials(
            username=data.get("username", ""),
            password=data.get("password", ""))

