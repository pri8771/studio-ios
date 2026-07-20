#!/usr/bin/env python3
"""Inject task command-center controls into the generated static dashboard."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "dashboard" / "index.html"

STYLE = """
.command-actions{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}.button{appearance:none;border:0;border-radius:10px;background:#18181b;color:white;padding:10px 14px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block}.button.secondary{background:#e4e4e7;color:#18181b}.command-summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:14px 0}.command-note{color:#71717a;font-size:.88rem}.command-table{min-width:1100px}a{color:inherit}
"""

SECTION = """
<h2>Task command center</h2>
<p class="sub">Create assignable work, monitor execution, and review human approval gates. GitHub Issues remain the durable task record.</p>
<div class="command-actions">
  <button class="button" data-new-task>Create task</button>
  <button class="button secondary" data-approval-queue>Approval queue</button>
  <a class="button secondary" href="https://github.com/pri8771/studio-ios/issues?q=is%3Aissue+label%3Astudio-task" target="_blank" rel="noreferrer">All tasks in GitHub</a>
</div>
<section class="command-summary">
  <article><div class="metric" id="command-open">—</div><div>Open tasks</div></article>
  <article><div class="metric" id="command-running">—</div><div>Running</div></article>
  <article><div class="metric" id="command-blocked">—</div><div>Blocked</div></article>
  <article><div class="metric" id="command-approvals">—</div><div>Approval needed</div></article>
</section>
<p class="command-note" id="task-freshness">Loading task snapshot…</p>
<section class="panel"><table class="command-table"><thead><tr><th>Task</th><th>Product</th><th>Owner</th><th>Priority</th><th>Status</th><th>Due</th><th>Approval gate</th><th></th></tr></thead><tbody id="task-issue-rows"><tr><td colspan="8">Loading…</td></tr></tbody></table></section>
"""


def main() -> int:
    text = INDEX.read_text(encoding="utf-8")
    if "data-new-task" not in text:
        text = text.replace("</style>", STYLE + "</style>")
        text = text.replace("</main>", SECTION + "</main>")
        text = text.replace("</body>", '<script src="./command-center.js"></script></body>')
        INDEX.write_text(text, encoding="utf-8")
    print("Dashboard command center ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
