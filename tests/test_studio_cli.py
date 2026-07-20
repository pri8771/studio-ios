from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "studio_cli.py"
SPEC = importlib.util.spec_from_file_location("studio_cli", MODULE_PATH)
assert SPEC and SPEC.loader
studio_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(studio_cli)


class StudioCLITests(unittest.TestCase):
    def test_slugify(self) -> None:
        self.assertEqual(studio_cli.slugify("Document Flow"), "document-flow")
        self.assertEqual(studio_cli.slugify("  Jyot / Daily  "), "jyot-daily")
        with self.assertRaises(studio_cli.StudioError):
            studio_cli.slugify("---")

    def test_document_ai_template_has_required_boundaries(self) -> None:
        files = studio_cli.document_ai_files("Document Flow", "document-flow")
        required = {
            "docker-compose.yml",
            "api/app/main.py",
            "web/src/main.tsx",
            ".github/workflows/ci.yml",
            "docs/ARCHITECTURE.md",
        }
        self.assertTrue(required.issubset(files))
        api = files["api/app/main.py"]
        self.assertIn("class OCRProvider", api)
        self.assertIn("class ExtractionProvider", api)
        self.assertIn("REVIEW_REQUIRED", api)
        self.assertNotIn("ABBYY", api)
        self.assertNotIn("SAP", api)

    def test_generate_template_writes_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            studio_cli.generate_template("Document Flow", "document-flow", "document-ai", root, False)
            self.assertTrue((root / "api/app/main.py").exists())
            self.assertTrue((root / "web/src/main.tsx").exists())
            self.assertTrue((root / "docker-compose.yml").exists())

    def test_parser_exposes_all_commands(self) -> None:
        parser = studio_cli.parser()
        for command in ("new", "enroll", "validate", "dashboard"):
            args = parser.parse_args(["--dry-run", command] + ({
                "new": ["--name", "Document Flow", "--no-remote", "--skip-factory-bootstrap"],
                "enroll": ["--target", "/tmp/example", "--repo", "owner/example", "--name", "Example", "--skip-factory-bootstrap"],
                "validate": [],
                "dashboard": [],
            }[command]))
            self.assertEqual(args.command, command)
            self.assertTrue(args.dry_run)


if __name__ == "__main__":
    unittest.main()
