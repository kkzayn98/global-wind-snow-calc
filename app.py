"""Desktop launcher — pywebview window (Windows .exe via PyInstaller)."""
import os
import socket
import sys
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler
import socketserver

import webview

APP_TITLE = "全球风压雪压计算评估工具"
APP_AUTHOR = "浙江中南新能源有限公司技术部 董子凌"
APP_VERSION = "1.0.0"
DEFAULT_PORT = 8765


def app_root() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.abspath(__file__))


ROOT = app_root()


def icon_path():
    path = os.path.join(ROOT, "assets", "app.ico")
    return path if os.path.isfile(path) else None


def find_free_port(start: int = DEFAULT_PORT) -> int:
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        pass


def start_server(port: int) -> None:
    handler = partial(Handler)
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        httpd.serve_forever()


def main() -> None:
    index = os.path.join(ROOT, "index.html")
    if not os.path.isfile(index):
        raise FileNotFoundError(f"Missing index.html at {index}")

    port = find_free_port()
    url = f"http://127.0.0.1:{port}/index.html"
    thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    thread.start()
    time.sleep(0.35)

    webview.create_window(
        title=APP_TITLE,
        url=url,
        width=1280,
        height=820,
        min_size=(900, 640),
    )
    start_kw: dict = {}
    icon = icon_path()
    if icon:
        start_kw["icon"] = icon
    webview.start(**start_kw)


if __name__ == "__main__":
    main()
