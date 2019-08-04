from aiohttp import web

from openchat.apis.context import api_context
from openchat.apis.documents_api import DocumentsAPI
from openchat.apis.login_api import LoginAPI
from openchat.apis.users_api import UsersAPI
from openchat.usecases.context import usecase_context


class Routes:
    def __init__(self):
        usecase_context.initialize()
        api_context.initialize()

        self.users_api = UsersAPI()
        self.login_api = LoginAPI()
        self.documents_api = DocumentsAPI()

    @staticmethod
    async def status_api(request: web.Request) -> web.Response:
        return web.Response(text="OpenChat: OK")

    async def create(self, app: web.Application):
        app.router.add_get("/status", self.status_api)
        app.router.add_post("/users", self.users_api.register_user)
        app.router.add_post("/login", self.login_api.login)
        app.router.add_get("/users", self.users_api.get_users)
        app.router.add_post("/users/{user_id}/timeline", self.documents_api.post_document)
        app.router.add_get("/users/{user_id}/timeline", self.documents_api.get_posts_for_user)
