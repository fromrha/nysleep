---
trigger: model_decision
description: Apply when starting any new project or when the user explicitly asks to initialize project tracking.
---

## Changelog Tracking Rule (NythSleep)

When triggered, you MUST:

1. Maintain `CHANGELOG.md` in the project root.

2. Every time you complete a feature, fix a bug, or make a meaningful change — append it under the `## [Unreleased]` block with the correct heading:
   - `### Added` for new features (e.g. new themes, CLI flags)
   - `### Fixed` for bug fixes (e.g. logic errors, output bugs)
   - `### Changed` for modifications (e.g. banner updates, refactoring)
   - `### Removed` for deletions

3. Never leave the changelog empty after completing work.

4. Use Caveman Full for short update. For Very big and long udpate, you can use an even more robust option, like ultra