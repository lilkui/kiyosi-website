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

    def test_publishes_complete_rustdoc_and_return_redirect(self):
        destination = self.root / "docs/public/api/rust"
        destination.mkdir(parents=True)
        (destination / "old.html").write_text("previous docs", encoding="utf-8")
        files = {
            "kiyosi_core/index.html": "<h1>Rust API</h1>",
            "static.files/main.js": "// rustdoc asset\n",
            "src/kiyosi_core/lib.rs.html": "<pre>pub struct Example;</pre>",
        }

        def fake_run(*command, **kwargs):
            if command[:2] == ("cargo", "doc"):
                for name, content in files.items():
                    file = self.cache / "target/doc" / name
                    file.parent.mkdir(parents=True, exist_ok=True)
                    file.write_text(content, encoding="utf-8")

        with patch("prepare_api_docs.venv.EnvBuilder"), patch(
            "prepare_api_docs.run", side_effect=fake_run
        ) as commands:
            prepare_api_docs.main()

        commands.assert_any_call(
            self.cache / "venv" / (
                "Scripts/python.exe" if prepare_api_docs.os.name == "nt" else "bin/python"
            ),
            self.root / "tools/generate_api_docs.py", "--version", "0.14.0",
            "--revision", self.revision, "--output", self.root / "docs/api",
        )
        self.assertEqual(
            {file.relative_to(destination).as_posix() for file in destination.rglob("*") if file.is_file()},
            {*files, "index.html"},
        )
        for name, content in files.items():
            self.assertEqual((destination / name).read_text(encoding="utf-8"), content)
        redirect = (destination / "index.html").read_text(encoding="utf-8")
        self.assertIn(
            'location.replace("kiyosi_core/index.html" + location.search + location.hash)',
            redirect,
        )
        self.assertIn('content="0;url=kiyosi_core/index.html"', redirect)


if __name__ == "__main__":
    unittest.main()
