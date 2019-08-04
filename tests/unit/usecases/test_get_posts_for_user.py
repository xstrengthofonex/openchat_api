from asynctest import TestCase

from openchat.usecases.context import usecase_context
from openchat.usecases.get_posts_for_user import GetPostsForUser
from tests.unit.builders import UserBuilder, DocumentBuilder


class GetPostForUserTest(TestCase):
    async def setUp(self) -> None:
        usecase_context.initialize()

    async def test_can_get_all_posts_for_one_user(self):
        user = UserBuilder().build()
        d1 = DocumentBuilder(id=1, username=user.username).build()
        d2 = DocumentBuilder(id=2, username=user.username).build()
        await usecase_context.repository.add_document(d1)
        await usecase_context.repository.add_document(d2)
        get_posts_for_user = GetPostsForUser()
        documents = await get_posts_for_user.execute(user.username)
        self.assertEqual((d1, d2), documents)
