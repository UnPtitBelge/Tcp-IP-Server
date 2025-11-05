# Basic client for server test
from socket import socket, AF_INET, SOCK_STREAM
from utils.log import Logger
import sys
from getpass import getpass


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
            self._login_client()

            self._log.log(
                f"Client {self.client_name} connected to server on {self.target_host}:{self.target_port}"
            )
        except Exception as e:
            self._log.log(f"Client {self.client_name} failed to start: {e}")
            if self._client_socket is not None:
                self._client_socket.close()
                self._client_socket = None
                self._log.log(f"Client {self.client_name} socket closed.")
            print(e, "\nEnding client..")
            sys.exit(1)

    def send_data(self, data: str) -> None:
        if self._client_socket is None:
            self._log.log(
                f"Client {self.client_name} failed to send data to the server: Socket is not set"
            )
            return
        try:
            self._client_socket.send(data.encode())
        except Exception as e:
            self._log.log(
                f"Client {self.client_name} failed to send data to the server: {e}"
            )

    def receive_data(self) -> str:
        if self._client_socket is None:
            self._log.log(
                f"Client {self.client_name} failed to receive data to the server: {NotImplementedError('Client socket is not set')}"
            )
            return ""
        try:
            res = self._client_socket.recv(4096)
            if len(res) == 0:
                self._log.log("Server offline")
                return ""
            self._log.log(f"Client {self.client_name} received response: {res}")
            return res.decode()
        except Exception as e:
            self._log.log(
                f"Client {self.client_name} failed to receive data to the server: {e}"
            )
            return ""

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
        pass
