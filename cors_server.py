#!/usr/bin/env python3
import http.server, os

SERVE_DIR = os.path.expanduser("~/Documents/Claude/Projects/Agency OS")

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)
    def do_OPTIONS(self):
        self.send_response(200)
        self.add_cors()
        self.end_headers()
    def add_cors(self):
        self.send_header('Access-Control-Allow-Origin', 'https://drive.google.com')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
    def end_headers(self):
        self.add_cors()
        super().end_headers()
    def log_message(self, format, *args): pass

if __name__ == '__main__':
    with http.server.HTTPServer(('127.0.0.1', 18765), CORSHandler) as httpd:
        httpd.serve_forever()
