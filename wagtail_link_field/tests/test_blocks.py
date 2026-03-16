from django.test import TestCase

from wagtail_link_field.blocks import LinkBlock
from wagtail_link_field.enums import ALL_LINK_TYPES


class TestLinkBlock(TestCase):
    """Tests for LinkBlock."""

    def test_default_initialization(self):
        """LinkBlock initializes with all link types by default."""
        block = LinkBlock()
        self.assertEqual(block._active_link_types, ALL_LINK_TYPES)
        self.assertTrue(block._is_required)

    def test_restricted_link_types(self):
        """LinkBlock can be restricted to specific link types."""
        block = LinkBlock(link_types=["internal-link", "external-link"])
        self.assertEqual(block._active_link_types, ["internal-link", "external-link"])

    def test_optional_block(self):
        """LinkBlock can be optional."""
        block = LinkBlock(required=False)
        self.assertFalse(block._is_required)

    def test_get_prep_value_filters_irrelevant_fields(self):
        """get_prep_value removes fields not relevant to the selected action."""
        block = LinkBlock()

        # Use external-link to avoid needing actual Page objects
        value = block.to_python({
            "action": "external-link",
            "external_link": "https://example.com",
            "internal_link": None,  # Should be removed
            "document_link": None,  # Should be removed
        })
        result = block.get_prep_value(value)
        self.assertIn("action", result)
        self.assertIn("external_link", result)
        self.assertNotIn("internal_link", result)
        self.assertNotIn("document_link", result)

    def test_get_prep_value_removes_empty_values(self):
        """get_prep_value removes None and empty string values."""
        block = LinkBlock()
        value = block.to_python({
            "action": "external-link",
            "external_link": "https://example.com",
            "internal_link": None,
            "anchor_link": "",
        })
        result = block.get_prep_value(value)
        self.assertNotIn("internal_link", result)
        self.assertNotIn("anchor_link", result)


class TestLinkValue(TestCase):
    """Tests for LinkValue (StructValue subclass)."""

    def test_url_method(self):
        """LinkValue.url() returns computed URL."""
        block = LinkBlock()
        value = block.to_python({"action": "external-link", "external_link": "https://example.com"})
        self.assertEqual(value.url(), "https://example.com")

    def test_is_external_for_external_link(self):
        """is_external returns True for external links."""
        block = LinkBlock()
        value = block.to_python({"action": "external-link", "external_link": "https://example.com"})
        self.assertTrue(value.is_external())

    def test_is_external_for_internal_link(self):
        """is_external returns False for internal links."""
        block = LinkBlock()
        value = block.to_python({"action": "internal-link"})
        self.assertFalse(value.is_external())
