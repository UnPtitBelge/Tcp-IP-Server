# src/server.py
import socket
import threading

from src.utils.log import Logger


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
            pass
        finally:
            self.stop()

    def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        if self._server_sock:
            try:
                self._server_sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self._server_sock.close()
            finally:
                self._server_sock = None
        self._log.log("Server stopped")

    def _handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        addr_str = f"{addr[0]}:{addr[1]}"
        self._log.log(f"Accepted connection from {addr_str}")

        try:
            request = conn.recv(1024)
            self._log.log(f"Request received: {request}")
            # Treat request
            conn.send("Ping back".encode())

        except Exception as e:
            self._log.log(f"Connection error with {addr_str}: {e}")
        finally:
            self._log.log(f"Connection closed from {addr_str}")
            conn.close()
