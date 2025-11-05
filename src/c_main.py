from client.client import Client

target_h = "0.0.0.0"
target_p = 8080

if __name__ == "__main__":
    clients: list[Client] = []
    for i in range(7):
        client: Client = Client(target_h, target_p, str(i))
        client.start_client()
        # client.send_data("Nice")
        res = client.receive_data()
        print(res)
        clients.append(client)

    for client in clients:
        client.close_socket()
