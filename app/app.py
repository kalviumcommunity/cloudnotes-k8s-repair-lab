#!/usr/bin/env python3
"""CloudNotes API — stdlib HTTP server. No third-party dependencies."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 5000
SERVICE_NAME = "cloudnotes-api"


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _json(self, status, data):
        self._send(status, json.dumps(data), "application/json")

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/health":
            self._json(
                200,
                {
                    "service": SERVICE_NAME,
                    "status": "ok",
                    "environment": os.environ.get("APP_ENV", ""),
                },
            )
            return
        if path == "/":
            self._send(
                200,
                "<!doctype html><title>CloudNotes</title><h1>CloudNotes</h1>",
                "text/html; charset=utf-8",
            )
            return
        self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"listening on {HOST}:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
