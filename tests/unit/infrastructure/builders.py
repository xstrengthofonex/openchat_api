
from dataclasses import dataclass
from uuid import uuid4

from datetime import datetime

from openchat.domain.posts.entities import Post
from openchat.domain.users.entities import User


@dataclass(frozen=True)
class UserBuilder:
    id: str = None
    username: str = "Username"
    password: str = "password"
    about: str = "About"

    def build(self) -> User:
        return User(
            id=self.id or str(uuid4()),
            username=self.username,
            password=self.password,
            about=self.about)


@dataclass(frozen=True)
class PostBuilder:
    post_id: str = None
    user_id: str = None
    text: str = "Some Text"
    date_time: datetime = None

    def build(self) -> Post:
        return Post(
            post_id=self.post_id or str(uuid4()),
            user_id=self.user_id or str(uuid4()),
            text=self.text,
            date_time=self.date_time or datetime.now())
