import json
from datetime import datetime

loans = {}
FINE_PER_DAY = 2


def add_book_loan(student_id, book_id, dates=[]):
    if not student_id:
        return

    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print(
        "%s borrowed %s (loan dates on record: %d)"
        % (student_id, book_id, len(dates))
    )


def return_book(student_id, book_id):
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        return


def calculate_fine(days_overdue):
    return days_overdue * FINE_PER_DAY


def renewBook(student_id, book_id, extra_days):
    global FINE_PER_DAY
    if extra_days > 14:
        FINE_PER_DAY = FINE_PER_DAY + 1

    print(
        "Renewed "
        + book_id
        + " for "
        + student_id
        + " by "
        + str(extra_days)
        + " days"
    )


def load_records(file="loans.json"):
    f = open(file, "r")
    global loans
    loans = json.loads(f.read())
    f.close()


def save_records(file="loans.json"):
    f = open(file, "w")
    f.write(json.dumps(loans))
    f.close()


def fine_from_rule(rule, days):
    """Calculate a fine using a restricted arithmetic expression."""
    import ast
    import operator

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

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
            operation = allowed_operators.get(type(node.op))
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
    except (SyntaxError, TypeError, ZeroDivisionError, OverflowError) as error:
        raise ValueError("Invalid fine calculation rule.") from error


def print_report():
    print("Loan Report")
    for student in loans:
        print(student, "->", loans[student])


def main():
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", "4521")
    return_book("S999", "B-NONE")
    renewBook("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    print("S102 owes:", calculate_fine(int(days)))
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
