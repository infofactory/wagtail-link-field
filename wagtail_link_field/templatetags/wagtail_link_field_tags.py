from django import template
from django.utils.safestring import mark_safe


register = template.Library()


def _url(value):
    if hasattr(value, "url"):
        return value.url() if callable(value.url) else value.url
    return "#"


def _title(value):
    """Get title from page/document, or None."""
    if hasattr(value, "title"):
        result = value.title() if callable(value.title) else value.title
        return result
    return None


def _safe_title(value):
    """Get title or formatted link value."""
    if hasattr(value, "safe_title"):
        result = value.safe_title() if callable(value.safe_title) else value.safe_title
        return result
    # Fallback to URL
    return _url(value)


def _is_external(value):
    if hasattr(value, "is_external"):
        return value.is_external() if callable(value.is_external) else value.is_external
    return False


@register.inclusion_tag("wagtail_link_field/link_tag.html")
def render_link(value, css_class="", extra_attrs=""):
    url = _url(value)
    safe_title = _safe_title(value)
    external = _is_external(value)
    return {
        "url": url,
        "title": safe_title,
        "is_external": external,
        "css_class": css_class,
        "extra_attrs": mark_safe(extra_attrs),
        "rel": "noopener noreferrer" if external else "",
        "target": "_blank" if external else "",
    }


@register.filter(name="link_url")
def link_url_filter(value):
    return _url(value)


@register.filter(name="link_title")
def link_title_filter(value):
    return _title(value)


@register.filter(name="link_safe_title")
def link_safe_title_filter(value):
    return _safe_title(value)
