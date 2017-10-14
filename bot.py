import slacker
import websocket
import _thread
import schedule
import time
import json
import settings
import events
import utils.log
import utils.api

class Bot(object):
    def __init__(self):
        self.connected = False
        self.websocket = None
        self.api       = slacker.Slacker(settings.API_TOKEN)
        self.webapi    = utils.api.WebAPI()
        self.event     = events.EventHandler()
        self.console   = utils.log.console()
        self.log       = utils.log.file()
        self.console.info('Start.')

    def connect(self):
        if self.connected:
            return
        while True:
            try:
                reply = self.api.rtm.start().body
                self.get_websocket(reply["url"])
                self.console.info("Connected to Slack.")
                self.connected = True
                time.sleep(1)
                return
            except Exception as e:
                self.console.exception("Failed to connect: %s", e)
                if str(e) == "not_authed":
                    self.console.exception("Wrong API Token.")
                    return
                time.sleep(5)

    def get_websocket(self, url):
        self.websocket = websocket.WebSocketApp(url, on_message=self.receive, on_error=self.error, on_close=self.close, on_open=self.send)

    def start(self):
        self.websocket.run_forever()

    def error(self, ws, e):
        if str(e):
            self.log.warning(e)
            self.console.warning(e)
            self.webapi.post_debug_info(e)

    def close(self, ws):
        self.console.info("Connection Closed.")

    def receive(self, ws, message):
        self.console.debug(message)
        event = json.loads(message)

        if self.validate(event):

            if event["type"] == "message" and "subtype" not in event:
                self.event.on_message(ws, event["user"], event["text"])

            if event["type"] == "member_left_channel":
                self.event.on_left(ws, event["user"])

            if event["type"] == "member_joined_channel":
                self.event.on_joined(ws, event["user"])

    def send(self, ws):
        schedule.every(settings.TIMER_INTERVAL).seconds.do(self.event.on_timer, ws)
        def timer():
            while True:
                schedule.run_pending()
                time.sleep(1)
        _thread.start_new_thread(timer,())

    def validate(self, event):
        if "type" not in event:
            return False
        if "bot_id" in event:
            return False
        if event.get("user") == settings.USER_SELF:
            return False
        return True
