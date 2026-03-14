## drive_list

List files and folders in Google Drive. Browse the root directory or a specific folder, with optional filtering by MIME type and sorting.

**Arguments:**
- **folder_id** (string, optional): The ID of the folder to list. Defaults to the root Drive folder (`root`).
- **limit** (integer, optional): Maximum number of files to return. Defaults to 25.
- **mime_type** (string, optional): Filter results by MIME type (e.g., `application/pdf`, `application/vnd.google-apps.spreadsheet`, `image/png`).
- **order_by** (string, optional): Sort order for results (e.g., `modifiedTime desc`, `name`, `createdTime desc`). Defaults to `modifiedTime desc`.

**Examples:**

List the 10 most recently modified files in Drive:
~~~json
{
  "limit": 10
}
~~~

List files in a specific folder:
~~~json
{
  "folder_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345",
  "limit": 50
}
~~~

List only Google Sheets sorted by name:
~~~json
{
  "mime_type": "application/vnd.google-apps.spreadsheet",
  "order_by": "name"
}
~~~

List PDF files in a specific folder:
~~~json
{
  "folder_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345",
  "mime_type": "application/pdf",
  "limit": 20
}
~~~
