import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LocalFirstTests(unittest.TestCase):
    def test_workspace_preview_does_not_create_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "workspace"
            result = subprocess.run([sys.executable, "scripts/setup_local_workspace.py", "--root", str(root), "--product", "Document Flow"], cwd=ROOT, text=True, capture_output=True, check=True)
            report = json.loads(result.stdout)
            self.assertEqual(report["mode"], "preview")
            self.assertFalse(root.exists())

    def test_dashboard_generation_produces_json(self):
        subprocess.run([sys.executable, "scripts/generate_dashboard.py"], cwd=ROOT, check=True)
        data = json.loads((ROOT / "dashboard/data.json").read_text(encoding="utf-8"))
        self.assertTrue(data["localOnly"])
        self.assertIn("products", data)
        document_flow = next(product for product in data["products"] if product["id"] == "PROD-DOCUMENT-FLOW")
        self.assertEqual(document_flow["current_milestone"], "Local text, image, and PDF processing verified")
        self.assertNotIn("task:", document_flow["next_action"])
