---
name: output-rules-first
description: Use when a task states required output files, keys, naming, sorting, units, or formats that the deliverable must follow.
---
- Before writing any output, re-read the task and list every explicit rule: required files, required keys/headers, field names, units, value formats, sort order, and naming conventions.
- Treat these rules as hard requirements, not suggestions. Never replace them with your own "standard conventions" (e.g., default rounding, default key order, raw identifiers).
- Create every required artifact exactly as specified — a missing required file or key is a failure even if the analysis is correct.
- Apply transformations the rules demand (e.g., normalizing identifiers, sorting output, converting units) inside the producing script, not mentally.
- If a rule's wording is precise (a format, a heading, a unit), follow it literally.
- Keep the rule list next to you and implement one rule at a time.
