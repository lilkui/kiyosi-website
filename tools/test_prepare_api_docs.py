import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import prepare_api_docs


class PreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.cache = self.root / ".cache"
        self.source = self.cache / "kiyosi"
        self.source.mkdir(parents=True)
        self.manifest = self.source / "Cargo.toml"
        self.manifest.write_text('[workspace.package]\nversion = "0.14.0"\n', encoding="utf-8")
        self.git("init", "-q")
        self.git("add", "Cargo.toml")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "Fixture")
        self.revision = self.git("rev-parse", "HEAD").strip()
        self.write_pin("0.14.0")
        replacement = patch.multiple(prepare_api_docs, ROOT=self.root, CACHE=self.cache)
        replacement.start()
        self.addCleanup(replacement.stop)

    def git(self, *arguments):
        return subprocess.check_output(["git", *arguments], cwd=self.source, text=True)

    def write_pin(self, version):
        (self.root / "upstream.json").write_text(json.dumps({
            "repository": "unused", "revision": self.revision, "version": version,
        }), encoding="utf-8")

    def test_rejects_dirty_source_without_overwriting_changes(self):
        self.manifest.write_text("local work", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Upstream cache has local changes"):
            prepare_api_docs.main()
        self.assertEqual(self.manifest.read_text(encoding="utf-8"), "local work")
        self.assertFalse((self.cache / "venv").exists())

    def test_rejects_mismatched_pin_before_building(self):
        self.write_pin("0.13.0")
        with self.assertRaisesRegex(RuntimeError, "version does not match"):
            prepare_api_docs.main()
        self.assertFalse((self.cache / "venv").exists())
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.revision)


if __name__ == "__main__":
    unittest.main()
