from django.apps import AppConfig


class WagtailLinkFieldConfig(AppConfig):
    name = "wagtail_link_field"
    label = "wagtail_link_field"
    verbose_name = "Wagtail Link Field"

    def ready(self):
        from . import blocks  # noqa: F401
