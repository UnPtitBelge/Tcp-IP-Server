# src/server/server.py
import socket
import threading

from utils import Cmd, Logger, utils


class Server:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        backlog: int = 100,
    ):
        self.host: str = host
        self.port: int = port
        self.backlog: int = backlog

        # Clients conected to the server
        self._clients_sock: set[socket.socket] = set()

        self._server_sock: socket.socket | None = None
        self._running: bool = False

        self._log: Logger = Logger("server.log")

    def serve(self) -> None:
        """Start the server and the loop accepting clients"""
        self._start()
        assert self._server_sock is not None

        try:
            while self._running:
                try:
                    # Accept incoming connection
                    sock, addr = self._server_sock.accept()
                except OSError as e:
                    if not self._running:
                        break
                    self._log.log(f"Error accepting connection: {e}")
                    continue

                # Add the accepted socket to the set
                self._clients_sock.add(sock)

                # Launch the client dedicated thread
                c_thread = threading.Thread(
                    target=self._handle_client, args=(sock, addr), daemon=True
                )
                c_thread.start()
        except KeyboardInterrupt:  # CTRL-C
            self._log.log("KeyboardInterrupt: Closing server.")
        finally:
            self._stop()

    def _start(self) -> None:
        """Open the server socket and make it ready to serve"""
        if self._server_sock is not None:
            return

        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind((self.host, self.port))
        self._server_sock.listen(self.backlog)

        self._running = True
        self._log.log(f"Server listening on {self.host}:{self.port}")

    def _stop(self) -> None:
        if not self._running:
            return
        self._running = False

        if self._server_sock:
            try:
                self._server_sock.shutdown(socket.SHUT_RDWR)
            except OSError as os_e:
                self._log.log(f"Error trying to close server: {os_e}")
            finally:
                self._server_sock.close()
                self._server_sock = None
        self._log.log("Server stopped")

    def _handle_client(self, sock: socket.socket, addr: tuple[str, int]) -> None:
        """Handle the dedicated loop for a specified client soccket. Deal with the requests"""

        addr_str = f"{addr[0]}:{addr[1]}"  # For debug/log

        self._log.log(f"Accepted connection from {addr_str}")

        try:
            while True:
                request = utils.recv(sock)  # wait for data

                if request is None:  # Socket is closed by the client
                    raise Exception("Client disconnected")

                # Prep and send the response (if there is one)
                res = self._handle_request(request)
                if res is not None:
                    utils.send(sock, res)

        except Exception as e:
            self._log.log(f"Error with socket {addr_str}: {e}")
        finally:
            sock.close()
            self._log.log(f"Client Socket closed {addr_str}")

    def _handle_request(self, request: dict) -> dict | None:
        """Match case the right command to handle a request sent by a client."""
        match request["cmd"]:
            case Cmd.PING:
                return {"cmd": Cmd.PING}
            case Cmd.LOGIN:
                return self._login_client(request)
            case Cmd.SEND_MESSAGE:
                pass
            case Cmd.GET_DATA:
                raise NotImplementedError
            case _:
                raise NotImplementedError(f"Uknown request's command: {request['cmd']}")

    def _login_client(self, data: dict) -> dict | None:
        user = data["user"]
        pwd = data["pwd"]
        new_conn = data["new"]  # Flag for new user

        # Set response dict
        res = {
            "cmd": Cmd.LOGIN,
            "done": True,
            "size": False,
            "user": True,
            "pwd": True,
        }

        # Checks for correct format
        if 3 > len(user) >= 32:
            res["user"] = False
        elif 3 > len(pwd) >= 32:
            res["pwd"] = False
        else:
            res["size"] = True

        # TODO: Lookup in JSON or database for user and pwd or insert if new connection (use of scrypt for pwd)

        print(user, pwd)  # Test purpose

        return res
