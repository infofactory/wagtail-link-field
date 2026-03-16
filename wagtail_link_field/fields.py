from django.db import models

from .utils import get_link_url, is_link_external


class LinkFieldValue:
    """
    Wraps the raw dict stored in a JSONField and exposes url() and is_external() methods.
    """

    def __init__(self, data: dict):
        if data:
            self._data = {k: v for k, v in data.items() if v not in (None, "")}
        else:
            self._data = {}

    def url(self):
        return get_link_url(self._data)

    def is_external(self):
        return is_link_external(self._data)

    @property
    def action(self):
        return self._data.get("action", "")

    def as_dict(self):
        return dict(self._data)

    def __bool__(self):
        return bool(self._data.get("action"))

    def __repr__(self):
        return f"<LinkFieldValue action={self.action!r}>"

    def __str__(self):
        return self.url()


class LinkDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self
        raw = instance.__dict__.get(self.field.attname)
        if raw and isinstance(raw, dict):
            return LinkFieldValue(raw)
        return None

    def __set__(self, instance, value):
        if isinstance(value, LinkFieldValue):
            instance.__dict__[self.field.attname] = value.as_dict()
        else:
            instance.__dict__[self.field.attname] = value


class LinkField(models.JSONField):
    """
    Stores a link as JSON. Access via model instances returns a
    LinkFieldValue with .url(), .is_external(), .action properties.

    Always pair with LinkPanel in content_panels.


    Example::

        from wagtail_link_field import LinkField, LinkPanel

        class MyPage(Page):
            cta = LinkField(null=True, blank=True)
            content_panels = Page.content_panels + [
                LinkPanel("cta"),
            ]
    """

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        setattr(cls, name, LinkDescriptor(self))

    def to_python(self, value):
        # Unwrap LinkFieldValue back to dict before letting JSONField handle it
        if isinstance(value, LinkFieldValue):
            value = value.as_dict()
        return super().to_python(value)

    def get_prep_value(self, value):
        # Unwrap LinkFieldValue back to dict before preparing for database
        if isinstance(value, LinkFieldValue):
            value = value.as_dict()
        return super().get_prep_value(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Unwrap LinkFieldValue back to dict before database serialization
        if isinstance(value, LinkFieldValue):
            value = value.as_dict()
        return super().get_db_prep_value(value, connection, prepared)

    def validate(self, value, model_instance):
        # Unwrap LinkFieldValue back to dict because JSONField runs json.dumps() in validate(),
        # which crashes on custom Python objects
        if isinstance(value, LinkFieldValue):
            value = value.as_dict()
        super().validate(value, model_instance)

    def value_to_string(self, obj):
        # Overridden to prevent Wagtail revisions from crashing on LinkFieldValue
        # when calling json.dumps() during historical save
        value = super().value_to_string(obj)
        if hasattr(value, "as_dict"):
            return value.as_dict()
        return value

    def value_from_object(self, obj):
        # Core unwrapping for Django serializers (like Wagtail's revision system)
        value = super().value_from_object(obj)
        if hasattr(value, "as_dict"):
            return value.as_dict()
        return value
