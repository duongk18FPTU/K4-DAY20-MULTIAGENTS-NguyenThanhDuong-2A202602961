"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use FIRST, before changing anything, when you must understand a task folder. It reads the "
                "READMEs, docstrings, task rules and a sample of the data files, then reports the facts "
                "(formats, conventions, edge cases, naming rules). Give it the folder paths to inspect. "
                "It never modifies files."
            ),
            "system_prompt": (
                "You are a read-only explorer. Read every README, docstring, instruction file and the first "
                "rows or lines of each data file in the paths you are given. Look hard for conventions and "
                "rules (naming, formats, units, timezones, ordering, required output files) and for dirty "
                "data (duplicates, missing values, mixed formats). Report a concise list of facts and "
                "rules, quoting the source file for each. Do NOT create, edit or delete any file."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use to carry out a well-specified change: fix code, write a script or produce an output "
                "file. The delegation message must contain ALL the rules of the task and the exact relative "
                "file paths, because the implementer sees nothing else. It runs the tests or scripts and "
                "reports what it really changed and the result."
            ),
            "system_prompt": (
                "You are an implementer. Do exactly the change described in the message, following every "
                "rule it lists. Fix the root cause, not the symptom. After the change, run the relevant "
                "tests or script with the shell and read the output. Report only the files you really "
                "created or changed and the real test or script result. If a rule is unclear, say so "
                "instead of guessing."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use LAST, after the work is done, to independently verify it against the task statement "
                "and its rules (output files exist, formats and naming follow the rules, edge cases and "
                "duplicates handled, tests pass). Give it the original task text and the paths of the "
                "results. It reports problems but never fixes them."
            ),
            "system_prompt": (
                "You are an independent reviewer. Re-check the finished work against the original task and "
                "every rule in it: do the required files exist, are names and formats correct, are edge "
                "cases handled, do the tests pass when you run them yourself. Do not trust claims, verify "
                "by reading files and running commands. Report a numbered list of concrete problems "
                "(or 'no problems found'). Do NOT modify any file."
            ),
        },
    ]
