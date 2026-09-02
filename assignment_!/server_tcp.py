import socket

SERVER_NAME = "Server of Modi Ji"
SERVER_PORT = 5001
SERVER_INTEGER = 25


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow quick reuse of the port after restarting the server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(("0.0.0.0", SERVER_PORT))
    server_socket.listen(5)

    print("          TCP SERVER STARTED")
    print(f"Server Name : {SERVER_NAME}")
    print(f"Port        : {SERVER_PORT}")
    print("Waiting for client connection...")
    print()

    client_socket, client_address = server_socket.accept()

    print(f"Client connected from {client_address}")
    print()

    # Receive data from client
    data = client_socket.recv(1024).decode()

    client_name, client_number = data.split("|")
    client_number = int(client_number)

    print("---------- RECEIVED FROM CLIENT ----------")
    print(f"Client Name   : {client_name}")
    print(f"Client Integer: {client_number}")
    print()

    # Validate client number
    if client_number < 1 or client_number > 100:
        print("ERROR: Client integer is outside 1-100.")
        print("Closing connection...")

        client_socket.close()
        server_socket.close()
        return

    total = client_number + SERVER_INTEGER

    print("---------- SERVER RESPONSE ----------")
    print(f"Server Name   : {SERVER_NAME}")
    print(f"Server Integer: {SERVER_INTEGER}")
    print(f"Sum           : {total}")
    print()

    # Send server information back to client
    response = f"{SERVER_NAME}|{SERVER_INTEGER}"
    client_socket.send(response.encode())

    print("Response sent to client.")
    print("Closing sockets...")

    client_socket.close()
    server_socket.close()

    print("Server terminated.")


if __name__ == "__main__":
    main()