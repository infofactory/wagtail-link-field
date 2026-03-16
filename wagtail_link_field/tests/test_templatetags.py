from django.template import Context, Template
from django.test import TestCase

from wagtail_link_field.fields import LinkFieldValue


class TestRenderLinkTag(TestCase):
    """Tests for render_link template tag."""

    def render_template(self, template_str, context):
        """Helper to render a template string with context."""
        template = Template(template_str)
        return template.render(Context(context))

    def test_render_link_basic(self):
        """render_link produces an anchor tag."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com"})
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{% render_link value %}',
            {"value": value}
        )
        self.assertIn('href="https://example.com"', result)
        self.assertIn("<a", result)
        self.assertIn("</a>", result)

    def test_render_link_with_css_class(self):
        """render_link applies css_class."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com"})
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{% render_link value css_class="btn btn-primary" %}',
            {"value": value}
        )
        self.assertIn('class="btn btn-primary"', result)

    def test_render_link_external_has_target_blank(self):
        """render_link adds target=_blank for external links."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com"})
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{% render_link value %}',
            {"value": value}
        )
        self.assertIn('target="_blank"', result)
        self.assertIn('rel="noopener noreferrer"', result)

    def test_render_link_internal_no_target(self):
        """render_link does not add target for internal links."""
        value = LinkFieldValue({"action": "internal-link"})
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{% render_link value %}',
            {"value": value}
        )
        self.assertNotIn("target", result)
        self.assertNotIn("rel", result)


class TestLinkUrlFilter(TestCase):
    """Tests for link_url filter."""

    def render_template(self, template_str, context):
        """Helper to render a template string with context."""
        template = Template(template_str)
        return template.render(Context(context))

    def test_link_url_filter(self):
        """link_url filter returns the URL."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com"})
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{{ value|link_url }}',
            {"value": value}
        )
        self.assertEqual(result.strip(), "https://example.com")

    def test_link_url_filter_empty(self):
        """link_url filter returns # for empty values."""
        value = LinkFieldValue({})
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{{ value|link_url }}',
            {"value": value}
        )
        self.assertEqual(result.strip(), "#")


class TestLinkTitleFilter(TestCase):
    """Tests for link_title filter."""

    def render_template(self, template_str, context):
        """Helper to render a template string with context."""
        template = Template(template_str)
        return template.render(Context(context))

    def test_link_title_filter_with_title(self):
        """link_title filter returns None for external links (no page/document)."""
        value = LinkFieldValue({
            "action": "external-link",
            "external_link": "https://example.com",
        })
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{{ value|link_title }}',
            {"value": value}
        )
        self.assertEqual(result.strip(), "None")

    def test_link_title_filter_empty(self):
        """link_title filter returns None when no title."""
        value = LinkFieldValue({"action": "external-link", "external_link": "https://example.com"})
        result = self.render_template(
            '{% load wagtail_link_field_tags %}{{ value|link_title }}',
            {"value": value}
        )
        self.assertEqual(result.strip(), "None")
