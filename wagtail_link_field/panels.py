import json

from django import forms
from wagtail.admin.panels import FieldPanel
from wagtail.blocks.base import BlockWidget

from .blocks import LinkBlock
from .enums import ACTION_FIELDS


def _normalize_to_dict(value):
    """Convert value to dict, handling JSON strings and None, masking JS 'undefined'."""
    result = {}
    if hasattr(value, "as_dict"):
        result = value.as_dict()
    elif isinstance(value, str):
        try:
            result = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            result = {}
    elif isinstance(value, dict):
        result = value

    if isinstance(result, dict):
        return {k: v for k, v in result.items() if v not in (None, "", "undefined")}
    return {}


class LinkBlockWidget(BlockWidget):
    """
    Wraps BlockWidget(LinkBlock(...)) for use as a standalone form widget.
    """

    def __init__(self, link_types=None, required=True, *args, **kwargs):
        block = LinkBlock(link_types=link_types, required=required)
        super().__init__(block, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if hasattr(value, "items"):
            return dict(value.items())
        return value


class LinkFormField(forms.Field):
    """
    Form field for LinkField.
    Converts values to StructValue and delegates validation to LinkBlock.
    """

    def __init__(self, link_types=None, *args, **kwargs):
        kwargs.pop("encoder", None)
        kwargs.pop("decoder", None)
        kwargs.pop("block", None)  # Wagtail StreamField passes this, ignore it
        super().__init__(*args, **kwargs)
        self._block = LinkBlock(link_types=link_types, required=self.required)
        self.widget = LinkBlockWidget(link_types=link_types, required=self.required)

    def prepare_value(self, value):
        value = _normalize_to_dict(value)
        if not value:
            return None
        # Convert to StructValue so BlockWidget gets a fully instantiated object with default keys
        return self._block.to_python(value)

    def clean(self, value):
        value = _normalize_to_dict(value)

        # Check if value is effectively empty (no action selected)
        if not value.get("action") and not self.required:
            return None

        # Convert Page/Document objects to IDs before to_python
        # The widget returns resolved objects, but to_python expects raw IDs
        for name, block in self._block.child_blocks.items():
            val = value.get(name)
            if val is not None:
                value[name] = block.get_prep_value(val)

        struct_value = self._block.to_python(value)
        cleaned = self._block.clean(struct_value)

        # Convert Page/Document objects to IDs by calling each child block's get_prep_value
        result = {}
        for name, block in self._block.child_blocks.items():
            val = cleaned.get(name) if hasattr(cleaned, "get") else None
            if val is not None and val != "":
                result[name] = block.get_prep_value(val)

        # Filter out None values and empty strings
        result = {k: v for k, v in result.items() if v is not None and v != ""}

        # Remove fields not relevant to the selected action
        action = result.get("action")
        if action in ACTION_FIELDS:
            allowed = {"action"} | ACTION_FIELDS[action]
            result = {k: v for k, v in result.items() if k in allowed}

        return result


class LinkPanel(FieldPanel):
    """
    Use instead of FieldPanel for LinkField in content_panels.

    Parameters
    ----------
    link_types : list[str], optional
        Restrict which link types are offered. Defaults to all types.
        Available values: "internal-link", "document-link", "external-link",
        "anchor-link", "email-link", "phone-link", "custom-link"

    Examples::

        # All link types (default)
        LinkPanel("cta")

        # Only page and external URL
        LinkPanel("cta", link_types=["internal-link", "external-link"])
    """

    def __init__(self, field_name, link_types=None, **kwargs):
        self._link_types = link_types
        super().__init__(field_name, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs["link_types"] = self._link_types
        return kwargs

    def get_form_options(self):
        opts = super().get_form_options()

        try:
            field_required = not getattr(self.db_field, "blank", False)
        except Exception:
            field_required = True

        link_types = self._link_types

        class PanelLinkFormField(LinkFormField):
            def __init__(self, **kwargs):
                kwargs.pop("required", None)
                super().__init__(
                    link_types=link_types,
                    required=field_required,
                    **kwargs
                )

        if "field_classes" not in opts:
            opts["field_classes"] = {}
        opts["field_classes"][self.field_name] = PanelLinkFormField
        return opts
