## drive_search

Search for files in Google Drive by name, content, or other properties. Uses Drive's full-text search to find matching files across all accessible locations.

**Arguments:**
- **query** (string, required): Search query string. Matches against file names and content. Supports Drive query syntax (e.g., `name contains 'report'`, `fullText contains 'budget'`).
- **limit** (integer, optional): Maximum number of results to return. Defaults to 25.

**Examples:**

Search for files by keyword:
~~~json
{
  "query": "quarterly report",
  "limit": 10
}
~~~

Search for files with a specific name:
~~~json
{
  "query": "name contains 'meeting notes'",
  "limit": 20
}
~~~

Search for files containing specific text:
~~~json
{
  "query": "fullText contains 'project roadmap'",
  "limit": 5
}
~~~
