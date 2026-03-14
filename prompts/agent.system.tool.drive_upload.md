## drive_upload

Upload a local file to Google Drive. Optionally specify a destination folder, custom name, and description.

**Arguments:**
- **file_path** (string, required): Absolute path to the local file to upload.
- **name** (string, optional): Name for the file in Drive. Defaults to the local filename.
- **folder_id** (string, optional): ID of the destination folder in Drive. Defaults to the root folder.
- **description** (string, optional): Description to attach to the file in Drive.

**Examples:**

Upload a file to the root of Drive:
~~~json
{
  "file_path": "/tmp/report.pdf"
}
~~~

Upload with a custom name and description:
~~~json
{
  "file_path": "/tmp/data_export.csv",
  "name": "Q1 Sales Data.csv",
  "description": "Sales data export for Q1 2026"
}
~~~

Upload to a specific folder:
~~~json
{
  "file_path": "/tmp/presentation.pptx",
  "name": "Team Offsite Deck.pptx",
  "folder_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345"
}
~~~
