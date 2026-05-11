#!/usr/bin/env python3
"""Crab Trap MUD — Web Server

Serves the MUD explorer on port 4064.
The heavy lifting is all client-side JS talking to the Keeper and PLATO APIs.

Usage:
    python3 server.py
    # Open http://localhost:4064
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            path = os.path.join(DIR, 'index.html')
            if os.path.exists(path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                with open(path, 'rb') as f:
                    self.wfile.write(f.read())
                return
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'404 Not Found')

    def log_message(self, fmt, *args):
        print(f'[crab-trap] {args[0]} {args[1]} {args[2]}')

if __name__ == '__main__':
    port = 4064
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'🦀 Crab Trap MUD running on http://0.0.0.0:{port}')
    print(f'   Open http://localhost:{port} in your browser')
    server.serve_forever()
