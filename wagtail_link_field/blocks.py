import json

from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.telepath import register
from wagtail.blocks.struct_block import StructBlockAdapter, StructBlockValidationError
from wagtail.documents.blocks import DocumentChooserBlock

from .enums import ACTION_FIELDS, ALL_LINK_TYPES, LINK_TYPE_LABELS, STANDARD_LINK_FIELDS
from .utils import get_link_title, get_link_url, get_safe_link_title, is_link_external


class LinkValue(blocks.StructValue):
    def url(self):
        return get_link_url(self)

    def is_external(self):
        return is_link_external(self)

    def title(self):
        """Return page/document title if available, otherwise None."""
        return get_link_title(self)

    def safe_title(self):
        """Return page/document title or formatted link value."""
        return get_safe_link_title(self)


class LinkAdapter(StructBlockAdapter):
    js_constructor = "wagtail_link_field.LinkBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return structblock_media + forms.Media(
            js=["wagtail_link_field/js/link-block.js"],
        )


class LinkBlock(blocks.StructBlock):
    """
    A flexible link block.

    Parameters
    ----------
    link_types : list[str], optional
        Subset of ALL_LINK_TYPES to offer. Defaults to all types.
        Example: LinkBlock(link_types=["internal-link", "external-link"])
    required : bool
        Whether a link type must be selected. Defaults to True.
    """

    def __init__(self, local_blocks=None, search_index=True, link_types=None, **kwargs):
        # Use get() to distinguish between False and not provided
        is_required = kwargs.pop("required") if "required" in kwargs else True

        # Resolve the active link type list
        if link_types is None:
            active_types = ALL_LINK_TYPES
        else:
            # Preserve canonical order, ignore unknown values
            active_types = [t for t in ALL_LINK_TYPES if t in link_types]

        self._active_link_types = active_types
        self._is_required = is_required

        # --- action choice block ---
        choices = [(t, LINK_TYPE_LABELS[t]) for t in active_types]

        # Add empty option for optional fields
        if not is_required:
            choices.insert(0, ("", "---"))

        default_action = active_types[0] if is_required and active_types else ""

        # Define child blocks before calling super().__init__()
        if local_blocks is None:
            local_blocks = [
                ("action", blocks.ChoiceBlock(
                    choices=choices,
                    required=is_required,
                    default=default_action,
                    label=_("Link type"),
                )),
                ("internal_link", blocks.PageChooserBlock(
                    required=False, label=_("Page")
                )),
                ("page_query_string", blocks.CharBlock(
                    required=False,
                    label=_("URL suffix (optional)"),
                    help_text=_("Append to the page URL: #anchor, ?query=value, or both (e.g., ?utm_source=newsletter#section)"),
                )),
                ("external_link", blocks.URLBlock(
                    required=False, label=_("External URL")
                )),
                ("document_link", DocumentChooserBlock(
                    required=False, label=_("Document")
                )),
                ("anchor_link", blocks.CharBlock(
                    required=False,
                    label=_("Anchor"),
                    help_text=_("Element ID without the # symbol"),
                )),
                ("url_link", blocks.CharBlock(
                    required=False,
                    label=_("URL / address"),
                    help_text=_("Used for email, phone and custom links"),
                )),
            ]

        super().__init__(local_blocks, search_index, **kwargs)

    def get_form_context(self, value, prefix="", errors=None):
        ctx = super().get_form_context(value, prefix=prefix, errors=errors)
        # Pass active link types to the JS via a data attribute on the block
        ctx["active_link_types"] = json.dumps(self._active_link_types)
        return ctx

    def clean(self, value):
        action = value.get("action")

        # If no action selected and field is optional, allow empty
        if not action and not self._is_required:
            return super().clean(value)

        validations = {
            "internal-link": ("internal_link", _("Please select a page.")),
            "document-link": ("document_link", _("Please select a document.")),
            "external-link": ("external_link", _("Please enter an external URL.")),
            "anchor-link": ("anchor_link", _("Please enter an anchor ID.")),
            "email-link": ("url_link", _("Please enter an email address.")),
            "phone-link": ("url_link", _("Please enter a phone number.")),
            "custom-link": ("url_link", _("Please enter a URL.")),
        }

        if action in validations:
            field_name, error_msg = validations[action]
            val = value.get(field_name)
            if not val:
                # Wagtail blocks need StructBlockValidationError, which wraps BlockValidationError
                # This ensures the specific child field (e.g. url_link) gets highlighted red
                raise StructBlockValidationError(block_errors={
                    field_name: ValidationError(error_msg)
                })

        return super().clean(value)

    def get_prep_value(self, value):
        result = super().get_prep_value(value)
        # Drop empty lists/dicts/nulls and the string "undefined" from JS
        result = {
            k: v for k, v in result.items() if v not in (None, "")
        }

        # Remove standard link fields not relevant to the selected action
        # Custom fields added via local_blocks are preserved
        action = result.get("action")
        if action in ACTION_FIELDS:
            # Keep action + relevant standard fields + any custom fields
            allowed_standard = {"action"} | ACTION_FIELDS[action]
            result = {
                k: v for k, v in result.items()
                if k not in STANDARD_LINK_FIELDS or k in allowed_standard
            }

        return result

    def get_form_state(self, value):
        # 1. Handle None values (the cause of your current crash)
        if value is None:
            # Return a dict containing defaults for all child blocks
            return {
                name: child.get_form_state(child.get_default())
                for name, child in self.child_blocks.items()
            }

        # 2. Ensure value is converted to a StructValue
        if isinstance(value, dict) and not isinstance(value, self.meta.value_class):
            value = self.to_python(value)

        return super().get_form_state(value)

    class Meta:
        icon = "link"
        label = _("Link")
        value_class = LinkValue


register(LinkAdapter(), LinkBlock)
