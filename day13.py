def parse_input(file_path):
    """
    Parses the input file to extract button configurations and prize locations.
    """
    machines = []
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines
        machines.extend(
            parse_machine(lines[i : i + 3]) for i in range(0, len(lines), 3)
        )
    return machines


def parse_machine(lines):
    """
    Parses the lines for a single machine and extracts button configurations and prize location.
    """

    def extract_values(line, key_x, key_y):
        x = int(line.split(key_x)[1].split(",")[0])
        y = int(line.split(key_y)[1])
        return x, y

    button_a = extract_values(lines[0], "X+", "Y+")
    button_b = extract_values(lines[1], "X+", "Y+")
    prize = extract_values(lines[2], "X=", "Y=")
    return button_a, button_b, prize


def solve_linear_diophantine(a_x, a_y, b_x, b_y, prize_x, prize_y, max_presses=None):
    """
    Solves the linear Diophantine equation for the given button configurations and prize location.
    Returns a tuple (x, y) of button presses or None if no solution exists.
    """
    det = a_x * b_y - a_y * b_x

    if det == 0:  # Check for dependent system
        return solve_dependent_system(a_x, a_y, b_x, b_y, prize_x, prize_y, max_presses)

    return solve_independent_system(a_x, a_y, b_x, b_y, prize_x, prize_y, det)


def solve_dependent_system(a_x, a_y, b_x, b_y, prize_x, prize_y, max_presses):
    """
    Handles the case where the system is dependent (det == 0).
    """
    if a_x * prize_y != a_y * prize_x or b_x * prize_y != b_y * prize_x:
        return None  # No solution exists

    min_tokens, solution = None, None

    for x in range(max_presses + 1 if max_presses else 101):
        y = compute_y_dependent(a_x, b_x, prize_x, x)
        if y is not None and a_y * x + b_y * y == prize_y:
            tokens = 3 * x + y
            if min_tokens is None or tokens < min_tokens:
                min_tokens, solution = tokens, (x, y)
    return solution


def compute_y_dependent(a_x, b_x, prize_x, x):
    """
    Computes the value of y for the dependent system.
    """
    if b_x == 0:
        return 0 if a_x * x == prize_x else None
    return None if (prize_x - a_x * x) % b_x != 0 else (prize_x - a_x * x) // b_x


def solve_independent_system(a_x, a_y, b_x, b_y, prize_x, prize_y, det):
    """
    Handles the case where the system is independent (det != 0).
    """
    numerator_y = a_x * prize_y - a_y * prize_x
    numerator_x = prize_x * b_y - prize_y * b_x

    if det < 0:
        numerator_y, numerator_x, det = -numerator_y, -numerator_x, -det

    if numerator_y % det != 0 or numerator_x % det != 0:
        return None

    x, y = numerator_x // det, numerator_y // det
    return (x, y) if x >= 0 and y >= 0 else None


def solve_claw_machine(machines, adjust_prize=False):
    """
    Solves the claw machine problem and returns prizes won, tokens spent, and solutions for all machines.
    """
    total_prizes_won = 0
    total_tokens_spent = 0
    all_solutions = []

    for idx, (button_a, button_b, prize) in enumerate(machines, 1):
        a_x, a_y = button_a
        b_x, b_y = button_b
        prize_x, prize_y = prize

        if adjust_prize:
            prize_x += 10**13
            prize_y += 10**13

        solution = solve_linear_diophantine(
            a_x,
            a_y,
            b_x,
            b_y,
            prize_x,
            prize_y,
            max_presses=(None if adjust_prize else 100),
        )

        if solution:
            x, y = solution
            tokens = 3 * x + y
            total_prizes_won += 1
            total_tokens_spent += tokens
            all_solutions.append(
                {"Machine": idx, "A_Presses": x, "B_Presses": y, "Tokens": tokens}
            )
        else:
            all_solutions.append(
                {"Machine": idx, "A_Presses": None, "B_Presses": None, "Tokens": None}
            )

    return total_prizes_won, total_tokens_spent, all_solutions


if __name__ == "__main__":
    file_path = "inputs/input_day13.txt"  # Ensure this path is correct
    machines = parse_input(file_path)

    # Part 1
    prizes_won_part1, tokens_spent_part1, solutions_part1 = solve_claw_machine(
        machines, adjust_prize=False
    )
    print(f"Part 1 - Maximum Prizes Won: {prizes_won_part1}")
    print(f"Part 1 - Minimum Tokens Spent: {tokens_spent_part1}")

    # Part 2
    prizes_won_part2, tokens_spent_part2, solutions_part2 = solve_claw_machine(
        machines, adjust_prize=True
    )
    print(f"\nPart 2 - Maximum Prizes Won: {prizes_won_part2}")
    print(f"Part 2 - Minimum Tokens Spent: {tokens_spent_part2}")
