from aiohttp import web

from openchat.apis.context import api_context
from openchat.entities.users import User
from openchat.usecases.create_user import CreateUser, CreateUserRequest
from openchat.usecases.repositories import DuplicateUser


class UsersAPI:
    async def register_user(self, request: web.Request) -> web.Response:
        create_user = CreateUser()
        data = await request.json()
        create_user_request = self.make_create_user_request(data)
        try:
            user = await create_user.create_user(create_user_request)
            return self.make_created_user_response(user)
        except DuplicateUser:
            return self.make_duplicate_user_response()

    @staticmethod
    def make_create_user_request(data: dict) -> CreateUserRequest:
        return CreateUserRequest(
            username=data.get("username", ""),
            password=data.get("password", ""),
            about=data.get("about", ""))

    def make_created_user_response(self, user: User) -> web.Response:
        return web.json_response(self.present_created_user(user), status=201)

    @staticmethod
    def make_duplicate_user_response() -> web.Response:
        return web.HTTPBadRequest(
            text="Username already in user.")

    @staticmethod
    def present_created_user(user: User):
        return dict(
            id=api_context.make_uuid_for_user(user.username),
            username=user.username,
            about=user.about)
