# src/utils/log,py
from typing import override
from .utils import LOG_PATH_DIR
from pathlib import Path
from datetime import datetime

def get_time() -> str:
    return "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]: "

class Singleton(type):
    _instances: dict[object, object] = {}

    @override
    def __call__(cls, *args: object, **kwargs: object):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    _log_file: Path = LOG_PATH_DIR / "server.log"
    def log(self, message: str) -> None:
        with open(self._log_file, 'a') as f:
            written = f.write(get_time() + message + '\n')
            if written == 0:
                raise IOError("Failed to write to log file\n")
