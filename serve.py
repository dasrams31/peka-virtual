#!/usr/bin/env python3
"""Static server for the Peka Virtual Office (virtual.peka.ai.id)."""
import http.server
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8093


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    server.serve_forever()
