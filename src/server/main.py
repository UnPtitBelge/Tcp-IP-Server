from server.server import Server

host = "0.0.0.0"
port = 8080

if __name__ == "__main__":
    tcp_server = Server(host, port, backlog=5)
    tcp_server.start()
    try:
        tcp_server.serve()
    except KeyboardInterrupt:
        tcp_server.stop()
