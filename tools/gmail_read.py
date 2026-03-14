from helpers.tool import Tool, Response
from plugins.google.helpers.google_auth import (
    get_google_config, build_service, GoogleAuthError, GoogleAPIError,
)
from plugins.google.helpers.gmail_client import (
    parse_message, format_email, format_email_list,
)
from plugins.google.helpers.sanitize import sanitize_body


class GmailRead(Tool):
    """Read emails from Gmail: list inbox, read a specific message, or list labels."""

    async def execute(self, **kwargs) -> Response:
        from plugins.google.helpers.google_auth import is_service_enabled
        if not is_service_enabled("gmail", self.agent):
            return Response(
                message="Gmail service is disabled. Enable it in Google Suite plugin settings.",
                break_loop=False,
            )

        action = self.args.get("action", "inbox")
        config = get_google_config(self.agent)

        try:
            service = build_service("gmail", config)
        except GoogleAuthError as e:
            return Response(message=f"Auth error: {e}", break_loop=False)

        try:
            if action == "inbox":
                return await self._list_inbox(service)
            elif action == "read":
                return await self._read_message(service)
            elif action == "labels":
                return await self._list_labels(service)
            else:
                return Response(
                    message=f"Unknown action '{action}'. Use 'inbox', 'read', or 'labels'.",
                    break_loop=False,
                )
        except GoogleAPIError as e:
            return Response(message=f"Gmail API error: {e}", break_loop=False)
        except Exception as e:
            return Response(message=f"Error reading Gmail: {e}", break_loop=False)

    async def _list_inbox(self, service) -> Response:
        """List emails from inbox with optional filtering."""
        label = self.args.get("label", "INBOX")
        query = self.args.get("query", "")
        limit = min(int(self.args.get("limit", "20")), 100)

        self.set_progress("Fetching emails...")

        label_ids = [label] if label else None
        results = (
            service.users()
            .messages()
            .list(
                userId="me",
                labelIds=label_ids,
                q=query or None,
                maxResults=limit,
            )
            .execute()
        )

        message_refs = results.get("messages", [])
        if not message_refs:
            filter_desc = f" (label: {label})" if label else ""
            filter_desc += f" (query: {query})" if query else ""
            return Response(
                message=f"No emails found{filter_desc}.",
                break_loop=False,
            )

        self.set_progress(f"Parsing {len(message_refs)} email(s)...")
        parsed_emails = []
        for ref in message_refs:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=ref["id"], format="full")
                .execute()
            )
            parsed = parse_message(msg)
            parsed["body"] = sanitize_body(parsed.get("body", ""))
            parsed_emails.append(parsed)

        result_text = format_email_list(parsed_emails)
        total = results.get("resultSizeEstimate", len(message_refs))
        header = f"Inbox ({len(parsed_emails)} of ~{total} emails)"
        if label and label != "INBOX":
            header = f"Label '{label}' ({len(parsed_emails)} emails)"
        if query:
            header += f" | Query: {query}"

        return Response(message=f"{header}:\n\n{result_text}", break_loop=False)

    async def _read_message(self, service) -> Response:
        """Read a specific email by message ID."""
        message_id = self.args.get("message_id", "")
        if not message_id:
            return Response(
                message="Error: message_id is required for the 'read' action.",
                break_loop=False,
            )

        self.set_progress("Fetching message...")
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )

        parsed = parse_message(msg)
        parsed["body"] = sanitize_body(parsed.get("body", ""))
        formatted = format_email(parsed, include_body=True)

        return Response(
            message=f"Email {message_id}:\n\n{formatted}",
            break_loop=False,
        )

    async def _list_labels(self, service) -> Response:
        """List all Gmail labels."""
        self.set_progress("Fetching labels...")
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            return Response(message="No labels found.", break_loop=False)

        system_labels = []
        user_labels = []
        for lbl in labels:
            entry = f"  - {lbl['name']} (ID: {lbl['id']})"
            if lbl.get("type") == "system":
                system_labels.append(entry)
            else:
                user_labels.append(entry)

        lines = [f"Gmail Labels ({len(labels)} total):"]
        if system_labels:
            lines.append("\nSystem Labels:")
            lines.extend(sorted(system_labels))
        if user_labels:
            lines.append("\nUser Labels:")
            lines.extend(sorted(user_labels))

        return Response(message="\n".join(lines), break_loop=False)
