import json
import struct
from enum import Enum
from pathlib import Path
from socket import socket
from typing import Any

# Static path of the log files
LOG_PATH_DIR = Path(__file__).resolve().parent.parent.parent / "logs"


class Cmd(int, Enum):
    """Commands for the requests and responses"""

    PING = 0
    LOGIN = 1
    SEND_MESSAGE = 2
    GET_DATA = 3


def recv(sock: socket) -> Any:
    """Receive the data and transform it into the right format:
    [4 bytes for the 'data' length]+['data']
    """
    b_len = sock.recv(4)  # Get the length of the data in byte (use 4 bytes)
    if len(b_len) == 0:
        return None

    # Get the length of the data to be received
    (data_len,) = struct.unpack("!I", b_len)

    raw_res = sock.recv(data_len)  # Get the rest of the data

    return json.loads(
        raw_res
    )  # Loads the data correctly into a dictionnary (format used)


def send(sock: socket, data: dict) -> None:
    """Transform the data into a formatted JSON string, pack it"""

    # Encode the data to bytes
    b_data = json.dumps(data).encode()

    # Set the data to be sent into the correct byte format
    packet = struct.pack("!I", len(b_data)) + b_data
    sock.sendall(packet)
