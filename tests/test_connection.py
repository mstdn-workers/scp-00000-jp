import unittest
import settings
from bot import Bot


class TestConnection(unittest.TestCase):

    def test_api_token(self):
        token = settings.API_TOKEN
        self.assertIsNotNone(token)

    def test_rtm_api(self):
        bot = Bot()
        bot.connect()
        self.assertIsNotNone(bot.websocket)
