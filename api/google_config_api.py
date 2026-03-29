"""API endpoint: Get/set Google plugin configuration + OAuth flow.
URL: POST /api/plugins/google/google_config_api
"""
import json
import os
import yaml
from pathlib import Path
from helpers.api import ApiHandler, Request, Response


def _get_config_path() -> Path:
    """Find the writable config path for the google plugin."""
    candidates = [
        Path(__file__).parent.parent / "config.json",
        Path("/a0/usr/plugins/google/config.json"),
        Path("/a0/plugins/google/config.json"),
        Path("/git/agent-zero/usr/plugins/google/config.json"),
    ]
    for p in candidates:
        if p.parent.exists():
            return p
    return candidates[-1]


class GoogleConfigApi(ApiHandler):

    @classmethod
    def get_methods(cls) -> list[str]:
        return ["GET", "POST"]

    @classmethod
    def requires_csrf(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        action = input.get("action", "get")
        if request.method == "GET" or action == "get":
            return self._get_config()
        elif action == "auth_url":
            return self._get_auth_url()
        elif action == "auth_callback":
            return self._handle_auth_callback(input)
        elif action == "upload_credentials":
            return self._upload_credentials(input)
        else:
            return self._set_config(input)

    def _get_config(self) -> dict:
        try:
            config_path = _get_config_path()
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
            else:
                default_path = config_path.parent / "default_config.yaml"
                if default_path.exists():
                    with open(default_path, "r") as f:
                        config = yaml.safe_load(f) or {}
                else:
                    config = {}

            # Check auth status
            try:
                from usr.plugins.google.helpers.google_auth import is_authenticated
                authenticated, email_or_error = is_authenticated(config)
                config["_auth_status"] = {
                    "authenticated": authenticated,
                    "email": email_or_error if authenticated else "",
                    "error": "" if authenticated else email_or_error,
                }
            except Exception as e:
                config["_auth_status"] = {
                    "authenticated": False,
                    "email": "",
                    "error": str(e),
                }

            # Check if credentials.json exists
            try:
                from usr.plugins.google.helpers.google_auth import _credentials_path
                config["_has_credentials"] = _credentials_path(config).exists()
            except Exception:
                config["_has_credentials"] = False

            # Report enabled services
            try:
                from usr.plugins.google.helpers.google_auth import get_enabled_services
                config["_enabled_services"] = sorted(get_enabled_services(config))
            except Exception:
                config["_enabled_services"] = []

            return config
        except Exception:
            return {"error": "Failed to read configuration."}

    def _get_auth_url(self) -> dict:
        """Generate OAuth authorization URL."""
        try:
            from usr.plugins.google.helpers.google_auth import (
                get_google_config, generate_auth_url,
            )
            config = get_google_config()
            url = generate_auth_url(config)
            return {"ok": True, "auth_url": url}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _handle_auth_callback(self, input: dict) -> dict:
        """Exchange auth code for token."""
        try:
            code = input.get("code", "").strip()
            if not code:
                return {"ok": False, "error": "No authorization code provided."}

            from usr.plugins.google.helpers.google_auth import (
                get_google_config, exchange_auth_code, is_authenticated,
            )
            config = get_google_config()
            exchange_auth_code(config, code)

            authenticated, email_or_error = is_authenticated(config)
            if authenticated:
                return {
                    "ok": True,
                    "authenticated": True,
                    "email": email_or_error,
                }
            else:
                return {"ok": False, "error": email_or_error}
        except Exception as e:
            return {"ok": False, "error": f"Auth callback failed: {e}"}

    def _upload_credentials(self, input: dict) -> dict:
        """Save credentials.json content to data directory."""
        try:
            creds_data = input.get("credentials", "")
            if not creds_data:
                return {"ok": False, "error": "No credentials data provided."}

            if isinstance(creds_data, str):
                creds_json = json.loads(creds_data)
            else:
                creds_json = creds_data

            if "installed" not in creds_json and "web" not in creds_json:
                return {
                    "ok": False,
                    "error": "Invalid credentials.json: must contain 'installed' or 'web' key.",
                }

            from usr.plugins.google.helpers.google_auth import _data_dir, get_google_config, secure_write_json
            config = get_google_config()
            data = _data_dir(config)
            creds_path = data / "credentials.json"

            secure_write_json(creds_path, creds_json)

            return {"ok": True, "path": str(creds_path)}
        except json.JSONDecodeError:
            return {"ok": False, "error": "Invalid JSON in credentials data."}
        except Exception as e:
            return {"ok": False, "error": f"Failed to save credentials: {e}"}

    def _set_config(self, input: dict) -> dict:
        try:
            config = input.get("config", input)
            if not config or config == {"action": "set"}:
                return {"error": "No config provided"}

            config.pop("action", None)
            config.pop("_auth_status", None)
            config.pop("_has_credentials", None)
            config.pop("_enabled_services", None)

            config_path = _get_config_path()
            config_path.parent.mkdir(parents=True, exist_ok=True)

            from usr.plugins.google.helpers.google_auth import secure_write_json
            secure_write_json(config_path, config)

            return {"ok": True}
        except Exception:
            return {"error": "Failed to save configuration."}
