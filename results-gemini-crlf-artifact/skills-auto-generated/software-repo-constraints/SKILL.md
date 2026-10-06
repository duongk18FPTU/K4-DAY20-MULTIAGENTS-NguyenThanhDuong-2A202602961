---
name: software-repo-constraints
description: Use when fixing bugs, adding features, or modifying codebases that have strict repository structure and process rules.
---
- Never modify original test files located in test directories unless explicitly permitted; always add new tests in separate files.
- Add regression tests for every individual bug fixed according to the specified count and filename conventions.
- Add corresponding entries to the changelog under the designated heading for every fix.
- Ensure all public functions have complete type annotations on all parameters and return values.
