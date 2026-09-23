import unittest
import xml.etree.ElementTree as ET

from generate_api_docs import member_markdown, python_doc_markdown, source_path, split_signature


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


if __name__ == "__main__":
    unittest.main()
