## gmail_draft

Manage Gmail drafts. Create new drafts for later editing, list existing drafts, send a draft, or delete drafts that are no longer needed.

**Arguments:**
- **action** (string, required): The draft operation to perform. One of `create`, `list`, `send`, or `delete`.
  - `create` — Create a new draft email.
  - `list` — List all existing drafts.
  - `send` — Send an existing draft immediately.
  - `delete` — Permanently delete a draft.
- **to** (string, optional): Recipient email address. Required when `action` is `create`.
- **subject** (string, optional): Email subject line. Required when `action` is `create`.
- **body** (string, optional): Email body content. Required when `action` is `create`.
- **draft_id** (string, optional): The draft ID to act on. Required when `action` is `send` or `delete`.

**Examples:**

Create a new draft:
~~~json
{
  "action": "create",
  "to": "partner@company.com",
  "subject": "Partnership proposal",
  "body": "I wanted to discuss a potential partnership opportunity..."
}
~~~

List all drafts:
~~~json
{
  "action": "list"
}
~~~

Send an existing draft:
~~~json
{
  "action": "send",
  "draft_id": "r8293847561"
}
~~~

Delete a draft:
~~~json
{
  "action": "delete",
  "draft_id": "r8293847561"
}
~~~
