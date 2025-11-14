# callback_server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract the authorization code from the URL
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get("code", [None])[0]

        if code:
            print(f"Authorization code: {code}")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authorization code received. You can close this window.")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authorization code not found.")

def run_server():
    server_address = ("localhost", 8888)
    httpd = HTTPServer(server_address, CallbackHandler)
    print("Server running on http://localhost:8888...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()