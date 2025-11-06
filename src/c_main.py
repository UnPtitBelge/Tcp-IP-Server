from client.client import Client
from utils import Cmd

target_h = "0.0.0.0"
target_p = 8080

if __name__ == "__main__":
    clients: list[Client] = []
    for i in range(1):
        client: Client = Client(target_h, target_p, str(i))
        client.start_client()
        client.send_data({"cmd": Cmd.PING})
        res = client.receive_data()
        res1 = client.receive_data()
        print(res, res1)
        clients.append(client)

    for client in clients:
        client.close_socket()
