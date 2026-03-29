from helpers.tool import Tool, Response
from usr.plugins.google.helpers.google_auth import (
    get_google_config, build_service, GoogleAuthError, GoogleAPIError,
)
from usr.plugins.google.helpers.gmail_client import (
    parse_message, create_message, format_email_list,
)
from usr.plugins.google.helpers.sanitize import (
    validate_recipients, sanitize_subject, sanitize_body,
)

VALID_ACTIONS = ("create", "list", "send", "delete")


class GmailDraft(Tool):
    """Manage Gmail drafts: create, list, send, or delete drafts."""

    async def execute(self, **kwargs) -> Response:
        from usr.plugins.google.helpers.google_auth import is_service_enabled
        if not is_service_enabled("gmail", self.agent):
            return Response(
                message="Gmail service is disabled. Enable it in Google Suite plugin settings.",
                break_loop=False,
            )

        action = self.args.get("action", "create")

        config = get_google_config(self.agent)
        try:
            service = build_service("gmail", config)
        except GoogleAuthError as e:
            return Response(message=f"Auth error: {e}", break_loop=False)

        try:
            if action == "create":
                return await self._create_draft(service)
            elif action == "list":
                return await self._list_drafts(service)
            elif action == "send":
                return await self._send_draft(service)
            elif action == "delete":
                return await self._delete_draft(service)
            else:
                return Response(
                    message=(
                        f"Unknown action '{action}'. "
                        f"Use one of: {', '.join(VALID_ACTIONS)}."
                    ),
                    break_loop=False,
                )

        except GoogleAPIError as e:
            return Response(message=f"Gmail API error: {e}", break_loop=False)
        except Exception as e:
            return Response(message=f"Error managing drafts: {e}", break_loop=False)

    # ------------------------------------------------------------------
    # Create a draft
    # ------------------------------------------------------------------

    async def _create_draft(self, service) -> Response:
        """Create a new email draft."""
        to = self.args.get("to", "")
        subject = self.args.get("subject", "")
        body = self.args.get("body", "")
        cc = self.args.get("cc", "")
        bcc = self.args.get("bcc", "")

        if not to:
            return Response(
                message="Error: 'to' is required to create a draft.",
                break_loop=False,
            )
        if not subject:
            return Response(
                message="Error: 'subject' is required to create a draft.",
                break_loop=False,
            )
        if not body:
            return Response(
                message="Error: 'body' is required to create a draft.",
                break_loop=False,
            )

        # Validate recipients (enforce allow-list if configured)
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

        # Sanitize
        subject = sanitize_subject(subject)
        body = sanitize_body(body)

        self.set_progress("Creating draft...")
        message_payload = create_message(
            to=to,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc,
        )

        draft = (
            service.users()
            .drafts()
            .create(userId="me", body={"message": message_payload})
            .execute()
        )

        draft_id = draft.get("id", "unknown")
        msg_id = draft.get("message", {}).get("id", "unknown")

        return Response(
            message=(
                f"Draft created successfully.\n"
                f"Draft ID: {draft_id}\n"
                f"Message ID: {msg_id}\n"
                f"To: {to}\n"
                f"Subject: {subject}"
            ),
            break_loop=True,
        )

    # ------------------------------------------------------------------
    # List drafts
    # ------------------------------------------------------------------

    async def _list_drafts(self, service) -> Response:
        """List existing email drafts."""
        limit = min(int(self.args.get("limit", "20")), 100)

        self.set_progress("Fetching drafts...")
        results = (
            service.users()
            .drafts()
            .list(userId="me", maxResults=limit)
            .execute()
        )

        draft_refs = results.get("drafts", [])
        if not draft_refs:
            return Response(message="No drafts found.", break_loop=False)

        self.set_progress(f"Parsing {len(draft_refs)} draft(s)...")
        parsed_drafts = []
        for ref in draft_refs:
            draft = (
                service.users()
                .drafts()
                .get(userId="me", id=ref["id"], format="full")
                .execute()
            )
            msg = draft.get("message", {})
            parsed = parse_message(msg)
            parsed["draft_id"] = draft.get("id", "")
            parsed_drafts.append(parsed)

        lines = [f"Drafts ({len(parsed_drafts)}):"]
        for i, d in enumerate(parsed_drafts, 1):
            att = f" [{len(d['attachments'])} attachment(s)]" if d.get("attachments") else ""
            lines.append(
                f"{i}. To: {d['to']}\n"
                f"   Subject: {d['subject']}{att}\n"
                f"   Draft ID: {d['draft_id']} | Message ID: {d['id']}"
            )

        return Response(message="\n".join(lines), break_loop=False)

    # ------------------------------------------------------------------
    # Send a draft
    # ------------------------------------------------------------------

    async def _send_draft(self, service) -> Response:
        """Send an existing draft."""
        draft_id = self.args.get("draft_id", "")
        if not draft_id:
            return Response(
                message="Error: draft_id is required to send a draft.",
                break_loop=False,
            )

        self.set_progress("Sending draft...")
        sent = (
            service.users()
            .drafts()
            .send(userId="me", body={"id": draft_id})
            .execute()
        )

        sent_id = sent.get("id", "unknown")
        thread_id = sent.get("threadId", "")

        # Try to get subject for confirmation
        subject = ""
        try:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=sent_id, format="metadata",
                     metadataHeaders=["Subject", "To"])
                .execute()
            )
            for header in msg.get("payload", {}).get("headers", []):
                if header["name"].lower() == "subject":
                    subject = header["value"]
        except Exception:
            pass

        subject_note = f"\nSubject: {subject}" if subject else ""
        return Response(
            message=(
                f"Draft sent successfully.\n"
                f"Message ID: {sent_id}\n"
                f"Thread ID: {thread_id}"
                f"{subject_note}"
            ),
            break_loop=True,
        )

    # ------------------------------------------------------------------
    # Delete a draft
    # ------------------------------------------------------------------

    async def _delete_draft(self, service) -> Response:
        """Delete a draft permanently."""
        draft_id = self.args.get("draft_id", "")
        if not draft_id:
            return Response(
                message="Error: draft_id is required to delete a draft.",
                break_loop=False,
            )

        self.set_progress("Deleting draft...")
        service.users().drafts().delete(
            userId="me", id=draft_id,
        ).execute()

        return Response(
            message=f"Draft {draft_id} deleted permanently.",
            break_loop=True,
        )
