import inspect
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import FrameType, ModuleType
from typing import Literal
from unittest.mock import patch

from generate_api_docs import (
    GENERATED_MARKER,
    class_markdown,
    generate,
    generate_python,
    python_doc_markdown,
    split_signature,
)


class GeneratorTests(unittest.TestCase):
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
        module.__version__ = "0.14.0"
        module.other = "not exported"
        with TemporaryDirectory() as directory, patch(
            "generate_api_docs.PYTHON_MODULES", (module.__name__,)
        ), patch("generate_api_docs.importlib.import_module", return_value=module):
            generate_python(Path(directory))
            rendered = (Path(directory) / "python/kiyosi.md").read_text(encoding="utf-8")
            self.assertIn("__version__ = '0.14.0'", rendered)
            self.assertNotIn("not exported", rendered)
            module.__all__.append("missing")
            with self.assertRaisesRegex(RuntimeError, "kiyosi exports missing names: missing"):
                generate_python(Path(directory))

    def test_converts_module_references(self):
        self.assertEqual(python_doc_markdown("See :mod:`kiyosi`."), "See `kiyosi`.")

    def test_preserves_doctest_examples_as_code(self):
        rendered = python_doc_markdown("Example.\n\n>>> price < 10\nTrue\n\nNext paragraph.")
        self.assertIn("```python\n>>> price < 10\nTrue\n```", rendered)
        self.assertIn("Next paragraph.", rendered)

    def test_renders_native_constructor_without_own_init(self):
        class Native:
            __signature__ = inspect.Signature([
                inspect.Parameter("strike", inspect.Parameter.KEYWORD_ONLY)
            ])

        rendered = class_markdown("EuropeanOption", Native)
        self.assertIn("EuropeanOption(*, strike)", rendered)
        self.assertNotIn("__init__", rendered)

    def test_omits_constructor_for_factory_only_native_type(self):
        rendered = class_markdown("Frame", FrameType)

        self.assertNotIn("Frame()", rendered)
        self.assertIn("## `Frame`", rendered)
        self.assertIn("### `f_code`", rendered)

    def test_preserves_explicit_parameterless_constructor(self):
        class Native:
            def __new__(cls):
                return super().__new__(cls)

        rendered = class_markdown("Engine", Native)
        self.assertIn("Engine()", rendered)

    def test_member_output_is_independent_of_declaration_order(self):
        members = {
            "zeta": property(doc="Last property."),
            "alpha": property(doc="First property."),
        }
        first = type("Native", (), members)
        second = type("Native", (), dict(reversed(members.items())))

        rendered = class_markdown("Native", first)
        self.assertEqual(rendered, class_markdown("Native", second))
        self.assertLess(rendered.index("### `alpha`"), rendered.index("### `zeta`"))
        self.assertIn("First property.", rendered)
        self.assertIn("Last property.", rendered)

    def test_renders_native_data_descriptors(self):
        class Native:
            __slots__ = {"strike": "The contract strike."}

        rendered = class_markdown("EuropeanOption", Native)
        self.assertIn("### `strike`", rendered)
        self.assertIn("The contract strike.", rendered)

    def test_renders_wrapped_methods_from_the_underlying_callable(self):
        class Native:
            @staticmethod
            def flat(rate):
                """Create a flat curve."""

            @classmethod
            def from_rate(cls, rate):
                """Create a curve from a rate."""

        vars(Native)["flat"].__doc__ = "Convert a function to be a static method."
        rendered = class_markdown("Curve", Native)
        self.assertIn("flat(rate)", rendered)
        self.assertIn("Create a flat curve.", rendered)
        self.assertIn("from_rate(rate)", rendered)
        self.assertIn("Create a curve from a rate.", rendered)
        self.assertNotIn("Convert a function", rendered)

    def test_version_mismatch_preserves_previous_output(self):
        module = ModuleType("kiyosi")
        module.__version__ = "0.13.0"
        with TemporaryDirectory() as directory, patch(
            "generate_api_docs.importlib.import_module", return_value=module
        ):
            output = Path(directory)
            old = output / "index.md"
            old.write_text("previous", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "expected 0.14.0, got 0.13.0"):
                generate(output, "0.14.0", "a" * 40)
            self.assertEqual(old.read_text(encoding="utf-8"), "previous")

    def test_failed_generation_preserves_previous_output(self):
        module = ModuleType("kiyosi")
        module.__version__ = "0.14.0"
        module.__all__ = ["missing"]
        with TemporaryDirectory() as directory, patch(
            "generate_api_docs.importlib.import_module", return_value=module
        ):
            output = Path(directory) / "api"
            output.mkdir()
            (output / GENERATED_MARKER).touch()
            old = output / "index.md"
            old.write_text("previous", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "exports missing names"):
                generate(output, "0.14.0", "a" * 40)
            self.assertEqual(old.read_text(encoding="utf-8"), "previous")

    def test_rejects_unmarked_output(self):
        module = ModuleType("kiyosi")
        module.__version__ = "0.14.0"
        with TemporaryDirectory() as directory, patch(
            "generate_api_docs.importlib.import_module", return_value=module
        ):
            output = Path(directory)
            old = output / "notes.md"
            old.write_text("manual", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Refusing to replace unmarked"):
                generate(output, "0.14.0", "a" * 40)
            self.assertEqual(old.read_text(encoding="utf-8"), "manual")

    def test_replaces_generated_pages_and_records_pin(self):
        module = ModuleType("kiyosi")
        module.__version__ = "0.14.0"
        module.__all__ = ["__version__"]
        with TemporaryDirectory() as directory, patch(
            "generate_api_docs.PYTHON_MODULES", ("kiyosi",)
        ), patch("generate_api_docs.importlib.import_module", return_value=module):
            output = Path(directory) / "api"
            output.mkdir()
            (output / GENERATED_MARKER).touch()
            (output / "stale.md").touch()
            generate(output, "0.14.0", "a" * 40)
            overview = (output / "index.md").read_text(encoding="utf-8")
            self.assertFalse((output / "stale.md").exists())
            self.assertIn("0.14.0", overview)
            self.assertIn("a" * 40, overview)
            self.assertIn('href="./rust/kiyosi/index.html" target="_self"', overview)
            self.assertIn("__version__ = '0.14.0'", (output / "python/kiyosi.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
