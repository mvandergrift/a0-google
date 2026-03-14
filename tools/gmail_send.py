from helpers.tool import Tool, Response
from plugins.google.helpers.google_auth import (
    get_google_config, build_service, GoogleAuthError, GoogleAPIError,
)
from plugins.google.helpers.gmail_client import (
    parse_message, create_message, create_message_with_attachments,
)
from plugins.google.helpers.sanitize import (
    validate_recipients, sanitize_subject, sanitize_body,
)


class GmailSend(Tool):
    """Compose and send an email via Gmail, with optional attachments and reply threading."""

    async def execute(self, **kwargs) -> Response:
        from plugins.google.helpers.google_auth import is_service_enabled
        if not is_service_enabled("gmail", self.agent):
            return Response(
                message="Gmail service is disabled. Enable it in Google Suite plugin settings.",
                break_loop=False,
            )

        to = self.args.get("to", "")
        subject = self.args.get("subject", "")
        body = self.args.get("body", "")
        cc = self.args.get("cc", "")
        bcc = self.args.get("bcc", "")
        reply_to_id = self.args.get("reply_to_id", "")
        attachments = self.args.get("attachments", "")

        # --- Validate required fields ---
        if not to:
            return Response(
                message="Error: 'to' is required. Provide one or more recipient email addresses.",
                break_loop=False,
            )
        if not subject and not reply_to_id:
            return Response(
                message="Error: 'subject' is required for new emails (not replies).",
                break_loop=False,
            )
        if not body:
            return Response(
                message="Error: 'body' is required.",
                break_loop=False,
            )

        # --- Validate all recipients ---
        config = get_google_config(self.agent)
        allowed = config.get("security", {}).get("allowed_recipients", [])

        try:
            validate_recipients(to, allowed=allowed or None)
        except ValueError as e:
            return Response(message=f"Invalid 'to' recipients: {e}", break_loop=False)

        if cc:
            try:
                validate_recipients(cc, allowed=allowed or None)
            except ValueError as e:
                return Response(message=f"Invalid 'cc' recipients: {e}", break_loop=False)

        if bcc:
            try:
                validate_recipients(bcc, allowed=allowed or None)
            except ValueError as e:
                return Response(message=f"Invalid 'bcc' recipients: {e}", break_loop=False)

        # --- Sanitize ---
        subject = sanitize_subject(subject)
        body = sanitize_body(body)

        # --- Authenticate ---
        try:
            service = build_service("gmail", config)
        except GoogleAuthError as e:
            return Response(message=f"Auth error: {e}", break_loop=False)

        try:
            thread_id = ""
            original_message_id_header = ""

            # --- Handle reply threading ---
            if reply_to_id:
                self.set_progress("Fetching original message for reply threading...")
                try:
                    original_msg = (
                        service.users()
                        .messages()
                        .get(userId="me", id=reply_to_id, format="full")
                        .execute()
                    )
                    thread_id = original_msg.get("threadId", "")

                    # Extract the Message-ID header for In-Reply-To
                    for header in original_msg.get("payload", {}).get("headers", []):
                        if header["name"].lower() == "message-id":
                            original_message_id_header = header["value"]
                            break

                    # If no explicit subject, use Re: original subject
                    if not subject:
                        parsed = parse_message(original_msg)
                        orig_subject = parsed.get("subject", "")
                        if orig_subject and not orig_subject.lower().startswith("re:"):
                            subject = f"Re: {orig_subject}"
                        else:
                            subject = orig_subject or "Re:"

                except Exception as e:
                    return Response(
                        message=f"Error fetching original message for reply: {e}",
                        break_loop=False,
                    )

            # --- Build the message ---
            self.set_progress("Sending email...")

            attachment_paths = []
            if attachments:
                attachment_paths = [
                    p.strip() for p in attachments.split(",") if p.strip()
                ]

            if attachment_paths:
                payload = create_message_with_attachments(
                    to=to,
                    subject=subject,
                    body=body,
                    attachment_paths=attachment_paths,
                    cc=cc,
                    bcc=bcc,
                )
            else:
                payload = create_message(
                    to=to,
                    subject=subject,
                    body=body,
                    cc=cc,
                    bcc=bcc,
                    reply_to_id=original_message_id_header,
                    thread_id=thread_id,
                )

            # --- Send ---
            sent = (
                service.users()
                .messages()
                .send(userId="me", body=payload)
                .execute()
            )

            sent_id = sent.get("id", "unknown")
            sent_thread = sent.get("threadId", "")
            att_note = (
                f" with {len(attachment_paths)} attachment(s)"
                if attachment_paths
                else ""
            )
            reply_note = (
                f" (reply in thread {sent_thread})"
                if reply_to_id
                else ""
            )

            return Response(
                message=(
                    f"Email sent successfully{att_note}{reply_note}.\n"
                    f"To: {to}\n"
                    f"Subject: {subject}\n"
                    f"Message ID: {sent_id}"
                ),
                break_loop=True,
            )

        except GoogleAPIError as e:
            return Response(message=f"Gmail API error: {e}", break_loop=False)
        except Exception as e:
            return Response(message=f"Error sending email: {e}", break_loop=False)
