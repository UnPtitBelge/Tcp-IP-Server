from server.server import Server

if __name__ == "__main__":
    tcp_server = Server(backlog=5)
    tcp_server.serve()
