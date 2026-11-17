"""Library book loan, renewal, and fine management system."""

import ast
import json
import operator
from datetime import datetime

FINE_PER_DAY = 2

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def add_book_loan(loans, student_id, book_id, dates=None):
    """Record a book loan for a student."""
    if not student_id:
        return loans

    if dates is None:
        dates = []

    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]

    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )
    return loans


def return_book(loans, student_id, book_id):
    """Remove a returned book from a student's loan records."""
    if student_id in loans and book_id in loans[student_id]:
        loans[student_id].remove(book_id)

        if not loans[student_id]:
            del loans[student_id]

    return loans


def calculate_fine(days_overdue, fine_per_day=FINE_PER_DAY):
    """Calculate the fine for overdue days."""
    return max(0, days_overdue) * fine_per_day


def renew_book(student_id, book_id, extra_days, fine_per_day):
    """Renew a book and update the fine rate for long renewals."""
    if extra_days > 14:
        fine_per_day += 1

    print(
        f"Renewed {book_id} for {student_id} "
        f"by {extra_days} days"
    )
    return fine_per_day


def load_records(file="loans.json"):
    """Load loan records from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as records_file:
            return json.load(records_file)
    except FileNotFoundError:
        return {}


def save_records(loans, file="loans.json"):
    """Save loan records to a JSON file."""
    with open(file, "w", encoding="utf-8") as records_file:
        json.dump(loans, records_file, indent=4)


def fine_from_rule(rule, days):
    """Calculate a fine using a restricted arithmetic expression."""

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(
                node.value, bool
            ):
                return node.value
            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.Name) and node.id == "days":
            return days

        if isinstance(node, ast.BinOp):
            operation = ALLOWED_OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large.")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Invalid fine calculation rule.")

    try:
        expression = ast.parse(rule, mode="eval")
        return evaluate(expression)
    except (
        SyntaxError,
        TypeError,
        ZeroDivisionError,
        OverflowError,
    ) as error:
        raise ValueError("Invalid fine calculation rule.") from error


def print_report(loans):
    """Display all current book loans."""
    print("Loan Report")
    for student, books in loans.items():
        print(student, "->", books)


def main():
    """Run the library loan management demonstration."""
    loans = {}
    fine_per_day = FINE_PER_DAY

    loans = add_book_loan(loans, "S101", "B-ALGO")
    loans = add_book_loan(loans, "S102", "B-NETW")
    loans = add_book_loan(loans, "", "B-DBMS")
    loans = add_book_loan(loans, "S103", "4521")

    loans = return_book(loans, "S999", "B-NONE")

    fine_per_day = renew_book(
        "S101", "B-ALGO", 21, fine_per_day
    )

    print("Fine for 5 days:", calculate_fine(5, fine_per_day))
    print("Fine for -3 days:", calculate_fine(-3, fine_per_day))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))

    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    print("S102 owes:", calculate_fine(int(days), fine_per_day))

    save_records(loans)
    loans = load_records()
    print_report(loans)


if __name__ == "__main__":
    main()
