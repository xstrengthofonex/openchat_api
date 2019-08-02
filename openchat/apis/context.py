from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4


@dataclass
class APIContext:
    _user_uuids: Dict[str, str] = field(default_factory=dict)

    def make_uuid_for_user(self, username: str) -> str:
        value = str(uuid4())
        self._user_uuids[username] = value
        return value

    def get_uuid_for_user(self, username: str) -> str:
        return self._user_uuids.get(username)

    def initialize(self):
        self._user_uuids = dict()


api_context = APIContext()
api_context.initialize()
