## gmail_read

Read emails from your Gmail inbox, retrieve specific messages by ID, or list available labels. Use this tool to check new mail, read full message content, or discover label organization.

**Arguments:**
- **action** (string, required): The read operation to perform. One of `inbox`, `read`, or `labels`.
  - `inbox` — Fetch recent messages from the inbox.
  - `read` — Read a specific message by ID.
  - `labels` — List all available Gmail labels.
- **message_id** (string, optional): The Gmail message ID to read. Required when `action` is `read`.
- **label** (string, optional): Filter inbox results by a specific label name (e.g., `INBOX`, `IMPORTANT`, `STARRED`).
- **limit** (integer, optional): Maximum number of messages to return. Defaults to 10.
- **query** (string, optional): Gmail search query to filter inbox results (e.g., `is:unread`, `from:boss@company.com`).

**Examples:**

Fetch the 5 most recent inbox messages:
~~~json
{
  "action": "inbox",
  "limit": 5
}
~~~

Read a specific message by ID:
~~~json
{
  "action": "read",
  "message_id": "18f3a4b2c1d0e5f6"
}
~~~

List unread messages with a specific label:
~~~json
{
  "action": "inbox",
  "label": "IMPORTANT",
  "query": "is:unread",
  "limit": 20
}
~~~

List all available labels:
~~~json
{
  "action": "labels"
}
~~~
