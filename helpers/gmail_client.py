"""Gmail API client wrapper.

Handles email parsing (MIME -> readable text), attachment handling,
thread reconstruction, and message composition. Auth is delegated
to the shared google_auth module.
"""

import base64
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from plugins.google.helpers.google_auth import (
    get_google_config, get_credentials, build_service,
    GoogleAuthError, GoogleAPIError,
)


def get_gmail_service(config: dict):
    """Get an authenticated Gmail API service."""
    return build_service("gmail", config)


# ---------------------------------------------------------------------------
# Email Parsing
# ---------------------------------------------------------------------------

def parse_message(msg: dict) -> dict:
    """Parse a Gmail API message into a readable dict."""
    headers = {}
    for h in msg.get("payload", {}).get("headers", []):
        name = h["name"].lower()
        if name in ("subject", "from", "to", "cc", "bcc", "date", "message-id"):
            headers[name] = h["value"]

    body = _extract_body(msg.get("payload", {}))
    attachments = _extract_attachments(msg.get("payload", {}))

    return {
        "id": msg.get("id", ""),
        "thread_id": msg.get("threadId", ""),
        "subject": headers.get("subject", "(no subject)"),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "date": headers.get("date", ""),
        "snippet": msg.get("snippet", ""),
        "body": body,
        "labels": msg.get("labelIds", []),
        "attachments": attachments,
    }


def _extract_body(payload: dict) -> str:
    """Extract plain text body from a MIME payload, preferring text/plain."""
    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    parts = payload.get("parts", [])
    if parts:
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

        for part in parts:
            if part.get("mimeType") == "text/html":
                data = part.get("body", {}).get("data", "")
                if data:
                    html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                    return _html_to_text(html)

        for part in parts:
            result = _extract_body(part)
            if result:
                return result

    if mime_type == "text/html":
        data = payload.get("body", {}).get("data", "")
        if data:
            html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
            return _html_to_text(html)

    return ""


def _html_to_text(html: str) -> str:
    """Basic HTML to plain text conversion with tracking pixel removal."""
    from plugins.google.helpers.sanitize import strip_tracking_pixels, html_to_text
    return html_to_text(strip_tracking_pixels(html))


def _extract_attachments(payload: dict) -> list[dict]:
    """Extract attachment metadata from a MIME payload."""
    attachments = []
    parts = payload.get("parts", [])
    for part in parts:
        filename = part.get("filename", "")
        if filename:
            attachments.append({
                "filename": filename,
                "mime_type": part.get("mimeType", ""),
                "size": part.get("body", {}).get("size", 0),
                "attachment_id": part.get("body", {}).get("attachmentId", ""),
            })
        attachments.extend(_extract_attachments(part))
    return attachments


# ---------------------------------------------------------------------------
# Email Formatting for LLM
# ---------------------------------------------------------------------------

def format_email(parsed: dict, include_body: bool = True, max_body: int = 4000) -> str:
    """Format a parsed email for LLM consumption."""
    lines = [
        f"From: {parsed['from']}",
        f"To: {parsed['to']}",
    ]
    if parsed.get("cc"):
        lines.append(f"CC: {parsed['cc']}")
    lines.extend([
        f"Date: {parsed['date']}",
        f"Subject: {parsed['subject']}",
    ])
    if parsed["attachments"]:
        att_names = [a["filename"] for a in parsed["attachments"]]
        lines.append(f"Attachments: {', '.join(att_names)}")
    lines.append(f"Labels: {', '.join(parsed['labels'])}")

    if include_body:
        body = parsed["body"]
        if len(body) > max_body:
            body = body[:max_body] + f"\n\n... [truncated — {len(parsed['body']):,} chars total]"
        lines.append(f"\n{body}")

    return "\n".join(lines)


def format_email_list(emails: list[dict]) -> str:
    """Format a list of parsed emails as a summary table."""
    if not emails:
        return "No emails found."
    lines = []
    for i, em in enumerate(emails, 1):
        labels = ", ".join(em.get("labels", []))
        att = f" [{len(em['attachments'])} attachment(s)]" if em.get("attachments") else ""
        lines.append(
            f"{i}. [{em['date']}] {em['from']}\n"
            f"   Subject: {em['subject']}{att}\n"
            f"   ID: {em['id']} | Labels: {labels}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Message Composition
# ---------------------------------------------------------------------------

def create_message(
    to: str, subject: str, body: str,
    cc: str = "", bcc: str = "",
    reply_to_id: str = "",
    thread_id: str = "",
) -> dict:
    """Create a Gmail API message payload."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["to"] = to
    msg["subject"] = subject
    if cc:
        msg["cc"] = cc
    if bcc:
        msg["bcc"] = bcc
    if reply_to_id:
        msg["In-Reply-To"] = reply_to_id
        msg["References"] = reply_to_id

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    payload = {"raw": raw}
    if thread_id:
        payload["threadId"] = thread_id
    return payload


def create_message_with_attachments(
    to: str, subject: str, body: str,
    attachment_paths: list[str],
    cc: str = "", bcc: str = "",
) -> dict:
    """Create a Gmail API message with file attachments."""
    msg = MIMEMultipart()
    msg["to"] = to
    msg["subject"] = subject
    if cc:
        msg["cc"] = cc
    if bcc:
        msg["bcc"] = bcc

    msg.attach(MIMEText(body, "plain", "utf-8"))

    for path_str in attachment_paths:
        path = Path(path_str)
        if not path.exists():
            continue
        part = MIMEBase("application", "octet-stream")
        with open(path, "rb") as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", "attachment",
            filename=path.name,
        )
        msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    return {"raw": raw}
