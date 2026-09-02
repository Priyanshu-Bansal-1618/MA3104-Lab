import socket

SERVER_NAME = "Server of Modi Ji"
SERVER_PORT = 5002
SERVER_INTEGER = 25


def main():

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    server_socket.bind(("0.0.0.0", SERVER_PORT))

    print("          UDP SERVER STARTED")
    print(f"Server Name : {SERVER_NAME}")
    print(f"Port        : {SERVER_PORT}")
    print("Waiting for UDP datagram...")
    print()

    # Receive message from client
    data, client_address = server_socket.recvfrom(1024)

    message = data.decode()

    client_name, client_number = message.split("|")
    client_number = int(client_number)

    print(f"Client address: {client_address}")
    print()

    print("---------- RECEIVED FROM CLIENT ----------")
    print(f"Client Name   : {client_name}")
    print(f"Client Integer: {client_number}")
    print()

    # Validate number
    if client_number < 1 or client_number > 100:

        print("ERROR: Client integer is outside 1-100.")
        print("Closing socket...")

        server_socket.close()
        return

    total = client_number + SERVER_INTEGER

    print("---------- SERVER RESPONSE ----------")
    print(f"Server Name   : {SERVER_NAME}")
    print(f"Server Integer: {SERVER_INTEGER}")
    print(f"Sum           : {total}")
    print()

    # Send response back to client
    response = f"{SERVER_NAME}|{SERVER_INTEGER}"

    server_socket.sendto(
        response.encode(),
        client_address
    )

    print("Response sent to client.")
    print("Closing socket...")

    server_socket.close()

    print("UDP server terminated.")


if __name__ == "__main__":
    main()