import socket

HOST = "127.0.0.1"
PORT = 8001


def parse_cookies(request):

    cookies = {}

    lines = request.split("\r\n")

    for line in lines:

        if line.lower().startswith("cookie:"):

            cookie_header = line.split(":", 1)[1].strip()

            cookie_pairs = cookie_header.split(";")

            for pair in cookie_pairs:

                if "=" in pair:

                    name, value = pair.strip().split("=", 1)

                    cookies[name] = value

    return cookies


def create_response(body, set_cookie=None):

    body_bytes = body.encode("utf-8")

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
    )

    if set_cookie:

        response += f"Set-Cookie: {set_cookie}\r\n"

    response += "\r\n"

    return response.encode("utf-8") + body_bytes


def start_server():

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server_socket.bind((HOST, PORT))

    server_socket.listen(5)

    print("=" * 60)
    print("Cookie Management Server Started")
    print("=" * 60)
    print(f"Server address: http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)

    while True:

        client_socket, client_address = server_socket.accept()

        print()
        print("-" * 60)
        print(f"Client connected: {client_address}")

        try:

            request = client_socket.recv(4096).decode(
                "utf-8",
                errors="ignore"
            )

            print("Raw HTTP Request:")
            print(request)

            cookies = parse_cookies(request)

            if "UserID" in cookies:

                user_id = cookies["UserID"]

                print("Returning visitor detected.")
                print(f"UserID: {user_id}")

                body = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Cookie Management</title>
</head>

<body style="font-family: Arial; text-align: center; padding-top: 80px;">

    <h1>Welcome Back!</h1>

    <p>It is good to see you again.</p>

    <p>Your UserID is:</p>

    <h2>{user_id}</h2>

    <p>Your cookie was successfully read by the server.</p>

</body>
</html>
"""

                response = create_response(body)

            else:

                user_id = "User123"

                print("First-time visitor detected.")
                print("Creating cookie: UserID=User123")

                body = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Cookie Management</title>
</head>

<body style="font-family: Arial; text-align: center; padding-top: 80px;">

    <h1>Welcome!</h1>

    <p>You are visiting this server for the first time.</p>

    <p>Your UserID is:</p>

    <h2>{user_id}</h2>

    <p>A cookie has been created for you.</p>

</body>
</html>
"""

                cookie = "UserID=User123; Path=/"

                response = create_response(
                    body,
                    set_cookie=cookie
                )

            client_socket.sendall(response)

        except Exception as error:

            print(f"Error: {error}")

        finally:

            client_socket.close()

            print("Client connection closed.")


if __name__ == "__main__":

    try:

        start_server()

    except KeyboardInterrupt:

        print()
        print("Server stopped.")
