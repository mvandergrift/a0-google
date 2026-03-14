# Human Test Plan: Google Suite Integration

> **Plugin:** `google`
> **Version:** 1.0.0
> **Type:** Productivity (Gmail, Calendar, Drive, Contacts, Tasks)
> **Prerequisite:** `regression_test.sh` passed 100%

---

## How to Use This Plan

1. Work through each phase in order -- phases are gated (don't skip ahead)
2. For each test, perform the **Steps**, check against **Expected**, mark **Result** (Pass/Fail/Skip)
3. Use Claude Code as companion: say "Start human verification for google"
4. Record results in `HUMAN_TEST_RESULTS.md`
5. If any test fails: fix, redeploy, re-test that phase

---

## Phase 0: Prerequisites & Environment

Before starting, confirm:

- [ ] Target container is running: `docker ps | grep agent-zero-dev-latest`
- [ ] WebUI is accessible: `http://localhost:50084`
- [ ] Plugin is enabled (`.toggle-1` exists)
- [ ] `credentials.json` from Google Cloud Console is available
- [ ] A Google account with Gmail, Calendar, Drive, Contacts, Tasks enabled
- [ ] At least one email in the inbox, one calendar event, one Drive file
- [ ] Automated regression passed: `bash tests/regression_test.sh agent-zero-dev-latest 50084`

---

## Phase 1: Plugin Activation & WebUI (6 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-01 | Plugin visible | Open Settings > Plugins | "Google Suite" appears in plugin list | |
| HV-02 | Enable plugin | Toggle plugin on if not already enabled | Plugin enables without error, .toggle-1 created | |
| HV-03 | Main dashboard loads | Click plugin dashboard tab | main.html renders, service cards display (Gmail, Calendar, Drive, Contacts, Tasks) | |
| HV-04 | Service cards display | Inspect dashboard for each service | Each service shows name, icon/indicator, and status (connected/disconnected) | |
| HV-05 | Test connection button | Click "Test Connection" on dashboard | Shows connection status (authenticated or not-authenticated message) | |
| HV-06 | Config page tabs work | Click plugin config tab, navigate sub-tabs if present | Config page loads, all sections (OAuth, services, defaults) render without JS errors | |

---

## Phase 2: OAuth Authentication (7 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-07 | Upload credentials.json | Upload or paste credentials.json content via config page | Config saves, _has_credentials shows true on reload | |
| HV-08 | Credentials detected | Reload config page after uploading credentials | _has_credentials field is true, no error banner | |
| HV-09 | Generate auth URL | Click "Authorize" or generate auth URL button | A Google OAuth consent URL is displayed/opened | |
| HV-10 | Complete OAuth flow | Follow the auth URL, grant permissions, paste authorization code | Authorization succeeds, status changes to "authenticated" | |
| HV-11 | Verify authenticated status | Reload config page | _auth_status shows authenticated, enabled services listed | |
| HV-12 | Test connection after auth | Click "Test Connection" on dashboard | Shows authenticated user email, lists available services | |
| HV-13 | Token.json created | Check container: `docker exec <container> ls /a0/usr/plugins/google/token.json` | token.json file exists | |

---

## Phase 3: Gmail Operations (10 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-14 | Read inbox | Ask agent: "Read my latest emails from Gmail" | Returns list of recent emails with subjects, senders, dates | |
| HV-15 | Read specific email | Ask agent: "Read the email with subject '[known subject]'" | Returns full email body, sender, recipients, date | |
| HV-16 | Search emails | Ask agent: "Search my Gmail for emails from [known sender]" | Returns matching emails filtered by sender | |
| HV-17 | Send email | Ask agent: "Send an email to [test address] with subject 'Test' and body 'Hello from Agent Zero'" | Email is sent, confirmation with message ID returned | |
| HV-18 | Reply to email | Ask agent: "Reply to the last email from [known sender] saying 'Thanks for your message'" | Reply sent in the same thread, visible in Gmail | |
| HV-19 | Manage labels | Ask agent: "List my Gmail labels" | Returns list of labels (Inbox, Sent, Drafts, custom labels) | |
| HV-20 | Archive email | Ask agent: "Archive the latest email in my inbox" | Email removed from inbox, still accessible in All Mail | |
| HV-21 | Create draft | Ask agent: "Create a draft email to [address] with subject 'Draft Test'" | Draft created, visible in Gmail Drafts folder | |
| HV-22 | Summarize thread | Ask agent: "Summarize the email thread with subject '[multi-message thread]'" | Returns coherent summary of the thread conversation | |
| HV-23 | List labels | Ask agent: "Show all my Gmail labels" | Returns complete label list including system and custom labels | |

---

## Phase 4: Calendar Operations (8 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-24 | View today's events | Ask agent: "What's on my calendar today?" | Returns today's events with times, titles, locations | |
| HV-25 | View upcoming | Ask agent: "Show my upcoming calendar events for this week" | Returns events for the current week in chronological order | |
| HV-26 | Create event (natural language) | Ask agent: "Schedule a meeting called 'Test Meeting' tomorrow at 2pm for 1 hour" | Event created on calendar, confirmation with event details | |
| HV-27 | Update event | Ask agent: "Change 'Test Meeting' to 3pm" | Event time updated, confirmation shown | |
| HV-28 | Delete event | Ask agent: "Delete the 'Test Meeting' event" | Event removed from calendar, confirmation shown | |
| HV-29 | Check availability | Ask agent: "Am I free tomorrow from 10am to 12pm?" | Returns availability status (free/busy) for the time range | |
| HV-30 | List calendars | Ask agent: "List all my Google calendars" | Returns list of calendars (primary + any shared/subscribed) | |
| HV-31 | Create recurring event | Ask agent: "Create a weekly team standup every Monday at 9am starting next week" | Recurring event created with correct recurrence rule | |

---

## Phase 5: Drive Operations (7 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-32 | List files | Ask agent: "List my recent Google Drive files" | Returns list of files with names, types, modified dates | |
| HV-33 | Search files | Ask agent: "Search my Drive for files named '[known filename]'" | Returns matching files | |
| HV-34 | Upload file | Ask agent: "Upload a file called 'test.txt' with content 'hello world' to my Drive" | File uploaded, confirmation with file ID and link | |
| HV-35 | Download file | Ask agent: "Download the file 'test.txt' from my Drive" | File content retrieved and displayed or saved locally | |
| HV-36 | Share file by email | Ask agent: "Share 'test.txt' with [email] as a viewer" | File shared, recipient gets access | |
| HV-37 | Enable link sharing | Ask agent: "Make 'test.txt' accessible to anyone with the link" | Link sharing enabled, shareable link returned | |
| HV-38 | Google Docs export | Ask agent: "Download my Google Doc named '[doc name]' as PDF" | Google Doc exported and downloaded in requested format | |

---

## Phase 6: Contacts Operations (5 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-39 | List contacts | Ask agent: "List my Google contacts" | Returns contacts with names and email addresses | |
| HV-40 | Search by name | Ask agent: "Find my contact named '[known name]'" | Returns matching contact(s) with details | |
| HV-41 | Search by email | Ask agent: "Find the contact with email '[known email]'" | Returns matching contact with full details | |
| HV-42 | Create contact | Ask agent: "Add a new contact: Test User, test@example.com, phone 555-0123" | Contact created in Google Contacts | |
| HV-43 | Verify contact created | Ask agent: "Find my contact named 'Test User'" | Returns the contact just created with correct details | |

---

## Phase 7: Tasks Operations (5 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-44 | List task lists | Ask agent: "List my Google task lists" | Returns task lists (at minimum "My Tasks" default list) | |
| HV-45 | List tasks | Ask agent: "Show my tasks in 'My Tasks'" | Returns tasks with titles, status, due dates | |
| HV-46 | Create task | Ask agent: "Add a task 'Buy groceries' due tomorrow to my task list" | Task created with correct title and due date | |
| HV-47 | Complete task | Ask agent: "Mark the task 'Buy groceries' as complete" | Task status updated to completed | |
| HV-48 | Delete task | Ask agent: "Delete the task 'Buy groceries'" | Task removed from the task list | |

---

## Phase 8: Service Toggles (5 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-49 | Disable a service | In config, disable the Drive service and save | Config saves, Drive shows as disabled | |
| HV-50 | Disabled tools hidden | Ask agent: "List my Drive files" | Agent reports Drive tools are unavailable or not loaded | |
| HV-51 | Re-enable service | In config, re-enable Drive and save | Config saves, Drive shows as enabled | |
| HV-52 | Re-enabled tools work | Ask agent: "List my Drive files" | Drive files returned normally | |
| HV-53 | OAuth scopes match | Check config page, verify only enabled services have active scopes | Enabled services listed match the OAuth scopes requested during auth | |

---

## Phase 9: Security & Edge Cases (6 tests)

| ID | Test | Steps | Expected | Result |
|----|------|-------|----------|--------|
| HV-54 | Invalid recipient blocked | Ask agent: "Send email to not-an-email" | Validation error, email not sent | |
| HV-55 | CSRF enforcement | Use curl without CSRF token: `curl -X POST http://localhost:50084/api/plugins/google/google_config_api -d '{}'` | Returns 403 or CSRF error | |
| HV-56 | Max attendees limit | Ask agent: "Create a calendar event and invite 200 people" | Error or limit enforced (not allowed to add excessive attendees) | |
| HV-57 | Tracking pixel removal | Send a test email containing `<img src="http://tracker.example.com/pixel.gif" width="1" height="1">` to yourself, then read it | Tracking pixel/image stripped or neutralized in displayed content | |
| HV-58 | Large email truncation | Read an email with extremely long body (10000+ chars) | Content truncated with indicator, no crash or timeout | |
| HV-59 | Expired token handling | Invalidate token (delete token.json or wait for expiry), then use a tool | Graceful error message about re-authentication needed, or automatic token refresh | |

---

## Results Summary

| Phase | Tests | Passed | Failed | Skipped |
|-------|-------|--------|--------|---------|
| 1. Plugin Activation & WebUI | 6 | | | |
| 2. OAuth Authentication | 7 | | | |
| 3. Gmail Operations | 10 | | | |
| 4. Calendar Operations | 8 | | | |
| 5. Drive Operations | 7 | | | |
| 6. Contacts Operations | 5 | | | |
| 7. Tasks Operations | 5 | | | |
| 8. Service Toggles | 5 | | | |
| 9. Security & Edge Cases | 6 | | | |
| **Total** | **59** | | | |

---

**Tester:** _______________
**Date:** _______________
**Container:** _______________
**Verdict:** PASS / FAIL
