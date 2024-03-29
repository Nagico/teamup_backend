import json
import random
from time import sleep
from uuid import UUID, uuid4

try:
    import thread
except ImportError:
    import _thread as thread
import requests
import websocket
from loguru import logger
from websocket import WebSocketApp

union_ids = [
    UUID("b9b5b5b5-5b5b-5b5b-5b5b-5b5b5b5b5b5b"),
    UUID("c9c5c5c5-5c5c-5c5c-5c5c-5c5c5c5c5c5c"),
    UUID("d9d5d5d5-5d5d-5d5d-5d5d-5d5d5d5d5d5d"),
    UUID("e9e5e5e5-5e5e-5e5e-5e5e-5e5e5e5e5e5e"),
]


def get_access_token(union_id: UUID) -> (int, str):
    data = requests.post(
        url="https://api.test.teamup.nagico.cn/auth/zq/unionid/",
        json={"union_id": union_id.hex},
    ).json()["data"]

    return int(data["id"]), data["access"]


class STOMP:
    @staticmethod
    def connect_debug(user_id: int) -> str:
        return f"""CONNECT
accept-version:1.2,1.1,1.0
heart-beat:0,0
UserId:{user_id}

\0"""

    @staticmethod
    def connect(access_token: str) -> str:
        return f"""CONNECT
accept-version:1.2,1.1,1.0
heart-beat:0,0
Authentication:Bearer {access_token}

\0"""

    @staticmethod
    def subscribe(topic: str | int) -> str:
        return f"""SUBSCRIBE
id:{uuid4()}
destination:{topic}
ack:client-individual

\0"""

    @staticmethod
    def disconnect(receipt: int) -> str:
        return """DISCONNECT
receipt:{}

\0""".format(
            receipt
        )

    @staticmethod
    def _send(receiver: str, msg_type: str, content: str) -> str:
        content_dict = {
            "type": int(msg_type),
            "content": content,
        }

        msg = json.dumps(content_dict)

        return f"""SEND
id:{uuid4()}
destination:{receiver}
content-type:application/json
receipt: {random.randint(0,10000)}
content-length:{len(msg)}

{msg}\0"""

    @staticmethod
    def send(command: str) -> str:
        cmd_list = command.split(" ")
        receiver = command.split(" ")[1]
        if len(cmd_list) == 2:
            msg_type = input("type: ")
            content = input("content: ")
        elif len(cmd_list) == 3:
            msg_type = input("type: ")
            content = " ".join(cmd_list[2:])
        else:
            msg_type = cmd_list[2]
            content = " ".join(cmd_list[3:])

        return STOMP._send(receiver, msg_type, content)

    @staticmethod
    def chat(command: str):
        cmd_list = command.split(" ")
        receiver = command.split(" ")[1]
        if len(cmd_list) == 2:
            content = input("content: ")
        else:
            content = " ".join(cmd_list[2:])

        return STOMP._send(receiver, "1", content)

    @staticmethod
    def read(command: str):
        cmd_list = command.split(" ")
        receiver = command.split(" ")[1]
        if len(cmd_list) == 2:
            content = input("content: ")
        else:
            content = " ".join(cmd_list[2:])

        return STOMP._send(receiver, "2", content)

    @staticmethod
    def ack(command: str) -> str:
        cmd_list = command.split(" ")
        return f"""ACK
message-id:{cmd_list[1]}

\0"""


class StompState:
    OPEN = 0
    CONNECTED = 1
    DISCONNECTED = 3
    CLOSE = 4


class WS:
    def __init__(self, url: str, user_id: int, access: str | None = None):
        self.url = url
        self.ws = None
        self.user_id = user_id
        self.access = access

        self.state = 0
        self.close_receipt = random.randint(0, 100000)

    def send(self, msg):
        logger.info("\n" + msg.replace("\0", "NULL"))
        self.ws.send(msg)

    def on_message(self, cls, message):
        if type(message) == bytes:
            msg = message.decode("utf-8").replace("\0", "NULL")
        elif type(message) == str:
            msg = message.replace("\0", "NULL")
        else:
            raise TypeError("Unknown message type")
        if self.state == StompState.DISCONNECTED and msg.startswith("RECEIPT"):
            self.state = StompState.CLOSE
        else:
            logger.info(f"\n{msg}")

    def on_error(self, cls, error):
        logger.error(f"\n{error}")

    def on_close(self, cls, code, reason):
        logger.success("close")

    def on_ping(self, cls, message):
        logger.info("ping")

    def on_pong(self, cls, message):
        logger.info("pong")

    def on_open(self, cls):
        logger.success("open")
        self.state = StompState.OPEN
        thread.start_new_thread(self.run, ())

    def prepare_close(self):
        self.state = True
        self.send(STOMP.disconnect(self.close_receipt))

    def run(self, *args):
        if self.access:
            self.send(STOMP.connect(access))
        else:
            self.send(STOMP.connect_debug(self.user_id))

        self.send(STOMP.subscribe(self.user_id))

        self.state = StompState.CONNECTED
        while True:
            msg = []
            tmp = input()
            if tmp.startswith("#SEND"):
                cmd = STOMP.send(tmp)
                self.send(cmd)
                continue
            if tmp.startswith("#CHAT"):
                cmd = STOMP.chat(tmp)
                self.send(cmd)
                continue
            if tmp.startswith("#READ"):
                cmd = STOMP.read(tmp)
                self.send(cmd)
                continue
            if tmp.startswith("#ACK"):
                cmd = STOMP.ack(tmp)
                self.send(cmd)
                continue

            while tmp != "NULL":
                msg.append(tmp)
                tmp = input()
            if len(msg) == 0:
                self.prepare_close()
                while self.state != StompState.CLOSE:
                    sleep(0.1)
            else:
                cmd = "\n".join(tmp) + "\n\0"
                self.ws.send(cmd)

    def start(self):
        websocket.enableTrace(False)  # 开启运行状态追踪。debug 的时候最好打开他，便于追踪定位问题。

        self.ws = WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        self.ws.run_forever()


if __name__ == "__main__":
    LOCAL_URL = "ws://localhost:8060/"
    REMOTE_URL = "wss://chat.test.teamup.nagico.cn/"

    URL = REMOTE_URL
    DEBUG = True

    if DEBUG:
        user_id = int(input("Input user id (must exist): "))
        access = None
    else:
        user = input(f"Choose an user to login [0-{len(union_ids) - 1}]: ")
        user_id, access = get_access_token(union_ids[int(user)])

    WS(URL, user_id, access).start()
