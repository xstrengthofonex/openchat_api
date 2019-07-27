from aiohttp import web


class Routes:
    @staticmethod
    async def status_api(request: web.Request) -> web.Response:
        return web.Response(text="OpenChat: OK")

    async def create(self, app: web.Application):
        app.router.add_get("/status", self.status_api)

