### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/inventory"}

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_report.py']

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool call: read_file
{"file_path": "workspace/tests/test_report.py"}

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool call: ls
{"path": "."}

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q"}

### Tool result
['/workspace/']

### Tool result
.FF...                                                                   [100%]
=================================== FAILURES ===================================
_____________________ test_total_value_thousands_separator _____________________

>   ???

D:\VinAI20K\K4-DAY20-MULTIAGENTS-NguyenThanhDuong-2A202602961\tasks\code-learn\workspace\tests\test_report.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
inventory/report.py:14: in total_value
    price = parse_price(item["price"])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '$1,299.50'

    def parse_price(text):
        """Convert a price string to a Decimal.
    
        Supported formats:
          "$1,299.50" -> Decimal("1299.50")
          "  12 "     -> Decimal("12")
          "1299.5"    -> Decimal("1299.5")
          "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
        """
        cleaned = text.strip().replace("$", "")
>       return Decimal(cleaned)
               ^^^^^^^^^^^^^^^^
E       decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

inventory/pricing.py:15: InvalidOperation
________________________ test_discount_rounding_half_up ________________________

>   ???
E   AssertionError: assert Decimal('9.04') == Decimal('9.05')
E    +  where Decimal('9.04') = apply_discount(Decimal('10.05'), 10)
E    +    where Decimal('10.05') = Decimal('10.05'

### Assistant
Now let me check for any convention docs and inspect the pycache for clues:

### Tool call: glob
{"path": "workspace", "pattern": "**/*.{md,cfg,ini,toml,txt}"}

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom decimal import Decimal\nprint(repr(f'{Decimal(\\\"12.345\\\"):.2f}'))\nprint(repr(f'{Decimal(\\\"12.335\\\"):.2f}'))\nimport decimal\nprint(decimal.getcontext())\n\""}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md']

### Tool result
'12.34'
'12.34'
Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])

[Command succeeded with exit code 0]

### Assistant
All issues identified. Now I'll fix the three source modules according to their docstrings:

### Tool call: write_file
{"file_path": "workspace/inventory/pricing.py", "content": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import ROUND_HALF_UP, Decimal\n\n\ndef parse_price(text):\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\").replace(\",\", \"\")\n    if cleaned.startswith(\"(\") and cleaned.endswith(\")\"):\n        cleaned = \"-\" + cleaned[1:-1].strip()\n    return Decimal(cleaned)\n\n\ndef apply_discount(price, percent):\n    \"\"\"Return `price` after a percentage discount.\n\n    The result is a Decimal rounded to 2 decimal places using the\n    commercial rule \"round half up\" (0.005 -> 0.01).\n    \"\"\"\n    discounted = price * (100 - percent) / 100\n    return discounted.quantize(Decimal(\"0.01\"), rounding=ROUND_HALF_UP)\n"}

### Tool call: edit_file
{"new_string": "    return sorted(\n        (item[\"name\"] for item in items if item[\"qty\"] < threshold),\n        key=str.casefold,\n    )", "old_string": "    return [item[\"name\"] for item in items if item[\"qty\"] <= threshold]", "file_path": "workspace/inventory/report.py"}

### Tool result
Updated file /workspace/inventory/pricing.py

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/export.py", "new_string": "    price = parse_price(item[\"price\"])\n    name = item[\"name\"]\n    if '\"' in name or \",\" in name:\n        name = '\"' + name.replace('\"', '\"\"') + '\"'\n    return f\"{name},{price:.2f},{item['qty']}\"", "old_string": "    price = parse_price(item[\"price\"])\n    return f'{item[\"name\"]},{price:.2f},{item[\"qty\"]}'"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q"}

### Tool result
......                                                                   [100%]
6 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
All tests pass. Let me verify every docstring example, including the ones not covered by the visible tests:

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom decimal import Decimal\nfrom inventory.pricing import parse_price, apply_discount\nfrom inventory.report import total_value, low_stock\nfrom inventory.export import to_csv_row\n\n# parse_price docstring examples\nassert parse_price('\\$1,299.50') == Decimal('1299.50'), parse_price('\\$1,299.50')\nassert parse_price('  12 ') == Decimal('12')\nassert parse_price('1299.5') == Decimal('1299.5')\nassert parse_price('(12.00)') == Decimal('-12.00'), parse_price('(12.00)')\n\n# apply_discount: round half up, 0.005 -> 0.01\nassert apply_discount(Decimal('10.05'), 10) == Decimal('9.05')\nassert apply_discount(Decimal('1.00'), 0.5) == Decimal('1.00') if False else True\nassert apply_discount(Decimal('0.005'), 0) == Decimal('0.01'), apply_discount(Decimal('0.005'), 0)\nassert apply_discount(Decimal('100'), 15) == Decimal('85.00')\n\n# total_value\nassert total_value([{'name': 'pen', 'price': '\\$2.50', 'qty': 4}]) == Decimal('10.00')\nassert total_value([{'name': 'laptop', 'price': '\\$1,299.50', 'qty': 2}]) == Decimal('2599.00')\nassert total_value([{'name': 'desk', 'price': '100.00', 'qty': 1, 'discount': 15}]) == Decimal('85.00')\nassert total_value([]) == Decimal('0')\n\n# low_stock: strictly below threshold, case-insensitive sort\nassert low_stock([{'name': 'pen', 'qty': 2}, {'name': 'ink', 'qty': 9}]) == ['pen']\nassert low_stock([{'name': 'b', 'qty': 5}], threshold=5) == []          # 5 is not strictly below 5\nassert low_stock([{'na

### Tool result
All docstring examples verified OK

[Command succeeded with exit code 0]

### Assistant
All docstring examples verified. Let me do a final review of the changed files:

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool result
@@ lines 1-27 of 27 @@
"""Price utilities for the inventory package."""
from decimal import ROUND_HALF_UP, Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "").replace(",", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = "-" + cleaned[1:-1].strip()
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

### Tool result
@@ lines 1-28 of 28 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return sorted(
        (item["name"] for item in items if item["qty"] < threshold),
        key=str.casefold,
    )

### Tool result
@@ lines 1-15 of 15 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    name = item["name"]
    if '"' in name or "," in name:
        name = '"' + name.replace('"', '""') + '"'
    return f"{name},{price:.2f},{item['qty']}"

### Assistant
All 6 tests pass and every docstring example is verified. Here's a summary of the changes:

## Changes (all in `workspace/inventory/`, no test files touched)

**`pricing.py`**
- `parse_price`: now strips thousands separators (`,`) so `"$1,299.50"` parses correctly, and handles accounting-style parentheses — `"(12.00)"` → `Decimal("-12.00")` — as the docstring specifies. Previously both cases raised `decimal.InvalidOperation`.
- `apply_discount`: now rounds with `ROUND_HALF_UP` (explicitly passed to `quantize`) instead of relying on the context default `ROUND_HALF_EVEN`, which turned `10.05 @ 10%` into `9.04` instead of the specified `9.05`.

**`report.py`**
- `low_stock`: changed `item["qty"] <= threshold` to a strict `<` (docstring says "strictly below"), and the returned names are now sorted alphabetically ignoring case via `key=str.casefold` (previously unsorted).

**`export.py`**
- `to_csv_row`: implements the RFC 4180 quoting rule from the docstring — names containing a comma or double quote are wrapped in double quotes with inner quotes doubled (e.g. `say "hi"` → `"say ""hi"""`). Previously the name was emitted raw, breaking the CSV for such names. Also switched the f-string to consistent double quotes.

Verified beyond the visible tests: negative-parenthesis prices, `0.005 → 0.01` half-up rounding, empty-item totals, threshold boundary (`qty == threshold` excluded), case-insensitive sorting, and CSV quoting of commas/quotes.