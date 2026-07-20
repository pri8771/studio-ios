#!/usr/bin/env python3
"""Serve a generated Studio OS portal on loopback only."""
from __future__ import annotations
import argparse, http.server, socket
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def available(preferred: int) -> int:
    for port in range(preferred, preferred + 100):
        with socket.socket() as sock:
            if sock.connect_ex(("127.0.0.1", port)) != 0: return port
    raise RuntimeError("No free local port in preferred range")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--port", type=int, default=8787); args = parser.parse_args(); portal = ROOT / "generated/local-portal"; port = available(args.port)
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=str(portal), **kw)
    print(f"Studio OS local portal: http://127.0.0.1:{port}/", flush=True); http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever(); return 0
if __name__ == "__main__": raise SystemExit(main())
