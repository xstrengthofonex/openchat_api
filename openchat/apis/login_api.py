from aiohttp import web

from openchat.apis.context import api_context
from openchat.entities.users import User
from openchat.usecases.context import usecase_context
from openchat.usecases.login import Login


class LoginAPI:
    async def login(self, request: web.Request) -> web.Response:
        usecase = Login()
        data = await request.json()
        username = data.get("username", "")
        password = data.get("password", "")
        if not await usecase.validate_credentials(username, password):
            raise web.HTTPNotFound(text="Invalid credentials.")
        user = await usecase_context.repository.get_user(username)
        return web.json_response(self.present_user(user), status=200)

    @staticmethod
    def present_user(user: User):
        return dict(
            id=api_context.get_uuid_for_user(user.username),
            username=user.username,
            about=user.about)

