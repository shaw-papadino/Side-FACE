# from websocket_server import WebsocketServer
from websocket_server import WebsocketServer
import threading

class WebsocketSidecamServer():
    def __init__(self):
        self.server = WebsocketServer(port=443, host='127.0.0.1')
        thread = threading.Thread(target=lambda: self.server.run_forever())
        thread.start()

    def send_message(self, message):
        self.server.send_message_to_all(message)
