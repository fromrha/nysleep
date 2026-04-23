---
trigger: model_decision
description: Apply when a meaningful feature set is complete, a bug fix is shipped, or the user says the app/feature is done. Use GitHub MCP to tag and release.
---

## GitHub Release & Tagging Rule (NythSleep)

When a feature or milestone is complete, you MUST use the GitHub MCP to:

1. **Verify the version** matches across `CHANGELOG.md` and the banner in `src/nythsleep.py`.
2. **Determine the version bump**:
   - New features → bump MINOR (e.g. v1.2.0 → v1.3.0)
   - Bug fixes only → bump PATCH (e.g. v1.2.0 → v1.2.1)
   - Breaking changes → bump MAJOR (e.g. v1.2.0 → v2.0.0)

3. **Move the changelog entries** from `[Unreleased]` to a new version block: