#!/usr/bin/env python3
"""Generate VitePress API pages from the pinned kiyosi Python package."""

import argparse
import enum
import importlib
import inspect
import re
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import get_origin

PYTHON_MODULES = ("kiyosi", "kiyosi.instruments", "kiyosi.market", "kiyosi.pricing")
PROTOCOL_METHODS = {"__contains__", "__getitem__", "__iter__", "__len__"}
GENERATED_MARKER = ".kiyosi-api-generated"


def split_signature(doc: str, name: str) -> tuple[list[str], str]:
    lines = inspect.cleandoc(doc).splitlines()
    signatures = []
    while (
        lines
        and "(" in lines[0]
        and (name in lines[0] or lines[0].lstrip().startswith("__init__("))
    ):
        signatures.append(lines.pop(0).strip())
    while lines and not lines[0].strip():
        lines.pop(0)
    return signatures, "\n".join(lines)


def python_doc_markdown(doc: str, heading_level: int = 4) -> str:
    lines = inspect.cleandoc(doc).splitlines()
    output = []
    field_sections = {
        "Parameters",
        "Attributes",
        "Returns",
        "Yields",
        "Raises",
        "Warns",
    }
    section = ""
    index = 0
    while index < len(lines):
        line = lines[index].rstrip()
        if line.startswith(">>> "):
            output.extend(("```python", line))
            index += 1
            while index < len(lines) and lines[index].strip():
                output.append(lines[index])
                index += 1
            output.extend(("```", ""))
            continue
        if (
            index + 1 < len(lines)
            and lines[index + 1].strip()
            and set(lines[index + 1].strip()) == {"-"}
        ):
            output.extend((f"{'#' * heading_level} {line.strip()}", ""))
            section = line.strip()
            index += 2
            continue
        if section in field_sections and line and not line.startswith((" ", "\t")):
            descriptions = []
            next_index = index + 1
            while next_index < len(lines) and (
                not lines[next_index].strip()
                or lines[next_index].startswith((" ", "\t"))
            ):
                if lines[next_index].strip():
                    descriptions.append(lines[next_index].strip())
                next_index += 1
            if descriptions:
                if section in {"Parameters", "Attributes"} and " : " in line:
                    field_name, field_type = line.split(" : ", 1)
                    label = f"**`{field_name}`** (`{field_type}`)"
                else:
                    label = f"`{line.strip()}`"
                output.append(f"- {label} — {' '.join(descriptions)}")
                index = next_index
                continue
        if line.startswith("    "):
            output.append(line.strip())
        else:
            output.append(line)
        index += 1
    rendered = "\n".join(output).strip()
    return re.sub(r":(?:class|func|meth|attr|mod):`([^`]+)`", r"`\1`", rendered)


def display_signature(signature: str) -> str:
    return signature.replace("kiyosi._native.", "").replace("kiyosi.", "")


def callable_signature(obj: object, name: str) -> tuple[list[str], str]:
    doc = inspect.getdoc(obj) or ""
    signatures, body = split_signature(doc, name)
    try:
        inspected = str(inspect.signature(obj))
    except (TypeError, ValueError):
        inspected = ""
    if inspected and inspected not in {
        "(*args, **kwargs)",
        "(self, /, *args, **kwargs)",
    }:
        signatures = [f"{name}{inspected}"]
    return [display_signature(value) for value in signatures], body


def class_markdown(name: str, cls: type) -> str:
    parts = [f"## `{name}`", ""]
    signatures = []
    # Factory-only native types can inherit object's misleading () signature.
    if (
        cls.__new__ is not object.__new__
        or cls.__init__ is not object.__init__
        or hasattr(cls, "__signature__")
    ):
        signatures, _ = callable_signature(cls, name)
    init = vars(cls).get("__init__")
    init_body = ""
    if init is not None:
        init_signatures, init_body = callable_signature(init, "__init__")
        if not signatures:
            signatures = [value.replace("__init__", name, 1) for value in init_signatures]
    if signatures:
        parts.extend(("```python", "\n".join(signatures), "```", ""))
    if init_body.startswith("Initialize self.  See help(type(self))"):
        init_body = ""
    class_doc = inspect.getdoc(cls) or ""
    if class_doc:
        parts.extend((python_doc_markdown(class_doc), ""))
    if init_body and init_body not in class_doc:
        parts.extend(("### 构造函数", "", python_doc_markdown(init_body), ""))

    if issubclass(cls, enum.Enum):
        parts.extend(("### 枚举值", ""))
        for member_name, member in cls.__members__.items():
            parts.append(f"- `{member_name}` = `{member.value!r}`")
        return "\n".join(parts).rstrip() + "\n"

    rendered_members = []
    for member_name, member in sorted(vars(cls).items()):
        if member_name.startswith("_") and member_name not in PROTOCOL_METHODS:
            continue
        if isinstance(member, (staticmethod, classmethod)):
            member = getattr(cls, member_name)
        if not (
            callable(member)
            or isinstance(member, property)
            or inspect.isdatadescriptor(member)
            or inspect.ismethoddescriptor(member)
        ):
            continue
        member_doc = inspect.getdoc(member) or ""
        signatures, body = (
            callable_signature(member, member_name)
            if callable(member)
            else ([], member_doc)
        )
        rendered_members.extend((f"### `{member_name}`", ""))
        if signatures:
            rendered_members.extend(("```python", "\n".join(signatures), "```", ""))
        if body:
            rendered_members.extend((python_doc_markdown(body), ""))
    if rendered_members:
        parts.extend(rendered_members)
    return "\n".join(parts).rstrip() + "\n"


def module_slug(module_name: str) -> str:
    return module_name.replace(".", "-")


def generate_python(output: Path) -> int:
    python_dir = output / "python"
    python_dir.mkdir(parents=True, exist_ok=True)
    index_lines = [
        "---",
        "description: 根据 kiyosi 运行时文档字符串自动生成的完整 Python API 参考文档。",
        "---",
        "",
        "# Python API 参考",
        "",
        "以下页面根据各公开模块的导出对象、运行时签名和文档字符串自动生成，也包含 PyO3 原生绑定对象。导出对象以 `__all__` 为准；未声明 `__all__` 时，使用模块中的公开名称。",
        "",
    ]
    for module_name in PYTHON_MODULES:
        module = importlib.import_module(module_name)
        names = (
            list(module.__all__)
            if hasattr(module, "__all__")
            else [name for name in vars(module) if not name.startswith("_")]
        )
        missing = [name for name in names if not hasattr(module, name)]
        if missing:
            raise RuntimeError(
                f"{module_name} exports missing names: {', '.join(missing)}"
            )
        slug = module_slug(module_name)
        index_lines.append(f"- [`{module_name}`](./{slug})")
        page = [
            "---",
            f"description: {module_name} 的 Python API 参考文档。",
            "outline: [2, 4]",
            "---",
            "",
            f"# `{module_name}`",
            "",
        ]
        module_doc = inspect.getdoc(module)
        if module_doc:
            page.extend((python_doc_markdown(module_doc, heading_level=2), ""))
        for name in names:
            obj = getattr(module, name)
            if inspect.isclass(obj):
                page.append(class_markdown(name, obj))
            elif callable(obj) and get_origin(obj) is None:
                signatures, body = callable_signature(obj, name)
                page.extend((f"## `{name}`", ""))
                if signatures:
                    page.extend(("```python", "\n".join(signatures), "```", ""))
                if body:
                    page.extend((python_doc_markdown(body), ""))
            else:
                page.extend(
                    (f"## `{name}`", "", f"```python\n{name} = {obj!r}\n```", "")
                )
        (python_dir / f"{slug}.md").write_text(
            "\n".join(page).rstrip() + "\n", encoding="utf-8"
        )
    (python_dir / "index.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )
    return len(PYTHON_MODULES)


def write_overview(output: Path, version: str, revision: str) -> None:
    (output / "index.md").write_text(
        f"""---
description: kiyosi Python API 与 Rust API 参考文档。
---

# API 参考

本参考文档根据同一上游提交的 Python 公开接口与 Rust 文档注释生成。

kiyosi 版本：**{version}**；[源码提交 `{revision[:7]}`](https://github.com/lilkui/kiyosi/tree/{revision})。

- [Python API](./python/)：公开导出对象、签名、成员和文档字符串。
- <a href="./rust/kiyosi_core/index.html" target="_self">Rust API</a>：原生 rustdoc，提供类型、trait、实现、源码链接和独立搜索。

Rust API 使用 rustdoc 的界面与搜索；网站的本地搜索涵盖中文指南和 Python API。

::: warning 早期开发阶段
Kiyosi 当前不保证 API 向后兼容。更新库后，请重新生成这些参考页面。
:::
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        required=True,
        help="Expected installed kiyosi version",
    )
    parser.add_argument("--revision", required=True, help="Pinned upstream commit")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/api"),
        help="Generated VitePress directory",
    )
    return parser.parse_args()


def generate(output: Path, version: str, revision: str) -> None:
    actual = importlib.import_module("kiyosi").__version__
    if actual != version:
        raise RuntimeError(f"kiyosi version mismatch: expected {version}, got {actual}")
    if (
        output.exists()
        and any(output.iterdir())
        and not (output / GENERATED_MARKER).is_file()
    ):
        raise RuntimeError(f"Refusing to replace unmarked directory: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Build first so import or rendering failures preserve the previous reference.
    with TemporaryDirectory(dir=output.parent) as temporary:
        staged = Path(temporary) / "api"
        staged.mkdir()
        python_modules = generate_python(staged)
        write_overview(staged, version, revision)
        (staged / GENERATED_MARKER).write_text(
            f"Generated by tools/generate_api_docs.py from {revision}.\n", encoding="utf-8"
        )
        if output.exists():
            shutil.rmtree(output)
        staged.rename(output)
    print(f"Generated {python_modules} Python module pages in {output}")


if __name__ == "__main__":
    args = parse_args()
    generate(args.output, args.version, args.revision)
