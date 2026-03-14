## gmail_send

Send emails via Gmail. Supports composing new messages, replying to existing threads, adding CC/BCC recipients, and including file attachments.

**Arguments:**
- **to** (string, required): Recipient email address or comma-separated list of addresses.
- **subject** (string, required): Email subject line.
- **body** (string, required): Email body content. Supports plain text.
- **cc** (string, optional): CC recipient email address or comma-separated list.
- **bcc** (string, optional): BCC recipient email address or comma-separated list.
- **reply_to_id** (string, optional): Message ID to reply to. When provided, the email is sent as a reply within the existing thread.
- **attachments** (list of strings, optional): List of file paths to attach to the email.

**Examples:**

Send a simple email:
~~~json
{
  "to": "colleague@company.com",
  "subject": "Meeting notes",
  "body": "Here are the notes from today's standup meeting..."
}
~~~

Reply to an existing message:
~~~json
{
  "to": "colleague@company.com",
  "subject": "Re: Meeting notes",
  "body": "Thanks for sharing. I have a few additions...",
  "reply_to_id": "18f3a4b2c1d0e5f6"
}
~~~

Send with CC, BCC, and attachments:
~~~json
{
  "to": "team-lead@company.com",
  "subject": "Q4 Report",
  "body": "Please find the Q4 report attached.",
  "cc": "manager@company.com,director@company.com",
  "bcc": "archive@company.com",
  "attachments": ["/tmp/q4_report.pdf"]
}
~~~
