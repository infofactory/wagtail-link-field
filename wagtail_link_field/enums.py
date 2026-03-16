from enum import Enum

from django.utils.translation import gettext_lazy as _


class LinkType(str, Enum):
    """Supported link types."""
    INTERNAL = "internal-link"
    DOCUMENT = "document-link"
    EXTERNAL = "external-link"
    ANCHOR = "anchor-link"
    EMAIL = "email-link"
    PHONE = "phone-link"
    CUSTOM = "custom-link"

    @property
    def label(self):
        """Human-readable label for this link type."""
        return LINK_TYPE_LABELS[self.value]


# All supported link types in display order.
ALL_LINK_TYPES = [lt.value for lt in LinkType]

LINK_TYPE_LABELS = {
    LinkType.INTERNAL.value: _("Internal page"),
    LinkType.DOCUMENT.value: _("Document"),
    LinkType.EXTERNAL.value: _("External URL"),
    LinkType.ANCHOR.value: _("Anchor"),
    LinkType.EMAIL.value: _("Email"),
    LinkType.PHONE.value: _("Phone"),
    LinkType.CUSTOM.value: _("Custom URL"),
}

# Maps action types to their relevant field names
ACTION_FIELDS = {
    "internal-link": {"internal_link", "page_query_string"},
    "document-link": {"document_link"},
    "external-link": {"external_link"},
    "anchor-link": {"anchor_link"},
    "email-link": {"url_link"},
    "phone-link": {"url_link"},
    "custom-link": {"url_link"},
}
