# Basic client for server test
import sys
from getpass import getpass
from socket import AF_INET, SOCK_STREAM, socket

from utils import Cmd, Logger, utils
from utils.enum import Login


class Client:
    def __init__(
        self,
        target_host: str = "127.0.0.1",
        target_port: int = 8080,
        client_name: str = "name",
    ) -> None:
        self.target_host = target_host
        self.target_port = target_port
        self.client_name = client_name  # For log puprose (maybe more use in future)

        self._client_socket: socket | None = None

        self._log: Logger = Logger("client.log")

    def start_client(self) -> None:
        """Create and connect the client to the server through the socket, then
        connect the client to his account (not yet implemented on the server side)
        """

        if self._client_socket is not None:
            return
        try:
            # Create socket
            self._client_socket = socket(AF_INET, SOCK_STREAM)

            # Connect to server
            self._client_socket.connect((self.target_host, self.target_port))

            # Get credentials
            user = str(input("Username: "))
            pwd = getpass()

            # Connect the user to the server (for now new user flag always at true)
            self._login(Cmd.LOGIN, user, pwd)

            self._log.log(
                f"Client {self.client_name} connected to server on {self.target_host}:{self.target_port}"
            )
        # An exception will result on the server being shutdown or a critical error on the client side
        except Exception as e:
            self._log.log(f"Client {self.client_name} failed to connect: {e}")
            if self._client_socket is not None:
                self._client_socket.close()
                self._log.log(f"Client {self.client_name} socket closed.")
            print(e, "\nEnding client..")
            sys.exit()

    def receive_data(self) -> dict | None:
        """Receive the response of the server and returns it in a dict format (see recv(..) in utils.py)"""
        if self._client_socket is None:
            raise Exception(
                "Failed to receive data from server: Client socket is not set"
            )
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
        """Properly close the socket"""
        if self._client_socket is None:
            return
        try:
            self._client_socket.close()
            self._log.log(f"Client {self.client_name} Socket Closed")
        except Exception as e:
            self._log.log(
                f"Client {self.client_name} failed to close the client socket: {e}"
            )

    def ping(self) -> None:
        """Ping the server"""
        if self._client_socket is None:
            raise Exception("Client socket is not set")

        packet = utils.pack(Cmd.PING)
        self._client_socket.sendall(packet)

    def _login(self, cmd: str, user: str, pwd: str, new_conn: bool = True) -> None:
        if self._client_socket is None:
            raise Exception("Client socket is not set")
        packet = utils.pack(
            cmd, {Login.USER: user, Login.PWD: pwd, Login.NEW_CONN: new_conn}
        )
        self._client_socket.sendall(packet)
