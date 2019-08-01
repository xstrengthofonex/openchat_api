from aiohttp import web

from openchat.apis.users_api import UsersAPI
from openchat.repositories.in_memory_repositories import InMemoryRepository
from openchat.usecases.context import Context


class Routes:
    def __init__(self):
        Context.repository = InMemoryRepository()
        self.users_api = UsersAPI()

    @staticmethod
    async def status_api(request: web.Request) -> web.Response:
        return web.Response(text="OpenChat: OK")

    async def create(self, app: web.Application):
        app.router.add_get("/status", self.status_api)
        app.router.add_post("/users", self.users_api.register_user)