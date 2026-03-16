from django.test import TestCase

from wagtail_link_field.enums import (
    ACTION_FIELDS,
    ALL_LINK_TYPES,
    LINK_TYPE_LABELS,
    LinkType,
)


class TestLinkTypeEnum(TestCase):
    """Tests for LinkType enum."""

    def test_all_link_types_matches_enum(self):
        """ALL_LINK_TYPES contains all enum values."""
        enum_values = [lt.value for lt in LinkType]
        self.assertEqual(ALL_LINK_TYPES, enum_values)

    def test_link_type_labels_exist(self):
        """All link types have labels."""
        for link_type in ALL_LINK_TYPES:
            self.assertIn(link_type, LINK_TYPE_LABELS)

    def test_action_fields_mapping_complete(self):
        """All link types have action field mappings."""
        for link_type in ALL_LINK_TYPES:
            self.assertIn(link_type, ACTION_FIELDS)

    def test_action_fields_are_sets(self):
        """ACTION_FIELDS values are sets."""
        for fields in ACTION_FIELDS.values():
            self.assertIsInstance(fields, set)


class TestActionFields(TestCase):
    """Tests for ACTION_FIELDS mapping."""

    def test_internal_link_fields(self):
        """Internal link uses internal_link and page_query_string."""
        self.assertEqual(
            ACTION_FIELDS["internal-link"],
            {"internal_link", "page_query_string"},
        )

    def test_external_link_fields(self):
        """External link uses external_link."""
        self.assertEqual(ACTION_FIELDS["external-link"], {"external_link"})

    def test_url_link_types(self):
        """Email, phone, and custom links all use url_link."""
        for link_type in ["email-link", "phone-link", "custom-link"]:
            self.assertEqual(ACTION_FIELDS[link_type], {"url_link"})
