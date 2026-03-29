"""API endpoint: Test Google connection (verify OAuth, get user profile + service status).
URL: POST /api/plugins/google/google_test
"""
from helpers.api import ApiHandler, Request, Response


class GoogleTest(ApiHandler):

    @classmethod
    def get_methods(cls) -> list[str]:
        return ["GET", "POST"]

    @classmethod
    def requires_csrf(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            # Self-heal: ensure symlink exists for plugin namespace imports
            from pathlib import Path
            plugin_dir = Path(__file__).resolve().parent.parent
            for root in [Path("/a0"), Path("/git/agent-zero")]:
                plugins_dir = root / "plugins"
                if plugins_dir.is_dir():
                    symlink = plugins_dir / "google"
                    if not symlink.exists():
                        symlink.symlink_to(plugin_dir)
                    break

            from plugins.google.helpers.google_auth import (
                get_google_config, is_authenticated, build_service,
                get_enabled_services,
            )

            config = get_google_config()
            authenticated, email_or_error = is_authenticated(config)

            if not authenticated:
                return {
                    "ok": False,
                    "authenticated": False,
                    "error": email_or_error,
                }

            result = {
                "ok": True,
                "authenticated": True,
                "email": email_or_error,
                "services": {},
            }

            enabled = get_enabled_services(config)

            # Gmail stats
            if "gmail" in enabled:
                try:
                    service = build_service("gmail", config)
                    profile = service.users().getProfile(userId="me").execute()
                    unread = service.users().messages().list(
                        userId="me", labelIds=["INBOX", "UNREAD"], maxResults=1,
                    ).execute()
                    result["services"]["gmail"] = {
                        "ok": True,
                        "messages_total": profile.get("messagesTotal", 0),
                        "threads_total": profile.get("threadsTotal", 0),
                        "unread": unread.get("resultSizeEstimate", 0),
                    }
                except Exception as e:
                    result["services"]["gmail"] = {"ok": False, "error": str(e)}

            # Calendar stats
            if "calendar" in enabled:
                try:
                    service = build_service("calendar", config)
                    cals = service.calendarList().list().execute()
                    result["services"]["calendar"] = {
                        "ok": True,
                        "calendars": len(cals.get("items", [])),
                    }
                except Exception as e:
                    result["services"]["calendar"] = {"ok": False, "error": str(e)}

            # Drive stats
            if "drive" in enabled:
                try:
                    service = build_service("drive", config)
                    about = service.about().get(fields="storageQuota,user").execute()
                    quota = about.get("storageQuota", {})
                    result["services"]["drive"] = {
                        "ok": True,
                        "usage_bytes": int(quota.get("usage", 0)),
                        "limit_bytes": int(quota.get("limit", 0)) if quota.get("limit") else None,
                    }
                except Exception as e:
                    result["services"]["drive"] = {"ok": False, "error": str(e)}

            # Contacts stats
            if "contacts" in enabled:
                try:
                    service = build_service("contacts", config)
                    conns = service.people().connections().list(
                        resourceName="people/me", pageSize=1, personFields="names",
                    ).execute()
                    result["services"]["contacts"] = {
                        "ok": True,
                        "total": conns.get("totalPeople", 0),
                    }
                except Exception as e:
                    result["services"]["contacts"] = {"ok": False, "error": str(e)}

            # Tasks stats
            if "tasks" in enabled:
                try:
                    service = build_service("tasks", config)
                    lists = service.tasklists().list(maxResults=10).execute()
                    result["services"]["tasks"] = {
                        "ok": True,
                        "task_lists": len(lists.get("items", [])),
                    }
                except Exception as e:
                    result["services"]["tasks"] = {"ok": False, "error": str(e)}

            return result

        except Exception as e:
            return {
                "ok": False,
                "authenticated": False,
                "error": f"Connection failed: {type(e).__name__}: {e}",
            }
