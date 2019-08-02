from openchat.usecases.context import usecase_context


class Login:
    @staticmethod
    async def validate_credentials(username: str, password: str) -> bool:
        user = await usecase_context.repository.get_user(username)
        return user and user.password == password
