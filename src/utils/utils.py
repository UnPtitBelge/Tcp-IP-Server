import json
import struct
from pathlib import Path
from socket import socket

# Static path of the log files
LOG_PATH_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
CMD = "cmd"


def pack(cmd: str, dict_data: dict = {}) -> bytes:
    """Transform the data into a formatted JSON string before encoding it into bytes and pack it"""

    packet = json.dumps({CMD: cmd} | dict_data).encode()
    return struct.pack("!I", len(packet)) + packet


def recv(sock: socket) -> dict | None:
    """Receive the data and transform it into the right format:
    [4 bytes for the 'data' length]+['data']
    """
    b_len = sock.recv(4)  # Get the length of the data in byte (use 4 bytes)
    if len(b_len) == 0:
        return None

    # Get the length of the data to be received
    (data_len,) = struct.unpack("!I", b_len)

    raw_res = sock.recv(data_len)  # Get the rest of the data

    return dict(
        json.loads(raw_res)
    )  # Loads the data correctly into a dictionnary (format used)


def send(sock: socket, packet: bytes) -> None:
    sock.sendall(packet)
