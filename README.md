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

### Accessing link data in Python

Both `LinkBlock` values and `LinkField` values provide the same methods:

```python
# From a LinkField
page = MyPage.objects.first()
link = page.cta  # Returns LinkFieldValue instance

# From a LinkBlock in StreamField
for block in page.body:
    if block.block_type == 'link':
        link = block.value  # Returns LinkValue instance

# Both provide the same methods:
url = link.url()              # Computed URL (e.g., "/about/", "https://example.com", "mailto:test@example.com")
is_external = link.is_external()  # True for external, email, phone, document, custom links
title = link.title()          # Page/document title if available, otherwise None
safe_title = link.safe_title()    # Formatted title (page title or cleaned URL/email/phone)
action = link.action          # Link type: "internal-link", "external-link", etc.
```

### Using in templates

Load the template tags:

```django
{% load wagtail_link_field_tags %}
```

#### Option 1: Use `render_link` tag (recommended)

Automatically renders a complete `<a>` tag with proper attributes:

```django
{# Basic usage - uses safe_title automatically #}
{% render_link page.cta %}
{# Output: <a href="/about/">About Us</a> #}

{# With CSS class #}
{% render_link page.cta css_class="btn btn-primary" %}

{# With extra attributes #}
{% render_link page.cta extra_attrs='data-action="click"' %}

{# Works with StreamField blocks too #}
{% for block in page.body %}
    {% if block.block_type == 'link' %}
        {% render_link block.value css_class="content-link" %}
    {% endif %}
{% endfor %}
```

The `render_link` tag automatically:
- Adds `target="_blank"` and `rel="noopener noreferrer"` for external links
- Uses `safe_title()` for the link text (page title or formatted URL/email/phone)

#### Option 2: Use filters for custom markup

```django
{# Get the URL #}
<a href="{{ page.cta|link_url }}">Click here</a>

{# Get page/document title (returns None if not available) #}
<a href="{{ page.cta|link_url }}">
    {{ page.cta|link_title|default:"Read more" }}
</a>

{# Get formatted title (always returns something user-friendly) #}
<a href="{{ page.cta|link_url }}">
    {{ page.cta|link_safe_title }}
</a>

{# Build custom markup #}
{% if page.cta %}
    <a href="{{ page.cta|link_url }}" 
       class="{% if page.cta.is_external %}external-link{% endif %}">
        {{ page.cta|link_safe_title }}
    </a>
{% endif %}
```

#### Option 3: Access methods directly

```django
{# Access methods on the value object #}
<a href="{{ page.cta.url }}" 
   {% if page.cta.is_external %}target="_blank" rel="noopener noreferrer"{% endif %}>
    {{ page.cta.safe_title }}
</a>

{# Check link type #}
{% if page.cta.action == "internal-link" %}
    <a href="{{ page.cta.url }}" class="internal">{{ page.cta.title|default:page.cta.safe_title }}</a>
{% elif page.cta.action == "email-link" %}
    <a href="{{ page.cta.url }}" class="email">{{ page.cta.safe_title }}</a>
{% endif %}
```

#### When to use each approach:

- **`{% render_link %}`**: Quick, automatic rendering with sensible defaults
- **Filters (`|link_url`, `|link_safe_title`)**: Custom HTML structure but simpler syntax
- **Direct methods (`.url`, `.safe_title`)**: Maximum control and conditional logic

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
