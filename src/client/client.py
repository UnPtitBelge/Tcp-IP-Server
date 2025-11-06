# Basic client for server test
import sys
from getpass import getpass
from socket import AF_INET, SOCK_STREAM, socket

from utils import Cmd, Logger, utils


class Client:
    def __init__(
        self, target_host: str, target_port: int, client_name: str = "name"
    ) -> None:
        self.target_host = target_host
        self.target_port = target_port
        self.client_name = client_name

        self._credentials = {"user": "", "pwd": ""}

        self._client_socket: socket | None = None

        self._log: Logger = Logger("client.log")

    def start_client(self) -> socket | None:
        if self._client_socket is not None:
            return
        try:
            # Create socket
            self._client_socket = socket(AF_INET, SOCK_STREAM)
            # Connect to server
            self._client_socket.connect((self.target_host, self.target_port))

            user = str(input("Username: "))
            pwd = getpass()

            self._credentials["user"] = user
            self._credentials["pwd"] = pwd

            # Connect the user to the server
            self.send_data({"cmd": Cmd.LOGIN, "new": True} | self._credentials)

            self._log.log(
                f"Client {self.client_name} connected to server on {self.target_host}:{self.target_port}"
            )
        except Exception as e:
            self._log.log(f"Client {self.client_name} failed to connect: {e}")
            if self._client_socket is not None:
                self._client_socket.close()
                self._client_socket = None
                self._log.log(f"Client {self.client_name} socket closed.")
            print(e, "\nEnding client..")
            sys.exit(1)

    def send_data(self, data: dict) -> None:
        if self._client_socket is None:
            self._log.log(
                f"Client {self.client_name} failed to send data to the server: Socket is not set"
            )
            return
        try:
            utils.send(self._client_socket, data)
        except Exception as e:
            self._log.log(
                f"Client {self.client_name} failed to send data to the server: {e}"
            )

    def receive_data(self) -> dict | None:
        if self._client_socket is None:
            self._log.log(
                f"Client {self.client_name} failed to receive data to the server: {NotImplementedError('Client socket is not set')}"
            )
            return None
        try:
            res = utils.recv(self._client_socket)
            if res is None:
                self._log.log("Server offline")
                return None

            self._log.log(f"Client {self.client_name} received response: {res}")
            return res

        except Exception as e:
            self._log.log(
                f"Client {self.client_name} failed to receive data to the server: {e}"
            )
            return None

    def close_socket(self) -> None:
        if self._client_socket is None:
            return
        try:
            self._client_socket.close()
            self._log.log(f"Client {self.client_name} Socket Closed")
        except Exception as e:
            self._log.log(
                f"Client {self.client_name} failed to close the client socket: {e}"
            )

    def _login_client(self) -> None:
        self.send_data({"cmd": Cmd.LOGIN, "new": True} | self._credentials)
