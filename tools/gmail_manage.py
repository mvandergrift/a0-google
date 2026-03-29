from helpers.tool import Tool, Response
from usr.plugins.google.helpers.google_auth import (
    get_google_config, build_service, GoogleAuthError, GoogleAPIError,
)

VALID_ACTIONS = (
    "archive", "trash", "untrash",
    "mark_read", "mark_unread",
    "label", "remove_label",
)


class GmailManage(Tool):
    """Manage Gmail messages: archive, trash, mark read/unread, add/remove labels."""

    async def execute(self, **kwargs) -> Response:
        from usr.plugins.google.helpers.google_auth import is_service_enabled
        if not is_service_enabled("gmail", self.agent):
            return Response(
                message="Gmail service is disabled. Enable it in Google Suite plugin settings.",
                break_loop=False,
            )

        action = self.args.get("action", "")
        message_id = self.args.get("message_id", "")

        if not action:
            return Response(
                message=(
                    "Error: action is required. "
                    f"Use one of: {', '.join(VALID_ACTIONS)}."
                ),
                break_loop=False,
            )

        if action not in VALID_ACTIONS:
            return Response(
                message=(
                    f"Unknown action '{action}'. "
                    f"Use one of: {', '.join(VALID_ACTIONS)}."
                ),
                break_loop=False,
            )

        if not message_id:
            return Response(
                message="Error: message_id is required.",
                break_loop=False,
            )

        config = get_google_config(self.agent)
        try:
            service = build_service("gmail", config)
        except GoogleAuthError as e:
            return Response(message=f"Auth error: {e}", break_loop=False)

        try:
            if action == "archive":
                return await self._archive(service, message_id)
            elif action == "trash":
                return await self._trash(service, message_id)
            elif action == "untrash":
                return await self._untrash(service, message_id)
            elif action == "mark_read":
                return await self._mark_read(service, message_id)
            elif action == "mark_unread":
                return await self._mark_unread(service, message_id)
            elif action == "label":
                return await self._add_label(service, message_id)
            elif action == "remove_label":
                return await self._remove_label(service, message_id)
            else:
                return Response(
                    message=f"Unhandled action '{action}'.",
                    break_loop=False,
                )

        except GoogleAPIError as e:
            return Response(message=f"Gmail API error: {e}", break_loop=False)
        except Exception as e:
            return Response(message=f"Error managing message: {e}", break_loop=False)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    async def _archive(self, service, message_id: str) -> Response:
        """Archive a message by removing the INBOX label."""
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"removeLabelIds": ["INBOX"]},
        ).execute()
        return Response(
            message=f"Message {message_id} archived (removed from INBOX).",
            break_loop=True,
        )

    async def _trash(self, service, message_id: str) -> Response:
        """Move a message to trash."""
        service.users().messages().trash(
            userId="me", id=message_id,
        ).execute()
        return Response(
            message=f"Message {message_id} moved to trash.",
            break_loop=True,
        )

    async def _untrash(self, service, message_id: str) -> Response:
        """Remove a message from trash."""
        service.users().messages().untrash(
            userId="me", id=message_id,
        ).execute()
        return Response(
            message=f"Message {message_id} removed from trash.",
            break_loop=True,
        )

    async def _mark_read(self, service, message_id: str) -> Response:
        """Mark a message as read by removing the UNREAD label."""
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"removeLabelIds": ["UNREAD"]},
        ).execute()
        return Response(
            message=f"Message {message_id} marked as read.",
            break_loop=True,
        )

    async def _mark_unread(self, service, message_id: str) -> Response:
        """Mark a message as unread by adding the UNREAD label."""
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"addLabelIds": ["UNREAD"]},
        ).execute()
        return Response(
            message=f"Message {message_id} marked as unread.",
            break_loop=True,
        )

    async def _add_label(self, service, message_id: str) -> Response:
        """Add a label to a message. Resolves label name to label ID."""
        label_name = self.args.get("label_name", "")
        if not label_name:
            return Response(
                message="Error: label_name is required for the 'label' action.",
                break_loop=False,
            )

        label_id = self._resolve_label_id(service, label_name)
        if label_id is None:
            return Response(
                message=f"Label '{label_name}' not found. Use gmail_read with action 'labels' to see available labels.",
                break_loop=False,
            )

        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"addLabelIds": [label_id]},
        ).execute()
        return Response(
            message=f"Label '{label_name}' added to message {message_id}.",
            break_loop=True,
        )

    async def _remove_label(self, service, message_id: str) -> Response:
        """Remove a label from a message. Resolves label name to label ID."""
        label_name = self.args.get("label_name", "")
        if not label_name:
            return Response(
                message="Error: label_name is required for the 'remove_label' action.",
                break_loop=False,
            )

        label_id = self._resolve_label_id(service, label_name)
        if label_id is None:
            return Response(
                message=f"Label '{label_name}' not found. Use gmail_read with action 'labels' to see available labels.",
                break_loop=False,
            )

        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"removeLabelIds": [label_id]},
        ).execute()
        return Response(
            message=f"Label '{label_name}' removed from message {message_id}.",
            break_loop=True,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_label_id(service, label_name: str) -> str | None:
        """Resolve a human-readable label name to its Gmail label ID.

        Handles both system labels (INBOX, SENT, etc.) and user-created labels.
        Matching is case-insensitive for user labels.
        """
        # System labels have IDs that match their names
        system_labels = {
            "INBOX", "SENT", "DRAFT", "TRASH", "SPAM",
            "STARRED", "IMPORTANT", "UNREAD",
            "CATEGORY_PERSONAL", "CATEGORY_SOCIAL",
            "CATEGORY_PROMOTIONS", "CATEGORY_UPDATES", "CATEGORY_FORUMS",
        }
        upper_name = label_name.upper()
        if upper_name in system_labels:
            return upper_name

        # Fetch all labels and match by name
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        for lbl in labels:
            if lbl["name"].lower() == label_name.lower():
                return lbl["id"]

        return None
