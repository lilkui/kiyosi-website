#!/usr/bin/env python3
"""Build Python references and rustdoc from the exact upstream commit."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib
import venv

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"


def run(*command, cwd=ROOT, env=None):
    print("+", " ".join(map(str, command)), flush=True)
    subprocess.run(list(map(str, command)), cwd=cwd, env=env, check=True)


def main():
    pin = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
    source = CACHE / "kiyosi"
    source.mkdir(parents=True, exist_ok=True)
    if not (source / ".git").exists():
        run("git", "init", source)
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=source, text=True
    ).strip()
    if dirty:
        raise RuntimeError(f"Upstream cache has local changes; refusing to replace: {source}")
    available = subprocess.run(
        ["git", "cat-file", "-e", f"{pin['revision']}^{{commit}}"],
        cwd=source, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if available.returncode:
        run("git", "fetch", "--depth=1", pin["repository"], pin["revision"], cwd=source)
    run("git", "checkout", "--detach", pin["revision"], cwd=source)
    manifest = tomllib.loads((source / "Cargo.toml").read_text(encoding="utf-8"))
    if manifest["workspace"]["package"]["version"] != pin["version"]:
        raise RuntimeError("upstream.json version does not match the pinned Cargo.toml")

    environment = CACHE / "venv"
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(environment)
    build_env = {**os.environ, "CARGO_TARGET_DIR": str(CACHE / "target")}
    run(python, "-m", "pip", "install", "--no-deps", "--force-reinstall", source, env=build_env)
    rustdoc = CACHE / "target/doc"
    if rustdoc.exists():
        shutil.rmtree(rustdoc)
    run("cargo", "doc", "-p", "kiyosi-core", "--no-deps", "--locked", cwd=source,
        env={**build_env, "RUSTDOCFLAGS": "-D warnings"})
    if not (rustdoc / "kiyosi_core/index.html").is_file():
        raise RuntimeError("Cargo did not produce the Rust API entry page")
    run(python, ROOT / "tools/generate_api_docs.py", "--version", pin["version"],
        "--revision", pin["revision"], "--output", ROOT / "docs/api")
    destination = ROOT / "docs/public/api/rust"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(rustdoc, destination)
    # rustdoc help/settings link back to a root index that Cargo does not emit.
    (destination / "index.html").write_text('''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>kiyosi Rust API</title>
<link rel="canonical" href="kiyosi_core/index.html">
<script>location.replace("kiyosi_core/index.html" + location.search + location.hash)</script>
<noscript><meta http-equiv="refresh" content="0;url=kiyosi_core/index.html"></noscript>
</head><body><a href="kiyosi_core/index.html">Rust API</a></body></html>
''', encoding="utf-8")


if __name__ == "__main__":
    main()
