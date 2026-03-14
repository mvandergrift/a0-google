## gmail_manage

Manage Gmail messages by archiving, trashing, labeling, or changing read status. Perform organizational actions on individual messages.

**Arguments:**
- **message_id** (string, required): The Gmail message ID to act on.
- **action** (string, required): The management action to perform. One of:
  - `archive` — Remove the message from the inbox (removes INBOX label).
  - `trash` — Move the message to trash.
  - `untrash` — Restore a message from trash.
  - `label` — Add a label to the message.
  - `remove_label` — Remove a label from the message.
  - `mark_read` — Mark the message as read.
  - `mark_unread` — Mark the message as unread.
- **label_name** (string, optional): The label name to add or remove. Required when `action` is `label` or `remove_label`.

**Examples:**

Archive a message:
~~~json
{
  "message_id": "18f3a4b2c1d0e5f6",
  "action": "archive"
}
~~~

Add a label to a message:
~~~json
{
  "message_id": "18f3a4b2c1d0e5f6",
  "action": "label",
  "label_name": "Projects/Website-Redesign"
}
~~~

Mark a message as unread:
~~~json
{
  "message_id": "18f3a4b2c1d0e5f6",
  "action": "mark_unread"
}
~~~

Move a message to trash:
~~~json
{
  "message_id": "18f3a4b2c1d0e5f6",
  "action": "trash"
}
~~~
