## gmail_summarize

Generate AI-powered summaries of email messages or threads. Quickly understand the key points of lengthy emails or entire conversation threads without reading every message.

**Arguments:**
- **message_id** (string, optional): The Gmail message ID to summarize. Use for a single message summary.
- **thread_id** (string, optional): The Gmail thread ID to summarize. Summarizes the entire conversation thread.
- **query** (string, optional): Search query to find and summarize matching messages. Returns summaries of the top results.
- **limit** (integer, optional): Maximum number of messages to include when using `query`. Defaults to 5.

**Examples:**

Summarize a single message:
~~~json
{
  "message_id": "18f3a4b2c1d0e5f6"
}
~~~

Summarize an entire email thread:
~~~json
{
  "thread_id": "18f3a4b2c1d0e000"
}
~~~

Summarize recent messages matching a query:
~~~json
{
  "query": "project alpha status update",
  "limit": 10
}
~~~
