#!/usr/bin/env python3
"""Build and serve the Studio OS dashboard and public-site preview locally.

Uses only the Python standard library. It does not mutate external systems,
create accounts, or require Docker. Generated output lives under
`generated/local-portal/` and may be safely deleted and regenerated.
"""
from __future__ import annotations

import argparse
import contextlib
import http.server
import shutil
import socket
import socketserver
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "generated" / "local-portal"


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def copy_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        raise RuntimeError(f"Expected generated path is missing: {source}")
    shutil.copytree(source, destination, dirs_exist_ok=True)


def build(skip_validation: bool = False) -> Path:
    run([sys.executable, "scripts/setup_local_data.py"])
    if not skip_validation:
        run([sys.executable, "scripts/validate_repo.py"])
        run([sys.executable, "scripts/check_standard_drift.py"])

    run([sys.executable, "scripts/generate_dashboard.py"])
    run([sys.executable, "scripts/generate_public_site.py"])

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)

    copy_tree(ROOT / "dashboard", OUTPUT / "dashboard")
    copy_tree(ROOT / "generated" / "public-site", OUTPUT / "website")

    (OUTPUT / "index.html").write_text(
        """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
  <title>Studio OS Local</title>
  <style>
    :root{font-family:Inter,ui-sans-serif,system-ui,-apple-system,sans-serif;color:#171717;background:#f4f4f5}
    *{box-sizing:border-box}body{margin:0}main{max-width:980px;margin:0 auto;padding:56px 24px}
    .eyebrow{font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color:#71717a;font-weight:700}
    h1{font-size:clamp(2.4rem,7vw,5rem);line-height:.95;margin:14px 0 18px;letter-spacing:-.055em}
    .lead{font-size:1.1rem;color:#52525b;max-width:680px;line-height:1.6}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px;margin-top:38px}
    a{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #e4e4e7;border-radius:20px;padding:24px;box-shadow:0 8px 30px #18181b0d;transition:.18s transform,.18s box-shadow}
    a:hover{transform:translateY(-3px);box-shadow:0 14px 40px #18181b18}.tag{font-size:.76rem;color:#71717a;text-transform:uppercase;letter-spacing:.08em}
    h2{margin:9px 0 8px;font-size:1.45rem}.desc{color:#52525b;line-height:1.5}.arrow{margin-top:22px;font-weight:700}
    footer{margin-top:42px;color:#71717a;font-size:.86rem}
  </style>
</head>
<body><main>
  <div class=\"eyebrow\">Local control plane</div>
  <h1>Studio OS</h1>
  <p class=\"lead\">A local-only view of the product portfolio and the sanitized shared website. Everything here is regenerated from repository records.</p>
  <section class=\"grid\">
    <a href=\"dashboard/\"><div class=\"tag\">Private operations</div><h2>Portfolio dashboard</h2><div class=\"desc\">Products, shared services, blockers, verification, and the Atlas/human queue.</div><div class=\"arrow\">Open dashboard →</div></a>
    <a href=\"website/\"><div class=\"tag\">Public preview</div><h2>Shared website</h2><div class=\"desc\">The opt-in, sanitized product site. Unpublished products are excluded by default.</div><div class=\"arrow\">Open website →</div></a>
  </section>
  <footer>Generated locally. Private CRM, content, inbox, calendar, and approval stores live under the git-ignored <code>.local/</code> directory.</footer>
</main></body></html>""",
        encoding="utf-8",
    )
    print(f"Built local portal: {OUTPUT / 'index.html'}")
    return OUTPUT


def free_port(preferred: int) -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex(("127.0.0.1", preferred)) != 0:
            return preferred
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def serve(directory: Path, port: int, open_browser: bool = True) -> None:
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(  # noqa: E731
        *args, directory=str(directory), **kwargs
    )

    class ReusableTCPServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    with ReusableTCPServer(("127.0.0.1", port), handler) as server:
        url = f"http://127.0.0.1:{port}/"
        print(f"Serving Studio OS locally at {url}")
        print("Press Ctrl+C to stop.")
        if open_browser:
            threading.Thread(target=lambda: (time.sleep(0.4), webbrowser.open(url)), daemon=True).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped local Studio OS server.")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Build and serve the local Studio OS portal")
    p.add_argument("--port", type=int, default=8787)
    p.add_argument("--build-only", action="store_true")
    p.add_argument("--no-open", action="store_true")
    p.add_argument("--skip-validation", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        output = build(skip_validation=args.skip_validation)
        if args.build_only:
            return 0
        serve(output, free_port(args.port), open_browser=not args.no_open)
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"Local portal build failed because a required check exited {exc.returncode}.", file=sys.stderr)
        return exc.returncode
    except Exception as exc:
        print(f"Local portal error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
