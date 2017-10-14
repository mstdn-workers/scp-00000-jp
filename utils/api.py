import slacker
import settings
import threading
import traceback, sys


class WebAPI(object):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.api = slacker.Slacker(settings.API_TOKEN)
                cls._instance.users = {}
        return cls._instance


    def get_username(self, user_id):
        if user_id not in self.users:
            user = self.api.users.info(user_id).body["user"]
            self.users[user_id] = {
                "id"     : user_id,
                "name"   : user["profile"]["real_name"]
            }
        return self.users[user_id]["name"]


    def get_channel_members(self, channel_id):
        channel = self.api.channels.info(channel_id).body["channel"]
        members = channel["members"]
        return members

    def get_team_members(self):
        members = self.api.users.list().body["members"]
        return [ user["id"] for user in members ]

    def post_debug_info(self, e):
        error_message = "```\n{0}\n```".format(traceback.format_exc())
        self.api.chat.post_message(channel=settings.CHANNEL_DEBUG, text=error_message, as_user=True)

    def post_message(self, channel, message):
        self.api.chat.post_message(channel=channel, text=message, as_user=True)

