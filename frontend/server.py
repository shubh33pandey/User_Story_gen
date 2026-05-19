from __future__ import annotations

import json
import mimetypes
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

FRONTEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = FRONTEND_DIR.parent
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


class FrontendHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path.startswith("/generated_md/"):
            self.serve_generated_markdown()
            return

        if self.path == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        if self.path == "/ask":
            self.proxy_ask_request()
            return

        self.send_error(404, "Not found")

    def serve_generated_markdown(self):
        relative_path = self.path.removeprefix("/generated_md/").split("?", 1)[0]
        requested_path = (PROJECT_DIR / "generated_md" / relative_path).resolve()
        generated_dir = (PROJECT_DIR / "generated_md").resolve()

        if generated_dir not in requested_path.parents and requested_path != generated_dir:
            self.send_error(403, "Forbidden")
            return

        if not requested_path.exists() or not requested_path.is_file():
            self.send_error(404, "Markdown file not found")
            return

        content_type = mimetypes.guess_type(str(requested_path))[0] or "text/markdown"
        content = requested_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def proxy_ask_request(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body or b"{}")
        except json.JSONDecodeError:
            self.send_json({"success": False, "error": "Invalid JSON body"}, status=400)
            return

        request = Request(
            f"{BACKEND_URL}/ask",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=300) as response:
                response_body = response.read()
                status = response.status
                content_type = response.headers.get("Content-Type", "application/json")
        except HTTPError as error:
            response_body = error.read()
            status = error.code
            content_type = error.headers.get("Content-Type", "application/json")
        except URLError as error:
            self.send_json(
                {
                    "success": False,
                    "error": f"Cannot reach backend at {BACKEND_URL}. Start FastAPI first. Details: {error.reason}",
                },
                status=502,
            )
            return

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def send_json(self, payload, status=200):
        content = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    port = int(os.getenv("FRONTEND_PORT", "3000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), FrontendHandler)
    print(f"Frontend running at http://127.0.0.1:{port}")
    print(f"Proxying API requests to {BACKEND_URL}")
    server.serve_forever()
