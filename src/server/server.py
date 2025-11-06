# src/server/server.py
import socket
import threading

from utils import Cmd, Logger, utils


class Server:
    def __init__(
        self,
        host: str,
        port: int,
        backlog: int = 100,
    ):
        self.host: str = host
        self.port: int = port
        self.backlog: int = backlog

        self._server_sock: socket.socket | None = None
        self._running: bool = False

        self._log: Logger = Logger("server.log")

    def start(self) -> None:
        if self._server_sock is not None:
            return

        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind((self.host, self.port))
        self._server_sock.listen(self.backlog)

        self._running = True
        self._log.log(f"Server listening on {self.host}:{self.port}")

    def serve(self) -> None:
        self.start()
        assert self._server_sock is not None

        try:
            while self._running:
                try:
                    conn, addr = self._server_sock.accept()
                except OSError as e:
                    if not self._running:
                        break
                    self._log.log(f"Error accepting connection: {e}")
                    continue

                c_thread = threading.Thread(
                    target=self._handle_client, args=(conn, addr), daemon=True
                )
                c_thread.start()
        except KeyboardInterrupt:
            self._log.log("KeyboardInterrupt: Closing server.")
        finally:
            self.stop()

    def stop(self) -> None:
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
        addr_str = f"{addr[0]}:{addr[1]}"
        self._log.log(f"Accepted connection from {addr_str}")

        try:
            while True:
                request = utils.recv(sock)

                if request is None:
                    raise Exception("Client disconnected")

                res = self._handle_request(request)
                if res is not None:
                    utils.send(sock, res)

        except Exception as e:
            self._log.log(f"Error with socket {addr_str}: {e}")
        finally:
            sock.close()
            self._log.log(f"Client Socket closed{addr_str}")

    def _handle_request(self, request: dict) -> dict | None:
        match request["cmd"]:
            case Cmd.PING:
                return {"cmd": Cmd.PING, "data": "Ping"}
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

        res = {
            "cmd": Cmd.LOGIN,
            "done": False,
            "size": False,
            "user": True,
            "pwd": True,
        }

        res["size"] = True if 3 <= len(pwd) < 32 and 3 <= len(user) < 32 else False
        # TODO: Lookup in JSON or database for user and pwd or insert if new connection (use of scrypt for pwd)

        return res
