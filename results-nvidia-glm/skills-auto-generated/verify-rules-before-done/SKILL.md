---
name: verify-rules-before-done
description: Use when finishing a task that has stated rules or a review checklist, before reporting completion.
---
- When the work looks done, re-read every stated rule and check the real artifacts against each rule one at a time.
- Verify by inspecting actual outputs (read the final file, run a check script), never from memory of what you wrote.
- Check organisation as well as content: required files exist, required keys/headers present, naming/format/sort/unit rules followed.
- Sanity checks you invent (counts add up, examples pass) do not substitute for the stated rules; do both.
- If any rule check fails, fix the output and re-run the check before finishing.
- Also confirm no prohibition was violated (e.g., files that must not be modified are untouched).
