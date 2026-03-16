"""Shared utilities for link field functionality."""


def get_link_url(data):
    """
    Compute the URL from a link data dict or StructValue.

    Args:
        data: A dict-like object with 'action' and corresponding field values.
              Supports both dict and StructValue (both have .get() method).

    Returns:
        The computed URL string, or '#' if no valid link.
    """
    from wagtail.documents import get_document_model
    from wagtail.models import Page
    action = data.get("action")
    page_query_string = data.get("page_query_string") or ""

    if action == "internal-link" and data.get("internal_link"):
        page = data.get("internal_link")
        if isinstance(page, int) or (isinstance(page, str) and str(page).isdigit()):
            page = Page.objects.filter(id=page).first()
        if page:
            base = page.localized.url
            if page_query_string:
                return base + page_query_string
            return base
    elif action == "document-link" and data.get("document_link"):
        doc = data.get("document_link")
        if isinstance(doc, int) or (isinstance(doc, str) and str(doc).isdigit()):
            Document = get_document_model()
            doc = Document.objects.filter(id=doc).first()
        if doc:
            return doc.url
    elif action == "external-link" and data.get("external_link"):
        return data.get("external_link")
    elif action == "anchor-link" and data.get("anchor_link"):
        return "#" + data.get("anchor_link").lstrip("#")
    elif action == "email-link" and data.get("url_link"):
        url = data.get("url_link")
        return url if url.startswith("mailto:") else f"mailto:{url}"
    elif action == "phone-link" and data.get("url_link"):
        url = data.get("url_link")
        return url if url.startswith("tel:") else f"tel:{url}"
    elif action == "custom-link" and data.get("url_link"):
        return data.get("url_link")
    return "#"


def is_link_external(data):
    """
    Determine if a link is external.

    Args:
        data: A dict-like object with 'action' key.

    Returns:
        True if the link is external (not internal or anchor), False otherwise.
    """
    return data.get("action") not in ("internal-link", "anchor-link")


def get_link_title(data):
    """
    Get the title for a link (page title, document title, or None).

    Args:
        data: A dict-like object with 'action' and corresponding field values.

    Returns:
        The title string from page/document, or None if not available.
    """
    from wagtail.documents import get_document_model
    from wagtail.models import Page

    action = data.get("action")

    if action == "internal-link" and data.get("internal_link"):
        page = data.get("internal_link")
        if isinstance(page, int) or (isinstance(page, str) and str(page).isdigit()):
            page = Page.objects.filter(id=page).first()
        if page and hasattr(page, "title"):
            return page.title
    elif action == "document-link" and data.get("document_link"):
        doc = data.get("document_link")
        if isinstance(doc, int) or (isinstance(doc, str) and str(doc).isdigit()):
            Document = get_document_model()
            doc = Document.objects.filter(id=doc).first()
        if doc and hasattr(doc, "title"):
            return doc.title

    return None


def get_safe_link_title(data):
    """
    Get a safe/formatted title for a link.

    Returns page/document title if available, otherwise formats the link value
    in a user-friendly way (removes protocols, formats emails/phones).

    Args:
        data: A dict-like object with 'action' and corresponding field values.

    Returns:
        A formatted title string.
    """
    # Try to get page/document title first
    title = get_link_title(data)
    if title:
        return title

    # Helper to safely get value (handles both dict and StructValue)
    def get_val(key):
        val = data.get(key)
        # Handle StructValue which may return empty string instead of None
        return val if val not in (None, "") else None

    action = get_val("action")

    # Format based on action type
    if action == "external-link":
        url = get_val("external_link")
        if url:
            # Remove protocol and trailing slash
            url = str(url).replace("https://", "").replace("http://", "")
            return url.rstrip("/")

    elif action == "email-link":
        email = get_val("url_link")
        if email:
            # Remove mailto: if present
            return str(email).replace("mailto:", "")

    elif action == "phone-link":
        phone = get_val("url_link")
        if phone:
            # Remove tel: if present
            return str(phone).replace("tel:", "")

    elif action == "anchor-link":
        anchor = get_val("anchor_link")
        if anchor:
            # Return anchor without #
            return str(anchor).lstrip("#")

    elif action == "custom-link":
        custom = get_val("url_link")
        if custom:
            return str(custom)

    # Fallback to URL
    return get_link_url(data)
