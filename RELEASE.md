---
status: published
repo: https://github.com/spinnakergit/a0-google
index_pr: https://github.com/agent0ai/a0-plugins/pull/74
published_date: 2026-03-14
version: 1.1.0
---

# Release Status

## Publication
- **GitHub**: https://github.com/spinnakergit/a0-google
- **Plugin Index PR**: [#74](https://github.com/agent0ai/a0-plugins/pull/74) (CI passed)
- **Published**: 2026-03-14

## v1.1.0 (2026-03-28)

### Changes
- Migrated config.html to Alpine.js framework pattern (outer Save button for settings, custom JS retained for OAuth flow)
- Added hooks.py for plugin lifecycle management
- Added thumbnail.png (256x256 indexed PNG, Google blue)
- Improved install.sh with in-place detection for plugin manager installs

### Notes
- Auth tab retains custom API-driven JS for OAuth flow (upload credentials, get auth URL, submit code)
- Services/Gmail/Calendar/Drive/Security tabs use Alpine.js x-model bindings saved by framework outer Save

## v1.0.0 (2026-03-14)

### Verification
- **Automated Tests**: 47/47 PASS
- **Human Verification**: 59/59 PASS
- **Security Assessment**: Completed

## Commit History
| Hash | Date | Description |
|------|------|-------------|
| `01a1899` | 2026-03-14 | Add 6 semantic workflow skills |
| `f88b0bd` | 2026-03-14 | Google Suite plugin for Agent Zero v1.0.0 |
