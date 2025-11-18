from client.client import Client

if __name__ == "__main__":
    clients: list[Client] = []
    for i in range(1):
        client: Client = Client(client_name=str(i))
        client.start_client()
        client.ping()
        res = client.receive_data()
        res1 = client.receive_data()
        print(res, res1)
        clients.append(client)

    for client in clients:
        client.close_socket()
