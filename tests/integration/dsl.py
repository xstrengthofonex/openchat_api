import logging

from tests.integration.api_test_suite import APITestSuite


class OpenChatTestDSL(APITestSuite):
    logger = logging.getLogger("OpenChatTestDSL")
    logger.setLevel(level=logging.INFO)

    async def register(self, user):
        self.logger.info(f"Register User: {user}")
