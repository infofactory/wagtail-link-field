from django.test import TestCase

from wagtail_link_field.panels import LinkPanel


class TestLinkPanel(TestCase):
    """Tests for LinkPanel."""

    def test_clone_kwargs_includes_link_types(self):
        """clone_kwargs preserves link_types parameter."""
        panel = LinkPanel("test_field", link_types=["internal-link", "external-link"])
        kwargs = panel.clone_kwargs()
        self.assertEqual(kwargs["link_types"], ["internal-link", "external-link"])

    def test_clone_kwargs_default_link_types(self):
        """clone_kwargs has None for link_types when not specified."""
        panel = LinkPanel("test_field")
        kwargs = panel.clone_kwargs()
        self.assertIsNone(kwargs["link_types"])

    def test_panel_initialization(self):
        """LinkPanel initializes with field_name."""
        panel = LinkPanel("test_field")
        self.assertEqual(panel.field_name, "test_field")
