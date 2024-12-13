from math import gcd


def parse_input(file_path):
    """
    Parses the input file to extract button configurations and prize locations.
    """
    machines = []
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines
        for i in range(0, len(lines), 3):
            # Parse Button A
            button_a_line = lines[i]
            a_x = int(button_a_line.split("X+")[1].split(",")[0])
            a_y = int(button_a_line.split("Y+")[1])

            # Parse Button B
            button_b_line = lines[i + 1]
            b_x = int(button_b_line.split("X+")[1].split(",")[0])
            b_y = int(button_b_line.split("Y+")[1])

            # Parse Prize
            prize_line = lines[i + 2]
            prize_x = int(prize_line.split("X=")[1].split(",")[0])
            prize_y = int(prize_line.split("Y=")[1])

            machines.append(((a_x, a_y), (b_x, b_y), (prize_x, prize_y)))
    return machines


def find_min_tokens(a_x, a_y, b_x, b_y, prize_x, prize_y, max_presses=100):
    """
    Finds the minimum number of tokens required to reach the prize position.
    Returns a tuple (x, y) representing the number of button A and B presses.
    If no solution exists within the given press limit, returns None.
    """
    det = a_x * b_y - a_y * b_x
    if det == 0:
        # Check if the system is consistent
        if a_x * prize_y != a_y * prize_x or b_x * prize_y != b_y * prize_x:
            # No solution
            return None
        else:
            # Infinite solutions: Find the one with minimal tokens within press limit
            min_tokens = None
            min_solution = None
            for x in range(0, max_presses + 1):
                if b_x == 0:
                    if a_x * x != prize_x:
                        continue
                    y = 0
                else:
                    if (prize_x - a_x * x) % b_x != 0:
                        continue
                    y = (prize_x - a_x * x) // b_x
                if y < 0:
                    continue
                # Verify Y-axis alignment
                if a_y * x + b_y * y != prize_y:
                    continue
                tokens = 3 * x + y
                if min_tokens is None or tokens < min_tokens:
                    min_tokens = tokens
                    min_solution = (x, y)
            return min_solution
    else:
        # Unique solution exists
        numerator_y = a_x * prize_y - a_y * prize_x
        numerator_x = prize_x * b_y - prize_y * b_x
        if det < 0:
            numerator_y = -numerator_y
            numerator_x = -numerator_x
            det = -det
        if numerator_y % det != 0 or numerator_x % det != 0:
            return None
        y = numerator_y // det
        x = numerator_x // det
        if x < 0 or y < 0:
            return None
        # Verify both equations
        if a_x * x + b_x * y != prize_x or a_y * x + b_y * y != prize_y:
            return None
        return (x, y)


def solve_claw_machine(machines, adjust_prize=False):
    """
    Solves the claw machine problem to find all possible solutions for each machine.
    Returns the total number of prizes won and the total tokens spent.
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

        # For Part 1, limit button presses to 100
        # For Part 2, increase the limit as necessary or handle unique solutions
        if not adjust_prize:
            solution = find_min_tokens(
                a_x, a_y, b_x, b_y, prize_x, prize_y, max_presses=100
            )
        else:
            # For Part 2, handle without press limit
            # Since find_min_tokens with a very high max_presses is inefficient,
            # we'll solve it analytically if possible
            det = a_x * b_y - a_y * b_x
            if det == 0:
                # Check consistency
                if a_x * prize_y != a_y * prize_x or b_x * prize_y != b_y * prize_x:
                    solution = None
                else:
                    # Find minimal tokens: iterate x to find y >=0
                    # To handle large numbers, find y = (prize_x - a_x * x) / b_x >=0 and integer
                    # Find x such that (prize_x - a_x * x) is divisible by b_x
                    # Minimal tokens: 3x + y
                    # To minimize 3x + y, prefer larger y (smaller x)
                    # Thus, find the smallest x possible
                    x = 0
                    while True:
                        if a_x * x > prize_x:
                            break
                        if (prize_x - a_x * x) % b_x == 0:
                            y = (prize_x - a_x * x) // b_x
                            if y < 0:
                                x += 1
                                continue
                            # Verify Y-axis
                            if a_y * x + b_y * y != prize_y:
                                x += 1
                                continue
                            tokens = 3 * x + y
                            solution = (x, y)
                            break
                        x += 1
                    else:
                        solution = None
            else:
                # det !=0, unique solution
                numerator_y = a_x * prize_y - a_y * prize_x
                numerator_x = prize_x * b_y - prize_y * b_x
                if det < 0:
                    numerator_y = -numerator_y
                    numerator_x = -numerator_x
                    det = -det
                if numerator_y % det != 0 or numerator_x % det != 0:
                    solution = None
                else:
                    y = numerator_y // det
                    x = numerator_x // det
                    if x < 0 or y < 0:
                        solution = None
                    else:
                        # Verify both equations
                        if a_x * x + b_x * y != prize_x or a_y * x + b_y * y != prize_y:
                            solution = None
                        else:
                            solution = (x, y)

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
    prizes_won_part2, tokens_spent_part2, solutions_part2 = solve_claw_machine(machines, adjust_prize=True)
    print(f"\nPart 2 - Maximum Prizes Won: {prizes_won_part2}")
    print(f"Part 2 - Minimum Tokens Spent: {tokens_spent_part2}")