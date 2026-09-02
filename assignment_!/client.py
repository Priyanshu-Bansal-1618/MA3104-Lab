import socket

SERVER_IP = "192.170.3.186"   # this is the ip address of device on which server is running
SERVER_PORT = 5002

CLIENT_NAME = "Client of Priyanshu"


def main():

    while True:

        try:
            client_number = int(
                input("Enter an integer between 1 and 100: ")
            )

            if 1 <= client_number <= 100:
                break

            print("Please enter a number between 1 and 100.")

        except ValueError:
            print("Please enter a valid integer.")

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    print()
    print("Sending UDP datagram...")

    message = f"{CLIENT_NAME}|{client_number}"

    client_socket.sendto(
        message.encode(),
        (SERVER_IP, SERVER_PORT)
    )

    print("---------- SENT TO SERVER ----------")
    print(f"Client Name   : {CLIENT_NAME}")
    print(f"Client Integer: {client_number}")
    print()

    # Wait for server response
    data, server_address = client_socket.recvfrom(1024)

    server_name, server_number = data.decode().split("|")
    server_number = int(server_number)

    total = client_number + server_number

    print("---------- RECEIVED FROM SERVER ----------")
    print(f"Client Name   : {CLIENT_NAME}")
    print(f"Server Name   : {server_name}")
    print(f"Client Integer: {client_number}")
    print(f"Server Integer: {server_number}")
    print(f"Sum           : {total}")
    print()

    client_socket.close()

    print("UDP socket closed.")
    print("UDP client terminated.")


if __name__ == "__main__":
    main()