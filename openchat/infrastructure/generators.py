from uuid import uuid4


class IdGenerator:
    @staticmethod
    def next_id():
        return str(uuid4())
