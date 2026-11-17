# Lab 5 – Static Code Analysis
## Library Fine and Book Renewal System

The original program was analysed using Pylint, Bandit and Flake8.
The following issues were identified and addressed.

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe eval() usage | Security | 45 | The eval() function could execute arbitrary expressions and create a security risk. | Replaced eval() with a restricted AST-based arithmetic evaluator that permits only approved operations. |
| Broad exception handling | Security / Reliability | 21 | A bare except silently ignored errors when returning a book. | Replaced exception-based handling with explicit checks for the student and book in the loan records. |
| Mutable default argument | Bug | 9 | The dates=[] default list was shared across function calls. | Changed the default to None and initialized a new list inside the function. |
| Global state modification | Code Quality | 28, 35, 52 | Functions modified global variables, making program behaviour harder to track and test. | Passed loan records and fine rates explicitly between functions. |
| Missing documentation | Code Quality | Multiple | The module and functions lacked docstrings. | Added module and function docstrings. |
| Incorrect function naming | Code Style | 27 | renewBook did not follow Python's snake_case naming convention. | Renamed it to renew_book. |
| Unsafe file handling | Reliability | 34, 40 | Files were opened without an encoding and were not managed with context managers. | Used with open() and explicitly specified UTF-8 encoding. |
| Old-style string formatting | Code Style | 14 | The program used percent-based string formatting. | Replaced it with f-strings. |
| Unused import | Code Style | 2 | The os module was imported but never used. | Removed the unused import. |
| Negative fine calculation | Functional Bug | 25 | Negative overdue days could produce a negative fine. | Used max(0, days_overdue) to prevent negative fines. |
| Incorrect book ID type | Functional / Data Quality | 57 | A book ID was supplied as an integer even though IDs should be strings. | Changed the sample book ID to a string. |

## Final Static Analysis Results

- Pylint score: 10.00/10
- Bandit: No issues identified.
- Flake8: No issues reported.

The final code was checked again using all three static analysis tools.
