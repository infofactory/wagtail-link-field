# wagtail-link-field

A flexible link block and field for Wagtail CMS that supports internal pages, external URLs, documents, anchors, email, phone, and custom links.

## Features

- **LinkBlock**: A StreamField block for flexible link selection
- **LinkField**: A model field that stores link data as JSON
- **LinkPanel**: A panel for editing LinkField in Wagtail admin
- **Template tags**: For rendering links in templates
- **Dynamic field visibility**: JavaScript shows/hides relevant fields based on selected link type
- **Clean JSON storage**: Only relevant fields are stored, irrelevant ones are stripped

## Installation

```bash
pip install wagtail-link-field
```

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_link_field",
    # ...
]
```

## Usage

### LinkBlock in StreamField

```python
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail_link_field import LinkBlock

class MyPage(Page):
    body = StreamField([
        ("link", LinkBlock()),
    ], blank=True, use_json_field=True)

    # Restrict to specific link types
    body_restricted = StreamField([
        ("link", LinkBlock(link_types=["internal-link", "external-link"])),
    ], blank=True, use_json_field=True)
```

### LinkField with LinkPanel

```python
from django.db import models
from wagtail_link_field import LinkField, LinkPanel

class MyPage(Page):
    cta = LinkField(blank=True, null=True)

    content_panels = Page.content_panels + [
        LinkPanel("cta"),
        # Or restrict link types:
        LinkPanel("cta_restricted", link_types=["internal-link", "external-link"]),
    ]
```

### Accessing link data

```python
page = MyPage.objects.first()

# Get the URL
url = page.cta.url()  # Returns the computed URL

# Check if external
is_external = page.cta.is_external()  # True for external, email, phone, custom links

# Get the action type
action = page.cta.action  # e.g., "internal-link", "external-link"
```

### Template tags

```django
{% load wagtail_link_field_tags %}

{# Render a full anchor tag #}
{% render_link page.cta css_class="btn btn-primary" %}

{# Or use filters for custom markup #}
<a href="{{ page.cta|link_url }}" class="my-class">{{ page.cta|link_title }}</a>
```

## Available link types

| Type | Description | Fields |
|------|-------------|--------|
| `internal-link` | Link to a Wagtail page | `internal_link`, `page_query_string` |
| `document-link` | Link to a Wagtail document | `document_link` |
| `external-link` | External URL | `external_link` |
| `anchor-link` | Same-page anchor | `anchor_link` |
| `email-link` | Email address | `url_link` (auto-prefixed with `mailto:`) |
| `phone-link` | Phone number | `url_link` (auto-prefixed with `tel:`) |
| `custom-link` | Custom URL scheme | `url_link` |

## Restricting link types

Pass `link_types` to `LinkBlock` or `LinkPanel`:

```python
# Only internal and external links
LinkBlock(link_types=["internal-link", "external-link"])

# Only documents
LinkPanel("download", link_types=["document-link"])
```

## Optional links

Set `required=False` for optional links:

```python
# LinkBlock (default is required=True)
LinkBlock(required=False)

# LinkField (use blank=True, null=True)
cta = LinkField(blank=True, null=True)
```

## Development

### Setup

```bash
# Clone the repo
git clone https://github.com/infofactory/wagtail-link-field.git
cd wagtail-link-field

# Install with uv
uv sync --extra testing
```

### Running tests

```bash
# Run tests
python testmanage.py test

# Run with coverage
python -m coverage run testmanage.py test
python -m coverage report -m
```

### Running linting

```bash
ruff check .
ruff format --check .
```

### Running tox (matrix testing)

```bash
tox
```

## License

BSD-3-Clause. See [LICENSE](LICENSE) for details.
