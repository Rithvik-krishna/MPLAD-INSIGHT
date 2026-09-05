"""
NIDHI TRACE Server with Integrated NIDHI Assistant Endpoint
Serves:
1. Static HTML/JS/CSS assets for NIDHI TRACE on port 3000
2. POST /api/assistant/chat -> NIDHI Assistant AI Audit Copilot
3. GET /api/assistant/status -> Operational status & mode
"""

import sys
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from backend.assistant_service import handle_chat_request, get_assistant_status

class NidhiTraceRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        url_path = self.path.split('?')[0]

        if url_path == '/api/assistant/status':
            status = get_assistant_status()
            resp_bytes = json.dumps(status).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self._set_cors_headers()
            self.send_header('Content-Length', str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # Default static file handling
        return super().do_GET()

    def do_POST(self):
        url_path = self.path.split('?')[0]

        if url_path == '/api/assistant/chat':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0:
                    self._send_json({"status": "bad_request", "message": "Empty body"}, status_code=400)
                    return

                raw_body = self.rfile.read(content_length).decode('utf-8')
                try:
                    body = json.loads(raw_body)
                except json.JSONDecodeError:
                    self._send_json({"status": "bad_request", "message": "Invalid JSON format"}, status_code=400)
                    return

                client_ip = self.client_address[0] if self.client_address else "127.0.0.1"
                result = handle_chat_request(body, client_ip=client_ip)

                status_code = 200
                if result.get("status") == "rate_limited":
                    status_code = 429
                elif result.get("status") == "bad_request":
                    status_code = 400

                self._send_json(result, status_code=status_code)

            except Exception as e:
                print(f"[NIDHI Server] Error processing chat request: {e}")
                self._send_json({
                    "status": "error",
                    "message": "NIDHI Assistant couldn't complete that request. Please try again.",
                    "mode": "error"
                }, status_code=500)
            return

        self.send_error(404, "Endpoint not found")

    def _send_json(self, data: dict, status_code: int = 200):
        resp_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._set_cors_headers()
        self.send_header('Content-Length', str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def log_message(self, format, *args):
        # Clean logging without leaking credentials or request bodies
        first_arg = args[0] if args else ""
        if "/api/assistant" in str(first_arg):
            sys.stderr.write(f"[{self.log_date_time_string()}] API: {format % args}\n")
        else:
            # Minimal static file logging
            pass

def run_server(port=3000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, NidhiTraceRequestHandler)
    print(f"==================================================")
    print(f"  NIDHI TRACE Institutional Platform & Assistant  ")
    print(f"==================================================")
    print(f"  Local URL:  http://localhost:{port}/")
    print(f"  API:        http://localhost:{port}/api/assistant/chat")
    print(f"  Status:     http://localhost:{port}/api/assistant/status")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '3000'))
    run_server(port)
