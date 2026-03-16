from django.test import TestCase

from wagtail_link_field.blocks import LinkBlock
from wagtail_link_field.fields import LinkFieldValue


class TestLinkValueTitleMethods(TestCase):
    """Tests for title() and safe_title() methods on LinkValue."""

    def setUp(self):
        """Create a LinkBlock instance for testing."""
        self.block = LinkBlock()

    def test_title_returns_none_for_external_link(self):
        """title() returns None for external links (no page/document)."""
        value = self.block.to_python({"action": "external-link", "external_link": "https://example.com"})
        self.assertIsNone(value.title())

    def test_safe_title_formats_external_link(self):
        """safe_title() removes protocol from external links."""
        value = self.block.to_python({"action": "external-link", "external_link": "https://example.com/"})
        self.assertEqual(value.safe_title(), "example.com")

    def test_safe_title_formats_email(self):
        """safe_title() removes mailto: from email links."""
        value = self.block.to_python({"action": "email-link", "url_link": "mailto:test@example.com"})
        self.assertEqual(value.safe_title(), "test@example.com")

    def test_safe_title_formats_phone(self):
        """safe_title() removes tel: from phone links."""
        value = self.block.to_python({"action": "phone-link", "url_link": "tel:+1234567890"})
        self.assertEqual(value.safe_title(), "+1234567890")

    def test_safe_title_formats_anchor(self):
        """safe_title() removes # from anchor links."""
        value = self.block.to_python({"action": "anchor-link", "anchor_link": "#section"})
        self.assertEqual(value.safe_title(), "section")

    def test_safe_title_custom_link(self):
        """safe_title() returns custom link as-is."""
        value = self.block.to_python({"action": "custom-link", "url_link": "myapp://path"})
        self.assertEqual(value.safe_title(), "myapp://path")


class TestLinkFieldValueTitleMethods(TestCase):
    """Tests for title() and safe_title() methods on LinkFieldValue."""

    def test_title_returns_none_for_external_link(self):
        """title() returns None for external links (no page/document)."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com"})
        self.assertIsNone(value.title())

    def test_safe_title_formats_external_link(self):
        """safe_title() removes protocol from external links."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com/"})
        self.assertEqual(value.safe_title(), "example.com")

    def test_safe_title_formats_email(self):
        """safe_title() removes mailto: from email links."""
        value = LinkFieldValue({"action": "email-link", "url_link": "mailto:test@example.com"})
        self.assertEqual(value.safe_title(), "test@example.com")

    def test_safe_title_formats_phone(self):
        """safe_title() removes tel: from phone links."""
        value = LinkFieldValue({"action": "phone-link", "url_link": "tel:+1234567890"})
        self.assertEqual(value.safe_title(), "+1234567890")

    def test_safe_title_formats_anchor(self):
        """safe_title() removes # from anchor links."""
        value = LinkFieldValue({"action": "anchor-link", "anchor_link": "#section"})
        self.assertEqual(value.safe_title(), "section")

    def test_safe_title_custom_link(self):
        """safe_title() returns custom link as-is."""
        value = LinkFieldValue({"action": "custom-link", "url_link": "myapp://path"})
        self.assertEqual(value.safe_title(), "myapp://path")
