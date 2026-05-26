# Google Suite Plugin — Quick Start

## Prerequisites

- Agent Zero instance (Docker or local)
- A Google account with access to Gmail, Calendar, Drive
- Access to [Google Cloud Console](https://console.cloud.google.com/)

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top and select **New Project**
3. Name it (e.g., "Agent Zero") and click **Create**
4. Wait for the project to be created, then select it

## Step 2: Enable Required APIs

1. Go to **APIs & Services > Library** (or search "API Library" in the console)
2. Enable each of these APIs (search by name, click, then click **Enable**):
   - **Gmail API**
   - **Google Calendar API**
   - **Google Drive API**
   - **People API** (for Contacts)
   - **Tasks API**

> **Note:** You only need to enable APIs for services you plan to use. Gmail, Calendar, and Drive are enabled by default in the plugin. Contacts and Tasks are disabled by default and can be enabled later.

## Step 3: Create OAuth Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth 2.0 Client ID**
3. If prompted to configure a consent screen:
   - Choose **External** (unless you have a Google Workspace org)
   - Fill in the required fields (app name, user support email, developer contact)
   - Add test users (your own Gmail address)
   - Save and continue through all steps
4. Back in Credentials, click **Create Credentials > OAuth 2.0 Client ID**
5. Application type: **Desktop app**
6. Name it (e.g., "Agent Zero Desktop")
7. Click **Create**
8. Click **Download JSON** — this is your `credentials.json`

## Step 4: Install the Plugin

```bash
# Copy to container
docker cp a0-google/ <container>:/tmp/a0-google/

# Install
docker exec <container> bash -c "cd /tmp/a0-google && ./install.sh"

# Restart UI
docker exec <container> supervisorctl restart run_ui
```

Or via the install script:
```bash
./install.sh
```

## Step 5: Upload Credentials

1. Open Agent Zero WebUI
2. Go to **Settings > External Services > Google Suite**
3. Open the **Auth** tab
4. Open your downloaded `credentials.json` in a text editor, copy the contents
5. Paste into the **Credentials JSON** textarea
6. Click **Upload Credentials**
7. Verify the status shows "Credentials uploaded"

## Step 6: Authorize

1. Click **Authorize** (or **Generate Auth URL**)
2. A Google consent URL will appear — open it in your browser
3. Sign in with your Google account
4. Grant the requested permissions (Gmail, Calendar, Drive, etc.)
5. Google will redirect your browser to `http://127.0.0.1:1/?code=...` — the page will fail to load ("This site can't be reached"); this is expected
6. Copy the full URL from your browser's address bar
7. Paste it into the plugin's **Authorization Code** field and click **Submit Code**
8. Verify the status shows **Authenticated** with your email address

## Step 7: Try It

Ask the agent:
- "Read my latest emails"
- "What's on my calendar today?"
- "List my recent Drive files"
- "Schedule a meeting called 'Team Sync' tomorrow at 2pm for 1 hour"
- "Send an email to bob@example.com with subject 'Hello' and body 'Hi Bob'"

## Enabling Additional Services

By default, Gmail, Calendar, and Drive are enabled. To enable Contacts and Tasks:

1. Go to **Settings > External Services > Google Suite**
2. In the config, set `contacts.enabled: true` and/or `tasks.enabled: true`
3. Save the config
4. **Re-authorize** — click Authorize again to request the additional scopes
5. Try: "List my Google contacts" or "Show my task lists"

## Troubleshooting

- **"Not authenticated"**: Complete the OAuth flow (Steps 5-6)
- **"credentials.json not found"**: Upload credentials via the Auth tab
- **"Token refresh failed"**: Re-authorize via the plugin settings
- **"Insufficient authentication scopes"**: You enabled a new service but didn't re-authorize. Click Authorize again to get the new scopes
- **"Calendar times are wrong"**: Check that the `calendar.timezone` setting matches your Google Calendar account timezone. The agent uses the configured timezone for relative time expressions like "tomorrow at 2pm"
- **"Gmail service is disabled"**: Enable the service in plugin config (services.gmail.enabled: true)
- **API quota errors**: Google APIs have daily quotas. Wait and retry, or check your quota in Google Cloud Console
