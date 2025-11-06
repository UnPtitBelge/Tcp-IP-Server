import json
import struct
from enum import Enum
from pathlib import Path
from socket import socket
from typing import Any

LOG_PATH_DIR = Path(__file__).resolve().parent.parent.parent / "logs"


class Cmd(int, Enum):
    PING = 0
    LOGIN = 1
    SEND_MESSAGE = 2
    GET_DATA = 3


def recv(sock: socket) -> Any:
    b_len = sock.recv(4)
    if len(b_len) == 0:
        return None

    (res_len,) = struct.unpack("!I", b_len)
    b_res = sock.recv(res_len)

    return json.loads(b_res)


def send(sock: socket, data: dict) -> None:
    b_data = json.dumps(data).encode()
    packet = struct.pack("!I", len(b_data)) + b_data
    sock.sendall(packet)
