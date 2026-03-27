__version__ = "0.1.2"

# Support for Django < 3.2 and simple INSTALLED_APPS configuration
default_app_config = "wagtail_link_field.apps.WagtailLinkFieldConfig"


def __getattr__(name):
    """Lazy import to avoid Django AppRegistryNotReady during settings import."""
    if name == "LinkBlock":
        from wagtail_link_field.blocks import LinkBlock

        return LinkBlock
    elif name == "LinkValue":
        from wagtail_link_field.blocks import LinkValue

        return LinkValue
    elif name == "LinkField":
        from wagtail_link_field.fields import LinkField

        return LinkField
    elif name == "LinkFieldValue":
        from wagtail_link_field.fields import LinkFieldValue

        return LinkFieldValue
    elif name == "LinkPanel":
        from wagtail_link_field.panels import LinkPanel

        return LinkPanel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "__version__",
    "LinkBlock",
    "LinkValue",
    "LinkField",
    "LinkFieldValue",
    "LinkPanel",
]
