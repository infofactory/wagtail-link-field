from django import template
from django.utils.safestring import mark_safe


register = template.Library()


def _url(value):
    if hasattr(value, "url"):
        return value.url() if callable(value.url) else value.url
    return "#"


def _title(value):
    if hasattr(value, "_data"):
        return value._data.get("title", "")
    if hasattr(value, "get"):
        return value.get("title", "")
    return ""


def _is_external(value):
    if hasattr(value, "is_external"):
        return value.is_external() if callable(value.is_external) else value.is_external
    return False


@register.inclusion_tag("wagtail_link_field/link_tag.html")
def render_link(value, css_class="", extra_attrs=""):
    url = _url(value)
    title = _title(value)
    external = _is_external(value)
    return {
        "url": url,
        "title": title or url,
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
