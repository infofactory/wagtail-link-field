from django.test import TestCase

from wagtail_link_field.fields import LinkField, LinkFieldValue


class TestLinkFieldValue(TestCase):
    """Tests for LinkFieldValue wrapper."""

    def test_url_for_external_link(self):
        """url() returns external URL for external-link action."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com"})
        self.assertEqual(value.url(), "https://example.com")

    def test_url_for_anchor_link(self):
        """url() returns anchor URL for anchor-link action."""
        value = LinkFieldValue({"action": "anchor-link", "anchor_link": "section"})
        self.assertEqual(value.url(), "#section")

    def test_url_for_anchor_link_with_hash(self):
        """url() strips leading # from anchor_link."""
        value = LinkFieldValue({"action": "anchor-link", "anchor_link": "#section"})
        self.assertEqual(value.url(), "#section")

    def test_url_for_email_link(self):
        """url() returns mailto: URL for email-link action."""
        value = LinkFieldValue({"action": "email-link", "url_link": "test@example.com"})
        self.assertEqual(value.url(), "mailto:test@example.com")

    def test_url_for_email_link_with_mailto(self):
        """url() preserves existing mailto: prefix."""
        value = LinkFieldValue({"action": "email-link", "url_link": "mailto:test@example.com"})
        self.assertEqual(value.url(), "mailto:test@example.com")

    def test_url_for_phone_link(self):
        """url() returns tel: URL for phone-link action."""
        value = LinkFieldValue({"action": "phone-link", "url_link": "+1234567890"})
        self.assertEqual(value.url(), "tel:+1234567890")

    def test_url_for_custom_link(self):
        """url() returns raw URL for custom-link action."""
        value = LinkFieldValue({"action": "custom-link", "url_link": "myapp://path"})
        self.assertEqual(value.url(), "myapp://path")

    def test_url_for_empty_value(self):
        """url() returns # for empty/invalid links."""
        value = LinkFieldValue({})
        self.assertEqual(value.url(), "#")

    def test_is_external_for_external_link(self):
        """is_external() returns True for external-link."""
        value = LinkFieldValue({"action": "external-link"})
        self.assertTrue(value.is_external())

    def test_is_external_for_internal_link(self):
        """is_external() returns False for internal-link."""
        value = LinkFieldValue({"action": "internal-link"})
        self.assertFalse(value.is_external())

    def test_is_external_for_anchor_link(self):
        """is_external() returns False for anchor-link."""
        value = LinkFieldValue({"action": "anchor-link"})
        self.assertFalse(value.is_external())

    def test_is_external_for_email_link(self):
        """is_external() returns True for email-link."""
        value = LinkFieldValue({"action": "email-link"})
        self.assertTrue(value.is_external())

    def test_action_property(self):
        """action property returns the action value."""
        value = LinkFieldValue({"action": "external-link"})
        self.assertEqual(value.action, "external-link")

    def test_action_property_empty(self):
        """action property returns empty string for missing action."""
        value = LinkFieldValue({})
        self.assertEqual(value.action, "")

    def test_bool_true(self):
        """bool() returns True when action is set."""
        value = LinkFieldValue({"action": "external-link"})
        self.assertTrue(value)

    def test_bool_false(self):
        """bool() returns False when action is not set."""
        value = LinkFieldValue({})
        self.assertFalse(value)

    def test_as_dict(self):
        """as_dict() returns the underlying data dict."""
        data = {"action": "external-link", "external_link": "https://example.com"}
        value = LinkFieldValue(data)
        self.assertEqual(value.as_dict(), data)

    def test_strips_empty_values_on_init(self):
        """Empty values are stripped on initialization."""
        value = LinkFieldValue({
            "action": "external-link",
            "external_link": "https://example.com",
            "internal_link": None,
            "anchor_link": "",
        })
        self.assertNotIn("internal_link", value._data)
        self.assertNotIn("anchor_link", value._data)


class TestLinkField(TestCase):
    """Tests for LinkField model field."""

    def test_field_creation(self):
        """LinkField can be created with standard field options."""
        field = LinkField(blank=True, null=True)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)
