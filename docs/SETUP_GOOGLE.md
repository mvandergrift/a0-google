# Google Suite Plugin — Google Cloud Setup Guide

Detailed guide for configuring Google Cloud Console for the Google Suite plugin.

## Google Cloud Project

### Creating a Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown > **New Project**
3. Name: `Agent Zero` (or any name you prefer)
4. Organization: Leave as default or select your org
5. Click **Create**

### Selecting the Project

After creation, ensure the project is selected in the top navigation bar dropdown.

## API Enablement

Navigate to **APIs & Services > Library** and enable each API:

| API Name | Search Term | Purpose |
|----------|-------------|---------|
| Gmail API | "Gmail" | Email read, send, search, manage |
| Google Calendar API | "Calendar" | Event CRUD, availability |
| Google Drive API | "Drive" | File list, search, upload, download, share |
| People API | "People" | Contact list, search, create |
| Tasks API | "Tasks" | Task list, create, complete, delete |

Click each API, then click **Enable**. Wait for the "API enabled" confirmation before proceeding.

> **Tip:** You only need to enable APIs for services you'll use. Gmail + Calendar + Drive are the most common. Add People and Tasks later if needed.

## OAuth Consent Screen

Before creating credentials, you must configure the consent screen. The Google Cloud Console uses a left-side menu with: **Overview**, **Branding**, **Audience**, **Clients**, **Data Access**, **Verification Center**, and **Settings**.

1. Go to **APIs & Services > OAuth consent screen**
2. Click **Get Started**
3. On the **Branding** page, fill in:
   - **App name**: `Agent Zero`
   - **User support email**: Your email
   - **Developer contact email**: Your email
4. Click **Save** or **Continue**
5. On the **Audience** page, select **External** (or **Internal** if you have Google Workspace)
6. Click **Save**

### Data Access (Scopes)

Go to the **Data Access** page in the left menu, then click **Add or Remove Scopes** and add:

| Scope | Description |
|-------|-------------|
| `https://www.googleapis.com/auth/gmail.readonly` | Read Gmail messages and labels |
| `https://www.googleapis.com/auth/gmail.send` | Send emails |
| `https://www.googleapis.com/auth/gmail.modify` | Modify messages (archive, label, trash) |
| `https://www.googleapis.com/auth/calendar` | Read/write calendar events |
| `https://www.googleapis.com/auth/calendar.events` | Manage calendar events |
| `https://www.googleapis.com/auth/drive.file` | Access files created by the app |
| `https://www.googleapis.com/auth/drive.readonly` | Read-only access to all Drive files |
| `https://www.googleapis.com/auth/contacts.readonly` | Read contacts |
| `https://www.googleapis.com/auth/contacts` | Read/write contacts |
| `https://www.googleapis.com/auth/tasks` | Read/write tasks |

> **Note:** The plugin dynamically requests only the scopes for enabled services. You don't need to add scopes for disabled services.

Click **Save**.

### Test Users

If you selected **External** audience:
1. Go back to the **Audience** page
2. Under **Test users**, click **Add Users**
3. Add your Google account email
4. Click **Save**

> **Important:** External apps in "Testing" mode are limited to test users only. For personal use, this is fine. For production, you'd need to publish the app.

## OAuth 2.0 Credentials

1. Go to the **Clients** page in the left menu (or **APIs & Services > Credentials**)
2. Click **Create Client** (or **Create Credentials > OAuth 2.0 Client ID**)
3. Application type: **Desktop app**
4. Name: `Agent Zero Desktop` (any name)
5. Click **Create**

### Download credentials.json

After creation, you'll see a dialog with your client ID and secret:
- Click **Download JSON**
- Save as `credentials.json`
- This file contains your `client_id` and `client_secret`

> **Security:** Keep `credentials.json` private. Never commit it to git. The plugin's `.gitignore` excludes it by default.

### credentials.json Structure

The file should look like:
```json
{
  "installed": {
    "client_id": "123456789-abc.apps.googleusercontent.com",
    "project_id": "your-project-name",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-...",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
  }
}
```

The key `"installed"` indicates a Desktop app type. The plugin also supports `"web"` type for web application credentials.

## Service-Specific Notes

### Gmail

- **gmail.readonly** — Required for reading emails, listing labels, searching
- **gmail.send** — Required for sending emails and creating drafts
- **gmail.modify** — Required for archiving, trashing, starring, and label management
- The plugin sanitizes email content before feeding it to the LLM (tracking pixel removal, HTML-to-text conversion)

### Calendar

- **calendar** + **calendar.events** — Full access to events
- The plugin uses the configured timezone (default: `America/New_York`) for natural language date parsing
- Make sure your Google Calendar account timezone matches the plugin timezone setting for accurate "tomorrow at 2pm" type expressions

### Drive

- **drive.file** — Access to files created/opened by the app
- **drive.readonly** — Read-only access to list and search all files
- Downloads are restricted to safe directories (`/a0/usr/workdir`, `/a0/usr/files`, `/tmp`)
- Uploads are blocked from sensitive directories (`/a0/usr/plugins`, `/etc`, `/root`)
- Google Docs/Sheets/Slides are automatically exported as PDF when downloaded

### Contacts (People API)

- **contacts.readonly** — Read-only access to contacts
- **contacts** — Full access to create/update contacts
- Disabled by default; enable in config (`services.contacts.enabled: true`)
- Requires re-authorization after enabling to get the new scopes

### Tasks

- **tasks** — Full access to task lists and tasks
- Disabled by default; enable in config (`services.tasks.enabled: true`)
- Requires re-authorization after enabling to get the new scopes

## Token Management

### token.json

After successful authorization, the plugin creates `token.json` in the data directory:
- Stored with `0o600` permissions (owner-only read/write)
- Written atomically (temp file + rename) to prevent corruption
- Contains refresh token + access token + scopes + expiry

### Token Refresh

The plugin automatically refreshes expired access tokens using the refresh token. No user action required unless:
- The refresh token is revoked (re-authorize)
- New scopes are needed (re-authorize)
- The Google Cloud project is deleted

### Revoking Access

To revoke the plugin's access to your Google account:
1. Go to [myaccount.google.com/permissions](https://myaccount.google.com/permissions)
2. Find "Agent Zero" (or your app name)
3. Click **Remove Access**
4. The plugin will need to be re-authorized

## Security Considerations

- **Least privilege**: Only enable services you need. Disabled services don't request scopes.
- **Recipient allow-list**: Configure `security.allowed_recipients` to restrict email sending to approved addresses.
- **Test users**: Keep your OAuth app in "Testing" mode to limit who can authorize.
- **Credential rotation**: Periodically delete and recreate OAuth credentials in Google Cloud Console.
- **Token storage**: token.json is stored with 0o600 permissions and never committed to git.
