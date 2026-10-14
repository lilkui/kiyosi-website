import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Literal
from unittest.mock import patch

from generate_api_docs import (
    generate_cpp,
    generate_python,
    member_markdown,
    python_doc_markdown,
    render_description,
    source_path,
    split_signature,
)


class GeneratorTests(unittest.TestCase):
    def test_cpp_member_signature_and_parameter_names(self):
        member = ET.fromstring(
            """<memberdef kind="function">
              <definition>KIYOSI_EXPORT Result&lt; double &gt; kiyosi::year_fraction</definition>
              <argsstring>(Date start, Date end)</argsstring>
              <name>year_fraction</name>
              <detaileddescription><para><parameterlist kind="param">
                <parameteritem><parameternamelist><parametername>start</parametername></parameternamelist>
                  <parameterdescription><para>Inclusive start date.</para></parameterdescription></parameteritem>
                <parameteritem><parameternamelist><parametername>end</parametername></parameternamelist>
                  <parameterdescription><para>End date.</para></parameterdescription></parameteritem>
              </parameterlist></para></detaileddescription>
            </memberdef>"""
        )

        rendered = member_markdown(member)

        self.assertIn("Result<double> kiyosi::year_fraction(Date start, Date end)", rendered)
        self.assertIn("- `start` — Inclusive start date.", rendered)
        self.assertIn("- `end` — End date.", rendered)
        self.assertNotIn("- ``", rendered)

    def test_splits_native_signature_from_docstring(self):
        signatures, body = split_signature(
            "price(self, value: float) -> float\n\nReturn the price.", "price"
        )

        self.assertEqual(signatures, ["price(self, value: float) -> float"])
        self.assertEqual(body, "Return the price.")

    def test_converts_numpy_fields_to_markdown(self):
        rendered = python_doc_markdown(
            """Price an option.

            Parameters
            ----------
            spot : float
                Positive spot price.
            """
        )

        self.assertIn("#### Parameters", rendered)
        self.assertIn("- **`spot`** (`float`) — Positive spot price.", rendered)

    def test_maps_generated_version_header_to_public_include(self):
        node = ET.fromstring(
            '<compounddef><location file="out/build/release/generated/kiyosi/core/version.hpp"/></compounddef>'
        )

        self.assertEqual(source_path(node), "include/kiyosi/core/version.hpp")

    def test_excludes_internal_detail_headers(self):
        node = ET.fromstring(
            '<compounddef><location file="include/kiyosi/pricing/detail/autocallable_traits.hpp"/></compounddef>'
        )

        self.assertIsNone(source_path(node))

    def test_generates_cpp_from_include_relative_doxygen_locations(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.xml").write_text(
                '<doxygenindex><compound kind="file" refid="vanilla"/></doxygenindex>',
                encoding="utf-8",
            )
            (root / "vanilla.xml").write_text(
                '<doxygen><compounddef kind="file"><location file="kiyosi/instruments/vanilla.hpp"/>'
                '<briefdescription><para>Vanilla options.</para></briefdescription>'
                '</compounddef></doxygen>', encoding="utf-8",
            )
            output = root / "output"
            self.assertEqual(generate_cpp(root, output), 1)
            rendered = (output / "cpp/instruments-vanilla.md").read_text(encoding="utf-8")
            self.assertIn("#include <kiyosi/instruments/vanilla.hpp>", rendered)
            self.assertIn("Vanilla options.", rendered)

    def test_rejects_xml_without_public_headers(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.xml").write_text("<doxygenindex/>", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "No public kiyosi headers"):
                generate_cpp(root, root / "output")

    def test_generates_public_names_and_literal_choices_without_all(self):
        module = ModuleType("kiyosi.instruments")
        module.OptionType = Literal["call", "put"]
        module._private = "hidden"
        with TemporaryDirectory() as directory:
            with patch("generate_api_docs.PYTHON_MODULES", (module.__name__,)), patch(
                "generate_api_docs.importlib.import_module", return_value=module
            ):
                self.assertEqual(generate_python(Path(directory)), 1)
            rendered = (Path(directory) / "python/kiyosi-instruments.md").read_text(encoding="utf-8")

        self.assertIn("OptionType = typing.Literal['call', 'put']", rendered)
        self.assertNotIn("_private", rendered)
        self.assertNotIn("Special typing form", rendered)

    def test_honors_all_and_rejects_missing_exports(self):
        module = ModuleType("kiyosi")
        module.__all__ = ["__version__"]
        module.__version__ = "0.10.0"
        module.other = "not exported"
        with TemporaryDirectory() as directory, patch(
            "generate_api_docs.PYTHON_MODULES", (module.__name__,)
        ), patch("generate_api_docs.importlib.import_module", return_value=module):
            generate_python(Path(directory))
            rendered = (Path(directory) / "python/kiyosi.md").read_text(encoding="utf-8")
            self.assertIn("__version__ = '0.10.0'", rendered)
            self.assertNotIn("not exported", rendered)
            module.__all__.append("missing")
            with self.assertRaisesRegex(RuntimeError, "kiyosi exports missing names: missing"):
                generate_python(Path(directory))

    def test_converts_module_references(self):
        self.assertEqual(python_doc_markdown("See :mod:`kiyosi`."), "See `kiyosi`.")

    def test_removes_xml_whitespace_before_block_sections(self):
        description = ET.fromstring(
            '<detaileddescription><para>Text. <simplesect kind="return">'
            '<para>Value.</para></simplesect></para></detaileddescription>'
        )

        self.assertEqual(render_description(description), "Text.\n**返回值:** Value.")


if __name__ == "__main__":
    unittest.main()
