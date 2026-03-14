"""Email-specific sanitization for the Google plugin.

Strips tracking pixels, sanitizes HTML to plain text for LLM consumption,
validates email addresses, and enforces content length limits.
"""

import re
import unicodedata

# ---------------------------------------------------------------------------
# Limits
# ---------------------------------------------------------------------------
MAX_EMAIL_BODY = 50_000
MAX_SUBJECT = 500
MAX_EMAIL_ADDRESS = 254
MAX_ATTACHMENT_FILENAME = 255
MAX_BULK_CHARS = 200_000

# ---------------------------------------------------------------------------
# Email address validation
# ---------------------------------------------------------------------------
_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)


def validate_email_address(addr: str) -> bool:
    """Validate an email address format."""
    if not addr or len(addr) > MAX_EMAIL_ADDRESS:
        return False
    match = re.search(r"<([^>]+)>", addr)
    if match:
        addr = match.group(1)
    addr = addr.strip()
    return bool(_EMAIL_RE.match(addr))


def validate_recipients(addresses: str, allowed: list[str] | None = None) -> list[str]:
    """Validate a comma-separated list of email addresses.

    Returns list of valid addresses. Raises ValueError if any are invalid
    or not in the allowed list.
    """
    if not addresses:
        raise ValueError("No recipients specified.")
    parts = [a.strip() for a in addresses.split(",") if a.strip()]
    if not parts:
        raise ValueError("No valid recipients specified.")

    for addr in parts:
        if not validate_email_address(addr):
            raise ValueError(f"Invalid email address: {addr}")

    if allowed:
        for addr in parts:
            match = re.search(r"<([^>]+)>", addr)
            bare = match.group(1).strip().lower() if match else addr.strip().lower()
            allowed_lower = [a.lower() for a in allowed]
            if bare not in allowed_lower:
                raise ValueError(
                    f"Recipient {addr} is not in the allowed recipients list."
                )

    return parts


# ---------------------------------------------------------------------------
# Tracking pixel removal
# ---------------------------------------------------------------------------

_TRACKING_PIXEL_RE = re.compile(
    r'<img[^>]*'
    r'(?:'
    r'(?:width\s*=\s*["\']?\s*[01]\s*["\']?.*?height\s*=\s*["\']?\s*[01]\s*["\']?)'
    r'|'
    r'(?:height\s*=\s*["\']?\s*[01]\s*["\']?.*?width\s*=\s*["\']?\s*[01]\s*["\']?)'
    r')'
    r'[^>]*>',
    re.IGNORECASE,
)

_TRACKING_DOMAINS = [
    "mailtrack.io", "mailchimp.com", "sendgrid.net", "hubspot.com",
    "litmus.com", "returnpath.net", "sailthru.com", "exacttarget.com",
    "click.email", "track.", "pixel.", "beacon.", "open.",
]

_TRACKING_URL_RE = re.compile(
    r'<img[^>]*src\s*=\s*["\']([^"\']*(?:'
    + "|".join(re.escape(d) for d in _TRACKING_DOMAINS)
    + r')[^"\']*)["\'][^>]*>',
    re.IGNORECASE,
)


def strip_tracking_pixels(html: str) -> str:
    """Remove tracking pixels from HTML email content."""
    html = _TRACKING_PIXEL_RE.sub("", html)
    html = _TRACKING_URL_RE.sub("", html)
    return html


# ---------------------------------------------------------------------------
# HTML to text conversion
# ---------------------------------------------------------------------------

def html_to_text(html: str) -> str:
    """Convert HTML email to plain text suitable for LLM consumption."""
    html = strip_tracking_pixels(html)
    text = re.sub(r"<br\s*/?\s*>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"</?(?:p|div|tr|li|h[1-6])[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(
        r'<a\s+[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        r"\2 (\1)", text, flags=re.IGNORECASE,
    )
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Content sanitization
# ---------------------------------------------------------------------------

def sanitize_subject(subject: str) -> str:
    """Sanitize an email subject line."""
    if not subject:
        return "(no subject)"
    subject = unicodedata.normalize("NFKC", subject)
    return subject[:MAX_SUBJECT]


def sanitize_body(body: str, max_length: int = MAX_EMAIL_BODY) -> str:
    """Sanitize email body content for LLM consumption."""
    if not body:
        return ""
    body = unicodedata.normalize("NFKC", body)
    # Decode HTML entities so tracking pixel regex can match encoded tags
    import html as _html
    body = _html.unescape(body)
    body = strip_tracking_pixels(body)
    return body[:max_length]


def sanitize_filename(name: str) -> str:
    """Sanitize an attachment filename."""
    if not name:
        return "file"
    name = name[:MAX_ATTACHMENT_FILENAME]
    name = name.replace("/", "_").replace("\\", "_").replace("..", "_")
    name = name.replace("\n", "").replace("\r", "")
    return name


def truncate_bulk(text: str, max_length: int = MAX_BULK_CHARS) -> str:
    """Truncate large email batches for LLM consumption."""
    if len(text) <= max_length:
        return text
    suffix = "\n[... truncated for safety ...]"
    return text[: max_length - len(suffix)] + suffix
