# Issues Found – supplier_orders.py

Tools: Pylint (before 2.41/10, after 10.00/10), Bandit (before 1 High, 1 Medium, 1 Low, after 0), Flake8 (before 11 warnings, after 0).
Line numbers refer to the ORIGINAL file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| OS command injection (Bandit B605, **High**) | Security | 20 | `os.system("echo ... " + supplier)` runs a shell command built from caller input. A supplier name like `x; rm -rf /` would run as a command. | Removed the shell call and used `logging.info("... %s", supplier)`. No shell is involved, so no injection is possible. |
| SQL injection (Bandit B608, **Medium**) | Security | 12 | The INSERT statement is built with `%` string formatting, so a supplier such as `x'); DROP TABLE orders;--` changes the query. | Switched to a parameterized query with `?` placeholders and a values tuple. |
| Silent `try/except/pass` (Bandit B110, Low; Pylint W0718) | Bug / Security | 24-26 | `except Exception: pass` hides every failure in `cleanup()`, so a failed delete goes unnoticed. | Catch only `sqlite3.Error`, log the error with `logging.error`, and wrap the delete in `with connection:` so it commits or rolls back. |
| Unused argument `remarks` (Pylint W0613) | Bug | 16 | `mark_received` accepted `remarks` but never used it, so the remarks were silently thrown away. | Added a `remarks` column and store it in the UPDATE (parameterized). |
| Global variable `order_total` (Pylint W0603, C0103) | Design | 8, 11 | The function modified module-level state through `global`, which is hard to test and reason about. | Removed the global. `place_order` returns the new order id and `main()` keeps a local running total. |
| Redefined outer name `conn` (Pylint W0621) | Design | 4, 10, 16, 22, 28 | A module-level `conn` was shadowed by every function parameter, and the DB was created at import time. | Added `create_connection()`, parameters renamed to `connection`, and the connection is created inside `main()`. |
| Naming (Pylint C0103) | Style | 10, 16, 19, 28 | `placeOrder`, `markReceived`, `notifyWarehouse`, `pendingCount` are camelCase, not snake_case. | Renamed to `place_order`, `mark_received`, `notify_warehouse`, `pending_count`. |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 10, 16, 19, 22, 28, 31 | The module and all functions had no docstring. | Added a module docstring and a one-line docstring for each function. |
| Line too long (Pylint C0301, Flake8 E501) | Style | 6, 12, 29 | Three lines exceed 79 characters (122, 131, 87). | Split long SQL strings across lines using implicit string concatenation inside parentheses. |
| Blank lines / spacing (Flake8 E302, E305, E225) | Style | 10, 16, 19, 22, 28, 31, 39, 13 | Only one blank line between functions, and `order_total+=quantity` has no spaces around the operator. | Two blank lines between top-level definitions, `order_total += quantity`. |
| `main()` runs on import | Design | 44 | `main()` was called at module level, so importing the file ran the whole demo. | Wrapped in `if __name__ == "__main__":`. |
