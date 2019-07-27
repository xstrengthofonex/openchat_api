import logging
from typing import Callable

from aiohttp import web
from aiohttp.web_middlewares import middleware

from openchat.routes import Routes


class OpenChat:
    API_NOT_IMPLEMENTED = "API Not Implemented"
    INTERNAL_SERVER_ERROR = "Internal Server Error"

    logger = logging.getLogger("OpenChat")
    logging.basicConfig(level=logging.INFO)

    def __init__(self) -> None:
        self.routes = Routes()

    @middleware
    async def enable_cors(self, request: web.Response, handler: Callable) -> web.Response:
        response: web.Response = await handler(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, PUT, PATCH, OPTIONS"
        return response

    @middleware
    async def configure_errors(self, request: web.Request, handler: Callable) -> web.Response:
        try:
            return await handler(request)
        except web.HTTPException as ex:
            if ex.status == 404:
                self.logger.error(f"{self.API_NOT_IMPLEMENTED}: {request.path}")
                raise web.HTTPNotImplemented(text=self.API_NOT_IMPLEMENTED)
            if ex.status == 500:
                self.logger.error(f"{self.INTERNAL_SERVER_ERROR}: {request.path}")
                raise web.HTTPNotImplemented(text=self.INTERNAL_SERVER_ERROR)
            raise

    async def create_app(self) -> web.Application:
        app = web.Application(middlewares=[
            self.enable_cors,
            self.configure_errors])
        await self.routes.create(app)
        return app


if __name__ == '__main__':
    openchat = OpenChat()
    web.run_app(openchat.create_app(), port=4321)

