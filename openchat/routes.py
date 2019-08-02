from aiohttp import web

from openchat.apis.context import api_context
from openchat.apis.users_api import UsersAPI
from openchat.usecases.context import context


class Routes:
    def __init__(self):
        context.initialize()
        api_context.initialize()

        self.users_api = UsersAPI()

    @staticmethod
    async def status_api(request: web.Request) -> web.Response:
        return web.Response(text="OpenChat: OK")

    async def create(self, app: web.Application):
        app.router.add_get("/status", self.status_api)
        app.router.add_post("/users", self.users_api.register_user)