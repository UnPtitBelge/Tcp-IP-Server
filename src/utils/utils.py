from pathlib import Path
from enum import Enum

LOG_PATH_DIR = Path(__file__).resolve().parent.parent.parent / "logs"


class Command(Enum):
    PING = 0
    LOGIN = 1
    SEND_MESSAGE = 2
