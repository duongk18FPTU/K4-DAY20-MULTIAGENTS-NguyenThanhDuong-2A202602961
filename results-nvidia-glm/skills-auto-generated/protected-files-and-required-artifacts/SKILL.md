---
name: protected-files-and-required-artifacts
description: Use when modifying an existing codebase that forbids changing some files or requires companion artifacts for each change.
---
- At the start, identify (a) files/directories that must not be modified and (b) artifacts the task requires you to add (e.g., a regression test per bug fixed, a changelog entry per fix, type annotations on all public functions).
- Never edit protected files; extend behavior by adding new files instead.
- After each fix, immediately create its companion artifact (test, changelog bullet) — do not defer them to the end or skip them because tests pass.
- Add type annotations to every public function you write or touch (parameters and return), per the stated rule.
- Before finishing, list changed and added files (diff or directory listing) and confirm: no protected file changed, every required artifact exists and passes.
