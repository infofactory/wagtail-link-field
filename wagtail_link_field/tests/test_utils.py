from django.test import TestCase

from wagtail_link_field.utils import get_link_url, is_link_external


class TestGetLinkUrl(TestCase):
    """Tests for get_link_url utility function."""

    def test_external_link(self):
        """Returns external URL for external-link action."""
        data = {"action": "external-link", "external_link": "https://example.com"}
        self.assertEqual(get_link_url(data), "https://example.com")

    def test_anchor_link(self):
        """Returns anchor URL for anchor-link action."""
        data = {"action": "anchor-link", "anchor_link": "section"}
        self.assertEqual(get_link_url(data), "#section")

    def test_anchor_link_with_hash(self):
        """Strips leading # from anchor_link."""
        data = {"action": "anchor-link", "anchor_link": "#section"}
        self.assertEqual(get_link_url(data), "#section")

    def test_email_link(self):
        """Returns mailto: URL for email-link action."""
        data = {"action": "email-link", "url_link": "test@example.com"}
        self.assertEqual(get_link_url(data), "mailto:test@example.com")

    def test_email_link_with_mailto(self):
        """Preserves existing mailto: prefix."""
        data = {"action": "email-link", "url_link": "mailto:test@example.com"}
        self.assertEqual(get_link_url(data), "mailto:test@example.com")

    def test_phone_link(self):
        """Returns tel: URL for phone-link action."""
        data = {"action": "phone-link", "url_link": "+1234567890"}
        self.assertEqual(get_link_url(data), "tel:+1234567890")

    def test_phone_link_with_tel(self):
        """Preserves existing tel: prefix."""
        data = {"action": "phone-link", "url_link": "tel:+1234567890"}
        self.assertEqual(get_link_url(data), "tel:+1234567890")

    def test_custom_link(self):
        """Returns raw URL for custom-link action."""
        data = {"action": "custom-link", "url_link": "myapp://path"}
        self.assertEqual(get_link_url(data), "myapp://path")

    def test_empty_action(self):
        """Returns # for missing action."""
        data = {}
        self.assertEqual(get_link_url(data), "#")

    def test_unknown_action(self):
        """Returns # for unknown action."""
        data = {"action": "unknown-link"}
        self.assertEqual(get_link_url(data), "#")


class TestIsLinkExternal(TestCase):
    """Tests for is_link_external utility function."""

    def test_external_link_is_external(self):
        """external-link is external."""
        self.assertTrue(is_link_external({"action": "external-link"}))

    def test_internal_link_is_not_external(self):
        """internal-link is not external."""
        self.assertFalse(is_link_external({"action": "internal-link"}))

    def test_anchor_link_is_not_external(self):
        """anchor-link is not external."""
        self.assertFalse(is_link_external({"action": "anchor-link"}))

    def test_document_link_is_external(self):
        """document-link is external."""
        self.assertTrue(is_link_external({"action": "document-link"}))

    def test_email_link_is_external(self):
        """email-link is external."""
        self.assertTrue(is_link_external({"action": "email-link"}))

    def test_phone_link_is_external(self):
        """phone-link is external."""
        self.assertTrue(is_link_external({"action": "phone-link"}))

    def test_custom_link_is_external(self):
        """custom-link is external."""
        self.assertTrue(is_link_external({"action": "custom-link"}))

    def test_empty_action(self):
        """Empty action is external (defaults to True)."""
        self.assertTrue(is_link_external({}))
