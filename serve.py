#!/usr/bin/env python3
"""Local dev server for browser debugging."""
import http.server
import os
import socket
import socketserver
import sys
import webbrowser
from functools import partial

DEFAULT_PORT = 8080
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    """Serve project root; redirect / to index.html."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("", "/"):
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
            return
        # Common wrong URLs → hint
        if path in ("/calc", "/calc/", "/calc/index.html"):
            self.send_error(
                404,
                "路径错误：请在 calc 目录运行 serve.py，访问 http://localhost:端口/index.html",
            )
            return
        return super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("[serve] " + (fmt % args) + "\n")


class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def find_free_port(start: int = DEFAULT_PORT, tries: int = 20) -> int:
    for port in range(start, start + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise OSError(f"No free port in range {start}-{start + tries - 1}")


def main():
    os.chdir(ROOT)
    if not os.path.isfile(os.path.join(ROOT, "index.html")):
        print(f"错误：未找到 index.html，当前目录应为：{ROOT}", file=sys.stderr)
        sys.exit(1)

    port = find_free_port()
    handler = partial(Handler)
    with ReuseTCPServer(("", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/index.html"
        print("=" * 56)
        print("全球风压雪压计算评估工具 — 本地调试服务已启动")
        print(f"  请用浏览器打开: {url}")
        print(f"  或:             http://localhost:{port}/index.html")
        if port != DEFAULT_PORT:
            print(f"  （8080 被占用，已改用端口 {port}）")
        print("  不要用 www.localhost.com")
        print("  按 Ctrl+C 停止")
        print("=" * 56)
        try:
            webbrowser.open(url)
        except Exception:
            pass
        httpd.serve_forever()


if __name__ == "__main__":
    main()
