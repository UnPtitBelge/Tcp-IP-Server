from server.server import Server

host = "0.0.0.0"
port = 8080

if __name__ == "__main__":
    tcp_server = Server(host, port, backlog=5)
    tcp_server.start()
    tcp_server.serve()
