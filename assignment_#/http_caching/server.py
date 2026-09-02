import http.server
import socketserver
import hashlib
import os
from email.utils import formatdate

PORT = 8000
FILE_NAME = "index.html"


class CachingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/" or self.path == "/index.html":

            if not os.path.exists(FILE_NAME):
                self.send_error(404, "index.html not found")
                return

            with open(FILE_NAME, "rb") as file:
                content = file.read()

            etag = '"' + hashlib.md5(content).hexdigest() + '"'

            modification_time = os.path.getmtime(FILE_NAME)

            last_modified = formatdate(
                modification_time,
                usegmt=True
            )

            client_etag = self.headers.get("If-None-Match")
            client_last_modified = self.headers.get("If-Modified-Since")

            if client_etag == etag:

                print("ETag matched -> Sending 304 Not Modified")

                self.send_response(304)
                self.send_header("ETag", etag)
                self.send_header("Last-Modified", last_modified)
                self.end_headers()

                return

            if client_last_modified == last_modified:

                print("Last-Modified matched -> Sending 304 Not Modified")

                self.send_response(304)
                self.send_header("ETag", etag)
                self.send_header("Last-Modified", last_modified)
                self.end_headers()

                return

            print("Cache not valid -> Sending 200 OK with file")

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("ETag", etag)
            self.send_header("Last-Modified", last_modified)
            self.end_headers()

            self.wfile.write(content)

        else:
            self.send_error(404, "File not found")


with socketserver.TCPServer(("", PORT), CachingHTTPRequestHandler) as server:

    print("=" * 60)
    print("HTTP Caching Server Started")
    print("=" * 60)
    print(f"Server address: http://localhost:{PORT}")
    print(f"Serving file: {FILE_NAME}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)

    server.serve_forever()
