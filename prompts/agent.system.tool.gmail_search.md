## gmail_search

Search Gmail messages using queries, date ranges, sender filters, and attachment filters. Returns matching messages sorted by date.

**Arguments:**
- **query** (string, required): Search query string. Supports Gmail search syntax (e.g., `project update`, `subject:invoice`, `has:attachment filename:pdf`).
- **limit** (integer, optional): Maximum number of results to return. Defaults to 10.
- **after_date** (string, optional): Only return messages after this date. Format: `YYYY-MM-DD`.
- **before_date** (string, optional): Only return messages before this date. Format: `YYYY-MM-DD`.
- **from_addr** (string, optional): Filter by sender email address.
- **has_attachment** (boolean, optional): When `true`, only return messages that have attachments.

**Examples:**

Search for messages containing a keyword:
~~~json
{
  "query": "quarterly report",
  "limit": 5
}
~~~

Search within a date range from a specific sender:
~~~json
{
  "query": "invoice",
  "from_addr": "billing@vendor.com",
  "after_date": "2026-01-01",
  "before_date": "2026-03-01"
}
~~~

Find messages with attachments:
~~~json
{
  "query": "contract",
  "has_attachment": true,
  "limit": 20
}
~~~

Search for recent messages from a sender:
~~~json
{
  "query": "",
  "from_addr": "ceo@company.com",
  "after_date": "2026-03-01",
  "limit": 10
}
~~~
