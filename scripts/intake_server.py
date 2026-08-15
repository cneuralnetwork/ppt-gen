#!/usr/bin/env python3
"""Serve the PPT Gen intake on localhost and persist the confirmed brief."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.dont_write_bytecode = True

from validate_brief import normalize_brief, validate_brief


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DASHBOARD_DIR = SKILL_DIR / "assets" / "dashboard"
MAX_BODY_BYTES = 2 * 1024 * 1024


def load_prefill(path: Path | None) -> dict:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Prefill file not found: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Prefill JSON must be an object")
    return raw


class IntakeServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address, handler, *, prefill: dict, result_path: Path, keep_open: bool):
        super().__init__(server_address, handler)
        self.prefill = prefill
        self.result_path = result_path
        self.keep_open = keep_open
        self.submitted = threading.Event()


class Handler(BaseHTTPRequestHandler):
    server: IntakeServer

    def log_message(self, format: str, *args) -> None:
        print(f"PPT_INTAKE_HTTP {self.address_string()} {format % args}", flush=True)

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self.send_json(HTTPStatus.OK, {"ok": True})
            return
        if path == "/api/prefill":
            self.send_json(HTTPStatus.OK, self.server.prefill)
            return

        requested = "index.html" if path in ("", "/") else path.lstrip("/")
        if requested not in {"index.html", "styles.css", "app.js"}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        file_path = DASHBOARD_DIR / requested
        if not file_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/submit":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "errors": ["Invalid Content-Length"]})
            return
        if length <= 0 or length > MAX_BODY_BYTES:
            self.send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"ok": False, "errors": ["Brief payload is empty or too large"]})
            return

        try:
            incoming = json.loads(self.rfile.read(length).decode("utf-8"))
            brief = normalize_brief(incoming)
            errors = validate_brief(brief, final=True)
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "errors": [str(exc)]})
            return

        if errors:
            self.send_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"ok": False, "errors": errors})
            return

        self.server.result_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.server.result_path.with_suffix(self.server.result_path.suffix + ".tmp")
        temp_path.write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
        os.replace(temp_path, self.server.result_path)
        self.server.submitted.set()
        self.send_json(HTTPStatus.OK, {"ok": True, "result": str(self.server.result_path)})
        print(f"PPT_INTAKE_SUBMITTED={self.server.result_path}", flush=True)

        if not self.server.keep_open:
            threading.Thread(target=self._shutdown_soon, daemon=True).start()

    def _shutdown_soon(self) -> None:
        time.sleep(0.4)
        self.server.shutdown()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefill", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--open", action="store_true", dest="open_browser")
    parser.add_argument("--no-open", action="store_false", dest="open_browser")
    parser.add_argument("--keep-open", action="store_true")
    parser.set_defaults(open_browser=False)
    args = parser.parse_args()

    prefill = load_prefill(args.prefill)
    server = IntakeServer(("127.0.0.1", args.port), Handler, prefill=prefill, result_path=args.result.resolve(), keep_open=args.keep_open)
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"PPT_INTAKE_URL={url}", flush=True)
    print(f"PPT_INTAKE_RESULT={server.result_path}", flush=True)
    print("PPT_INTAKE_READY=1", flush=True)

    if args.open_browser:
        threading.Timer(0.15, lambda: webbrowser.open(url, new=2)).start()

    try:
        server.serve_forever(poll_interval=0.15)
    except KeyboardInterrupt:
        print("PPT_INTAKE_STOPPED=1", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
