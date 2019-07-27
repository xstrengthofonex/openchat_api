from typing import Dict

from aiohttp import web

from openchat.domain.user_entities import User
from openchat.domain.user_exceptions import UsernameAlreadyInUse
from openchat.domain.user_services import UserService
from openchat.domain.user_requests import RegistrationData


class UsersAPI:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def create_user(self, request: web.Request) -> web.Response:
        registration_data = await self.registration_data_from(request)
        try:
            user = await self.user_service.create_user(registration_data)
            return web.json_response(self.user_to_registration_response(user), status=201)
        except UsernameAlreadyInUse:
            return web.HTTPBadRequest(text="Username already in use.")

    @staticmethod
    def user_to_registration_response(user: User) -> Dict[str, str]:
        return dict(
            id=user.id,
            username=user.username,
            about=user.about)

    @staticmethod
    async def registration_data_from(request: web.Request) -> RegistrationData:
        data = await request.json()
        registration_data = RegistrationData(
            username=data.get("username", ""),
            password=data.get("password", ""),
            about=data.get("about", ""))
        return registration_data
