# Reflection – Lab 5: Static Code Analysis

(Match each heading below to the exact wording of the four questions in your handout/portal.)

## 1. Which issues were the easiest and which were the hardest to fix?
The style issues were the easiest. Flake8 and Pylint gave exact line numbers and the fix was mechanical: renaming functions to snake_case, adding docstrings, adding blank lines and wrapping long lines. The hardest ones were the design problems. Removing the `global order_total` and the module-level `conn` meant changing how data flows through the program: `place_order` now returns the order id and `main()` keeps the running total, so I had to make sure the output (`1 540`) stayed the same. Replacing `os.system` was also a decision rather than a one-line patch, because I had to think about what "notify the warehouse" should actually do.

## 2. Did the tools report any false positives, or issues that you chose not to fix or disagreed with?
I did not find any real false positives. Bandit's B110 (try/except/pass) is only Low severity, but it was a real problem here because it hid database errors. The Pylint messages about docstrings and naming are style preferences rather than bugs, but they are cheap to fix and improve readability. If I had replaced `os.system` with `subprocess.run`, Bandit would have raised new Low warnings (B404/B603), so I removed the shell call entirely and used `logging`.

## 3. How could static analysis be integrated into a real development workflow?
I would run Flake8 and Pylint as a pre-commit hook so that style problems never reach the repository, and run Bandit plus Pylint in a CI pipeline (for example GitHub Actions) on every pull request, failing the build if Bandit reports High/Medium issues or the Pylint score drops below a threshold such as 9.5. Developers can also run them inside the editor for instant feedback.

## 4. What impact did fixing these issues have on code quality, security and maintainability?
Pylint went from 2.41/10 to 10.00/10, Bandit went from 3 issues (1 High, 1 Medium, 1 Low) to 0, and Flake8 went from 11 warnings to 0. The program prints the same result as before, but it is no longer open to SQL injection or shell command injection, it reports errors instead of hiding them, it no longer depends on global state, and every function is documented. This makes the code safer, easier to test (functions take a connection and can be tested with a temporary database) and easier for someone else to read. Static analysis cannot prove the program is correct, but it caught real bugs I would probably have missed by reading the code.
