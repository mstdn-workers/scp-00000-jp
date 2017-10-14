import utils.log
import utils.file
import utils.api
import settings

import json

収容所 = settings.CHANNEL_CONTAINER

class EventHandler(object):

    def __init__(self):
        self.set_loggers()
        self.webapi = utils.api.WebAPI()

    def set_loggers(self):
        self.console   = utils.log.console()
        self.log       = utils.log.file()

    def on_message(self, ws, user, text):
        pass

    def on_left(self, ws, user):
        pass

    def on_joined(self, ws, user):
        try:
            感染者 = set(utils.file.load("infected"))
            感染者.add(user)
            utils.file.save("infected", list(感染者))

        except Exception as e:
            self.webapi.post_debug_info(e)

    def on_timer(self, ws):
        try:
            感染者 = set(utils.file.load("infected"))
            収容者 = set(self.webapi.get_channel_members(収容所))
            全人類 = set(self.webapi.get_team_members())

            脱走者 = 感染者 - 収容者
            新参者 = 収容者 - 感染者
            死亡者 = 感染者 - 全人類

            utils.file.save("infected", list(感染者 | 新参者 - 死亡者))
            if len(脱走者) > 0:
                名簿 = "」「 ".join([ self.webapi.get_username(ID) for ID in 脱走者 ])
                警告 = "感染者「{0}」が収容所から脱走しました。職員はただちに再収容を行ってください。".format(名簿)
                self.webapi.post_message(settings.CHANNEL_DEBUG if settings.DEBUG_MODE else 収容所, 警告)

        except Exception as e:
            self.webapi.post_debug_info(e)

