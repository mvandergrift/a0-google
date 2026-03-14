## drive_share

Share a Google Drive file or folder with specific users or enable link sharing. Control access levels with role-based permissions.

**Arguments:**
- **file_id** (string, required): The Drive file or folder ID to share.
- **email** (string, optional): Email address of the user to share with. Required for user-level sharing.
- **role** (string, optional): Permission role to grant. One of `reader`, `commenter`, or `writer`. Defaults to `reader`.
- **link_sharing** (boolean, optional): When `true`, enable "anyone with the link" sharing. When `false`, disable link sharing. Defaults to `false`.

**Examples:**

Share a file with a specific user as a reader:
~~~json
{
  "file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345",
  "email": "colleague@company.com",
  "role": "reader"
}
~~~

Share a file with write access:
~~~json
{
  "file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345",
  "email": "editor@company.com",
  "role": "writer"
}
~~~

Enable link sharing for anyone:
~~~json
{
  "file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345",
  "link_sharing": true,
  "role": "reader"
}
~~~

Share with commenter access:
~~~json
{
  "file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345",
  "email": "reviewer@company.com",
  "role": "commenter"
}
~~~
