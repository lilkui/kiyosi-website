#!/usr/bin/env python3
"""Generate VitePress API pages from kiyosi Doxygen XML and Python docstrings."""

import argparse
import enum
import importlib
import inspect
import re
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

PYTHON_MODULES = ("kiyosi", "kiyosi.instruments", "kiyosi.market", "kiyosi.pricing")
PROTOCOL_METHODS = {"__contains__", "__getitem__", "__iter__", "__len__"}
GENERATED_MARKER = ".kiyosi-api-generated"


def text_of(node: ET.Element | None) -> str:
    return "" if node is None else "".join(node.itertext()).strip()


def clean_space(value: str) -> str:
    return re.sub(r"[ \t\r\f\v]+", " ", value).strip()


def markdown_inline(node: ET.Element) -> str:
    pieces = [node.text or ""]
    for child in node:
        content = markdown_node(child, inline=True)
        pieces.append(content)
        pieces.append(child.tail or "")
    return clean_space("".join(pieces))


def markdown_node(node: ET.Element, *, inline: bool = False) -> str:
    tag = node.tag
    if tag in {"computeroutput", "ref"}:
        return f"`{text_of(node)}`"
    if tag == "bold":
        return f"**{markdown_inline(node)}**"
    if tag == "emphasis":
        return f"*{markdown_inline(node)}*"
    if tag == "ulink":
        return f"[{markdown_inline(node)}]({node.get('url', '')})"
    if tag == "linebreak":
        return "  \n"
    if tag == "sp":
        return " "
    if tag == "formula":
        return f"`{text_of(node)}`"
    if tag == "programlisting":
        lines = [
            clean_space("".join(line.itertext())) for line in node.findall("codeline")
        ]
        return f"\n```cpp\n{'\n'.join(lines)}\n```\n"
    if tag in {"itemizedlist", "orderedlist"}:
        marker = "-" if tag == "itemizedlist" else "1."
        items = [
            f"{marker} {markdown_inline(item)}" for item in node.findall("listitem")
        ]
        return "\n" + "\n".join(items) + "\n"
    if tag == "parameterlist":
        labels = {
            "param": "Parameters",
            "retval": "Return values",
            "exception": "Exceptions",
            "templateparam": "Template parameters",
        }
        rows = []
        for item in node.findall("parameteritem"):
            names = [text_of(name) for name in item.findall("parameternamelist/parametername")]
            description = render_description(item.find("parameterdescription"))
            rows.append(f"- `{', '.join(names)}` — {description}")
        label = labels.get(node.get("kind", ""), "Parameters")
        return f"\n**{label}**\n\n" + "\n".join(rows) + "\n"
    if tag == "simplesect":
        labels = {
            "return": "Returns",
            "note": "Note",
            "warning": "Warning",
            "see": "See also",
            "pre": "Precondition",
            "post": "Postcondition",
            "remark": "Remarks",
        }
        label = labels.get(node.get("kind", ""), node.get("kind", "").title())
        return f"\n**{label}:** {markdown_inline(node)}\n"
    if tag == "xrefsect":
        title = text_of(node.find("xreftitle")) or "Note"
        description = render_description(node.find("xrefdescription"))
        return f"\n**{title}:** {description}\n"
    if tag == "para":
        return markdown_inline(node) + ("" if inline else "\n\n")
    return markdown_inline(node)


def render_description(node: ET.Element | None) -> str:
    if node is None:
        return ""
    rendered = "".join(markdown_node(child) for child in node)
    if node.text and node.text.strip():
        rendered = node.text.strip() + rendered
    return re.sub(r"\n{3,}", "\n\n", rendered).strip()


def template_prefix(node: ET.Element) -> str:
    params = node.find("templateparamlist")
    if params is None:
        return ""
    values = []
    for param in params.findall("param"):
        value = " ".join(
            filter(None, (text_of(param.find("type")), text_of(param.find("declname"))))
        )
        default = text_of(param.find("defval"))
        values.append(f"{value} = {default}" if default else value)
    return f"template <{', '.join(values)}>\n"


def member_signature(member: ET.Element) -> str:
    kind = member.get("kind", "member")
    definition = text_of(member.find("definition"))
    args = text_of(member.find("argsstring"))
    if kind == "enum":
        scoped = " class" if member.get("strong") == "yes" else ""
        return f"enum{scoped} {text_of(member.find('name'))}"
    signature = (definition or text_of(member.find("name"))) + args
    return template_prefix(member) + re.sub(
        r"<\s+|\s+>", lambda match: match.group().strip(), signature
    )


def member_markdown(member: ET.Element, level: int = 4) -> str:
    name = text_of(member.find("name"))
    parts = [
        f"{'#' * level} `{name}`",
        "",
        "```cpp",
        member_signature(member),
        "```",
        "",
    ]
    description = "\n\n".join(
        value
        for value in (
            render_description(member.find("briefdescription")),
            render_description(member.find("detaileddescription")),
        )
        if value
    )
    if description:
        parts.extend((description, ""))
    enum_values = member.findall("enumvalue")
    if enum_values:
        parts.extend(("**Values**", ""))
        for value in enum_values:
            value_name = text_of(value.find("name"))
            initializer = text_of(value.find("initializer"))
            value_description = " ".join(
                filter(
                    None,
                    (
                        render_description(value.find("briefdescription")),
                        render_description(value.find("detaileddescription")),
                    ),
                )
            )
            label = f"`{value_name}{initializer}`"
            parts.append(
                f"- {label}" + (f" — {value_description}" if value_description else "")
            )
        parts.append("")
    return "\n".join(parts)


def public_members(compound: ET.Element) -> list[ET.Element]:
    members = []
    for section in compound.findall("sectiondef"):
        if section.get("kind", "").startswith("public"):
            members.extend(section.findall("memberdef"))
    return [member for member in members if member.get("prot", "public") == "public"]


def compound_markdown(compound: ET.Element) -> str:
    name = text_of(compound.find("compoundname"))
    kind = compound.get("kind", "type")
    signature = f"{kind} {name}"
    bases = [
        text_of(base) for base in compound.findall("basecompoundref") if text_of(base)
    ]
    if bases:
        signature += " : " + ", ".join(bases)
    parts = [
        f"## `{name}`",
        "",
        "```cpp",
        template_prefix(compound) + signature,
        "```",
        "",
    ]
    description = "\n\n".join(
        value
        for value in (
            render_description(compound.find("briefdescription")),
            render_description(compound.find("detaileddescription")),
        )
        if value
    )
    if description:
        parts.extend((description, ""))
    members = public_members(compound)
    if members:
        parts.extend(("### Members", ""))
        for member in members:
            parts.append(member_markdown(member))
    return "\n".join(parts).rstrip() + "\n"


def source_path(node: ET.Element) -> str | None:
    location = node.find("location")
    if location is None:
        return None
    file_name = (location.get("file") or "").replace("\\", "/")
    if "include/" in file_name:
        return file_name[file_name.index("include/") :]
    generated_marker = "/generated/kiyosi/"
    if generated_marker in file_name:
        return "include/kiyosi/" + file_name.split(generated_marker, 1)[1]
    return None


def slug_for_header(header: str) -> str:
    return (
        header.removeprefix("include/kiyosi/")
        .removesuffix(".hpp")
        .replace("/", "-")
        .replace("_", "-")
    )


def generate_cpp(xml_dir: Path, output: Path) -> int:
    index = ET.parse(xml_dir / "index.xml").getroot()
    headers: dict[str, dict[str, list[ET.Element]]] = defaultdict(
        lambda: {"files": [], "compounds": [], "members": []}
    )
    for entry in index.findall("compound"):
        if entry.get("kind") != "file":
            continue
        compound_file = xml_dir / f"{entry.get('refid')}.xml"
        if not compound_file.exists():
            continue
        compound = ET.parse(compound_file).getroot().find("compounddef")
        if compound is not None and (header := source_path(compound)):
            headers[header]["files"].append(compound)

    for entry in index.findall("compound"):
        kind = entry.get("kind")
        if kind not in {"class", "struct", "concept", "namespace"}:
            continue
        compound_file = xml_dir / f"{entry.get('refid')}.xml"
        if not compound_file.exists():
            continue
        compound = ET.parse(compound_file).getroot().find("compounddef")
        if compound is None:
            continue
        name = text_of(compound.find("compoundname"))
        if not name.startswith("kiyosi") or "::detail" in name:
            continue
        if kind == "namespace":
            for member in compound.findall("sectiondef/memberdef"):
                header = source_path(member)
                if header and member.get("prot", "public") == "public":
                    headers[header]["members"].append(member)
            continue
        if compound.get("prot", "public") != "public":
            continue
        header = source_path(compound)
        if not header:
            continue
        headers[header]["compounds"].append(compound)

    cpp_dir = output / "cpp"
    cpp_dir.mkdir(parents=True, exist_ok=True)
    index_lines = [
        "---",
        "description: Complete C++ API generated from kiyosi Doxygen XML.",
        "---",
        "",
        "# C++ API reference",
        "",
        "This reference is generated from the public headers and Doxygen XML. Declarations without comments are included so the surface remains complete.",
        "",
    ]
    for header in sorted(headers):
        slug = slug_for_header(header)
        title = header.removeprefix("include/")
        index_lines.append(f"- [`<{title}>`](./{slug})")
        page = [
            "---",
            f"description: C++ API declarations from {title}.",
            "outline: [2, 4]",
            "---",
            "",
            f"# `<{title}>`",
            "",
            f"```cpp\n#include <{title}>\n```",
            "",
        ]
        for file_compound in headers[header]["files"]:
            file_description = "\n\n".join(
                filter(
                    None,
                    (
                        render_description(file_compound.find("briefdescription")),
                        render_description(file_compound.find("detaileddescription")),
                    ),
                )
            )
            if file_description:
                page.extend((file_description, ""))
        for member in headers[header]["members"]:
            page.append(member_markdown(member, level=2))
        for compound in headers[header]["compounds"]:
            page.append(compound_markdown(compound))
        (cpp_dir / f"{slug}.md").write_text(
            "\n".join(page).rstrip() + "\n", encoding="utf-8"
        )
    (cpp_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return len(headers)


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
    return re.sub(r":(?:class|func|meth|attr):`([^`]+)`", r"`\1`", rendered)


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
    init = vars(cls).get("__init__")
    if init is not None:
        signatures, init_body = callable_signature(init, "__init__")
        signatures = [value.replace("__init__", name, 1) for value in signatures]
        if signatures:
            parts.extend(("```python", "\n".join(signatures), "```", ""))
    else:
        init_body = ""
    if init_body.startswith("Initialize self.  See help(type(self))"):
        init_body = ""
    class_doc = inspect.getdoc(cls) or ""
    if class_doc:
        parts.extend((python_doc_markdown(class_doc), ""))
    if init_body and init_body not in class_doc:
        parts.extend(("### Constructor", "", python_doc_markdown(init_body), ""))

    if issubclass(cls, enum.Enum):
        parts.extend(("### Values", ""))
        for member_name, member in cls.__members__.items():
            parts.append(f"- `{member_name}` = `{member.value!r}`")
        return "\n".join(parts).rstrip() + "\n"

    rendered_members = []
    for member_name, member in vars(cls).items():
        if member_name.startswith("_") and member_name not in PROTOCOL_METHODS:
            continue
        if not (
            callable(member)
            or isinstance(member, property)
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
        "description: Complete Python API generated from kiyosi runtime docstrings.",
        "---",
        "",
        "# Python API reference",
        "",
        "The pages below are generated from each public module's `__all__`, runtime signatures, and docstrings, including native nanobind objects.",
        "",
    ]
    for module_name in PYTHON_MODULES:
        module = importlib.import_module(module_name)
        names = list(module.__all__)
        missing = [name for name in names if not hasattr(module, name)]
        if missing:
            raise RuntimeError(
                f"{module_name} exports missing names: {', '.join(missing)}"
            )
        slug = module_slug(module_name)
        index_lines.append(f"- [`{module_name}`](./{slug})")
        page = [
            "---",
            f"description: Python API reference for {module_name}.",
            "outline: [2, 4]",
            "---",
            "",
            f"# `{module_name}`",
            "",
        ]
        module_doc = inspect.getdoc(module)
        if module_doc:
            page.extend((module_doc, ""))
        for name in names:
            obj = getattr(module, name)
            if inspect.isclass(obj):
                page.append(class_markdown(name, obj))
            elif callable(obj):
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


def write_overview(output: Path) -> None:
    (output / "index.md").write_text(
        """---
description: Complete generated C++ and Python API reference for kiyosi.
---

# API reference

This reference is generated from the library's public C++ headers and installed Python API.

- [C++ API](./cpp/) — declarations and Doxygen comments from every public header.
- [Python API](./python/) — public exports, signatures, members, and docstrings.

::: warning Alpha API
Kiyosi currently makes no backward-compatibility guarantees. Regenerate these pages after updating the library.
:::
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--doxygen-xml",
        type=Path,
        required=True,
        help="Directory containing Doxygen index.xml",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/api"),
        help="Generated VitePress directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.doxygen_xml / "index.xml").is_file():
        raise SystemExit(f"Doxygen index not found: {args.doxygen_xml / 'index.xml'}")
    if (
        args.output.exists()
        and any(args.output.iterdir())
        and not (args.output / GENERATED_MARKER).is_file()
    ):
        raise SystemExit(f"Refusing to replace unmarked directory: {args.output}")
    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)
    (args.output / GENERATED_MARKER).write_text(
        "Generated by tools/generate_api_docs.py.\n", encoding="utf-8"
    )
    cpp_headers = generate_cpp(args.doxygen_xml, args.output)
    python_modules = generate_python(args.output)
    write_overview(args.output)
    print(
        f"Generated {cpp_headers} C++ header pages and {python_modules} Python module pages "
        f"in {args.output}"
    )


if __name__ == "__main__":
    main()
