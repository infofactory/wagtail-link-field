from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_link_field import LinkBlock, LinkField, LinkPanel


class TestPage(Page):
    """A test page with LinkField and LinkPanel."""

    link = LinkField(blank=True, null=True)
    link_restricted = LinkField(blank=True, null=True)

    content_panels = Page.content_panels + [
        LinkPanel("link"),
        LinkPanel("link_restricted", link_types=["internal-link", "external-link"]),
    ]


class TestStreamFieldPage(Page):
    """A test page with LinkBlock in StreamField."""

    body = StreamField(
        [
            ("link", LinkBlock()),
            ("link_optional", LinkBlock(required=False)),
            ("link_restricted", LinkBlock(link_types=["internal-link", "document-link"])),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
