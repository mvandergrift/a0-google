## drive_download

Download a file from Google Drive to the local filesystem. Google Workspace files (Docs, Sheets, Slides) are automatically exported to compatible formats.

**Arguments:**
- **file_id** (string, required): The Drive file ID to download.
- **local_path** (string, optional): Local filesystem path to save the file to. If omitted, the file is saved to a temporary directory using its original name.

**Examples:**

Download a file to a specific location:
~~~json
{
  "file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345",
  "local_path": "/tmp/downloaded_report.pdf"
}
~~~

Download a file using its default name:
~~~json
{
  "file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345"
}
~~~
