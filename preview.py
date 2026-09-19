"""Preview the site locally: python preview.py (Python standard library only)."""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import webbrowser

class PreviewHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".md": "text/plain; charset=utf-8",
    }
    def end_headers(self) -> None:
        # Only the local preview uses no-store; production hosting is unchanged.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        server = ThreadingHTTPServer(
            ("127.0.0.1", args.port), partial(PreviewHandler, directory=str(root))
        )
    except OSError as exc:
        parser.error(f"Cannot open port {args.port}: {exc}. Try --port 8001.")
    address = f"http://127.0.0.1:{args.port}/"
    print(f"Local preview: {address}\nPress Ctrl+C to stop.", flush=True)
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(address)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPreview stopped.")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
