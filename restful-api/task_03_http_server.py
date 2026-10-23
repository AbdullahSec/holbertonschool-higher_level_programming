#!/usr/bin/python3
"""Serve a small JSON API using Python's built-in HTTP server."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Handle the API's basic text and JSON endpoints."""

    def _send_text(self, status, message):
        """Send a UTF-8 plain-text response."""
        body = message.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status, data):
        """Send a JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Route GET requests to the available endpoints."""
        if self.path == "/":
            self._send_text(200, "Hello, this is a simple API!")
        elif self.path == "/data":
            self._send_json(
                200, {"name": "John", "age": 30, "city": "New York"}
            )
        elif self.path == "/status":
            self._send_text(200, "OK")
        elif self.path == "/info":
            self._send_json(
                200,
                {
                    "version": "1.0",
                    "description": "A simple API built with http.server",
                },
            )
        else:
            self._send_text(404, "Endpoint not found")


if __name__ == "__main__":
    server = HTTPServer(("", 8000), SimpleAPIHandler)
    print("Serving API on port 8000...")
    server.serve_forever()
