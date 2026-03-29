from helpers.tool import Tool, Response
from usr.plugins.google.helpers.google_auth import (
    get_google_config, build_service, GoogleAuthError, GoogleAPIError,
)
from usr.plugins.google.helpers.gmail_client import (
    parse_message, format_email_list,
)
from usr.plugins.google.helpers.sanitize import sanitize_body


class GmailSearch(Tool):
    """Search Gmail with query, date filters, sender, and attachment filters."""

    async def execute(self, **kwargs) -> Response:
        from usr.plugins.google.helpers.google_auth import is_service_enabled
        if not is_service_enabled("gmail", self.agent):
            return Response(
                message="Gmail service is disabled. Enable it in Google Suite plugin settings.",
                break_loop=False,
            )

        query = self.args.get("query", "")
        after_date = self.args.get("after_date", "")
        before_date = self.args.get("before_date", "")
        from_addr = self.args.get("from_addr", "")
        has_attachment = self.args.get("has_attachment", "")
        limit = min(int(self.args.get("limit", "20")), 100)

        # Build the Gmail query string
        query_parts = []
        if query:
            query_parts.append(query)
        if after_date:
            query_parts.append(f"after:{after_date}")
        if before_date:
            query_parts.append(f"before:{before_date}")
        if from_addr:
            query_parts.append(f"from:{from_addr}")
        if has_attachment and has_attachment.lower() in ("true", "yes", "1"):
            query_parts.append("has:attachment")

        gmail_query = " ".join(query_parts)
        if not gmail_query:
            return Response(
                message=(
                    "Error: At least one search parameter is required. "
                    "Provide query, after_date, before_date, from_addr, or has_attachment."
                ),
                break_loop=False,
            )

        config = get_google_config(self.agent)
        try:
            service = build_service("gmail", config)
        except GoogleAuthError as e:
            return Response(message=f"Auth error: {e}", break_loop=False)

        try:
            self.set_progress(f"Searching: {gmail_query}")

            results = (
                service.users()
                .messages()
                .list(userId="me", q=gmail_query, maxResults=limit)
                .execute()
            )

            message_refs = results.get("messages", [])
            if not message_refs:
                return Response(
                    message=f"No emails found matching: {gmail_query}",
                    break_loop=False,
                )

            total_estimate = results.get("resultSizeEstimate", len(message_refs))
            self.set_progress(f"Parsing {len(message_refs)} result(s)...")

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
            header = (
                f"Search results for '{gmail_query}' "
                f"({len(parsed_emails)} of ~{total_estimate} matches):"
            )

            return Response(message=f"{header}\n\n{result_text}", break_loop=False)

        except GoogleAPIError as e:
            return Response(message=f"Gmail API error: {e}", break_loop=False)
        except Exception as e:
            return Response(message=f"Error searching Gmail: {e}", break_loop=False)
