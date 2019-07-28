from aiohttp import web

from openchat.apis.following_api import FollowingAPI
from openchat.apis.login_api import LoginAPI
from openchat.apis.posts_api import PostsAPI
from openchat.apis.users_api import UsersAPI
from openchat.domain.posts.repositories import PostRepository
from openchat.domain.posts.services import PostService, LanguageService
from openchat.domain.users.repositories import UserRepository
from openchat.domain.users.services import UserService
from openchat.infrastructure.clock import Clock
from openchat.infrastructure.generators import IdGenerator


class Routes:
    def __init__(self):
        self.id_generator = IdGenerator()
        self.clock = Clock()
        self.user_repository = UserRepository()
        self.post_repository = PostRepository()
        self.language_service = LanguageService()
        self.user_service = UserService(self.user_repository, self.id_generator)
        self.post_service = PostService(
            self.post_repository, self.language_service,
            self.id_generator, self.clock)

        self.users_api = UsersAPI(self.user_service)
        self.login_api = LoginAPI(self.user_repository)
        self.posts_api = PostsAPI(self.post_service)
        self.following_api = FollowingAPI(self.user_service)

    @staticmethod
    async def status_api(request: web.Request) -> web.Response:
        return web.Response(text="OpenChat: OK")

    async def create(self, app: web.Application):
        app.router.add_get("/status", self.status_api)
        app.router.add_post("/users", self.users_api.create_user)
        app.router.add_get("/users", self.users_api.all_users)
        app.router.add_post("/login", self.login_api.login)
        app.router.add_post("/users/{user_id}/timeline", self.posts_api.create_post)
        app.router.add_get("/users/{user_id}/timeline", self.posts_api.posts_by_user)
        app.router.add_post("/followings", self.following_api.create_following)
