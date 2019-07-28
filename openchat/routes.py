from aiohttp import web

from openchat.apis.login_api import LoginAPI
from openchat.apis.users_api import UsersAPI
from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.services import UserService


class Routes:
    def __init__(self):
        self.user_repository = UserRepository()
        self.user_service = UserService(self.user_repository)
        self.users_api = UsersAPI(self.user_service)
        self.login_api = LoginAPI(self.user_repository)

    @staticmethod
    async def status_api(request: web.Request) -> web.Response:
        return web.Response(text="OpenChat: OK")

    async def create(self, app: web.Application):
        app.router.add_get("/status", self.status_api)
        app.router.add_post("/users", self.users_api.create_user)
        app.router.add_post("/login", self.login_api.login)

