from typing import Tuple

from aiohttp import web

from openchat.apis.context import api_context
from openchat.entities.documents import Document
from openchat.usecases.get_posts_for_user import GetPostsForUser
from openchat.usecases.post_document import PostDocument, InappropriateLanguage


class DocumentsAPI:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    async def post_document(self, request: web.Request) -> web.Response:
        user_id = request.match_info.get("user_id", "")
        data = await request.json()
        post_document = PostDocument()
        try:
            created_document = await post_document.post_only_appropriate_document(
                username=api_context.get_username_for_uuid(user_id), text=data.get("text", ""))
            return web.json_response(self.present_created_document(created_document), status=201)
        except InappropriateLanguage:
            raise web.HTTPBadRequest(text="Post contains inappropriate language.")

    async def get_posts_for_user(self, request: web.Request) -> web.Response:
        user_id = request.match_info.get("user_id", "")
        get_posts_for_user = GetPostsForUser()
        username = api_context.get_username_for_uuid(user_id)
        documents = await get_posts_for_user.execute(username=username)
        return web.json_response(self.present_documents(documents))

    def present_documents(self, documents: Tuple[Document]):
        return [dict(
            userId=api_context.get_uuid_for_user(d.username),
            postId=api_context.get_uuid_for_document(d.id),
            text=d.text,
            dateTime=d.date_time.strftime(self.DATE_FORMAT))
            for d in sorted(documents, key=lambda d: d.date_time, reverse=True)]

    def present_created_document(self, created_document) -> dict:
        return dict(
            userId=api_context.get_uuid_for_user(created_document.username),
            postId=api_context.make_uuid_for_document(created_document.id),
            text=created_document.text,
            dateTime=created_document.date_time.strftime(self.DATE_FORMAT))
