from aiohttp import web

from openchat.apis.context import api_context
from openchat.usecases.post_document import PostDocument


class DocumentsAPI:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    async def post_document(self, request: web.Request) -> web.Response:
        user_id = request.match_info.get("user_id", "")
        data = await request.json()
        post_document = PostDocument()
        created_document = await post_document.post_only_appropriate_document(
            username=api_context.get_username_for_uuid(user_id), text=data.get("text", ""))
        return web.json_response(self.present_created_document(created_document), status=201)

    def present_created_document(self, created_document) -> dict:
        return dict(
            userId=api_context.get_uuid_for_user(created_document.username),
            postId=api_context.make_uuid_for_document(created_document.id),
            text=created_document.text,
            dateTime=created_document.date_time.strftime(self.DATE_FORMAT))
