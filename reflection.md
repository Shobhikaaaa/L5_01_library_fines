# Lab 5 – Reflection
## Static Code Analysis

### 1. What did you learn about static code analysis?

I learned that static code analysis helps identify potential bugs, security vulnerabilities and coding standard violations without executing the program. It helps developers detect problems early and improve code quality, reliability and maintainability.

### 2. What is the purpose of Pylint, Bandit and Flake8?

Pylint checks overall Python code quality, including naming conventions, documentation, unused variables and programming practices. Bandit identifies common security vulnerabilities and unsafe coding patterns. Flake8 checks Python formatting and compliance with PEP 8 style guidelines.

Using all three tools provided a more complete analysis because each tool focuses on a different aspect of the code.

### 3. What issues did you identify and how did you fix them?

The original library system contained several issues, including a mutable default argument, unsafe use of eval(), broad exception handling, global variables, missing docstrings and incorrect naming conventions.

I replaced eval() with a restricted AST-based arithmetic evaluator, removed silent exception handling, changed the mutable default argument to None, and refactored functions to pass data explicitly. I also improved file handling, documentation and formatting.

### 4. How did static analysis improve the final program?

Static analysis helped improve the security, readability and maintainability of the library system. The final program achieved a Pylint score of 10.00/10, Bandit reported no security issues, and Flake8 reported no style violations.

This lab demonstrated that static analysis tools are useful during development because they help identify issues before they become larger problems.
