from typing import List, Optional, Tuple


def parse_equation(line: str) -> Optional[Tuple[int, List[str]]]:
    line = line.strip()
    if not line:
        return None
    try:
        test_value_str, numbers_str = line.split(":")
        test_value = int(test_value_str.strip())
        numbers = [int(n) for n in numbers_str.strip().split()]
        if any(n <= 0 for n in numbers):
            raise ValueError("All numbers must be positive integers")
        return test_value, numbers
    except ValueError as e:
        print(f"Error parsing line '{line}': {e}")
        return None


def is_equation_valid_dp(test_value: int, numbers: List[str]) -> bool:
    if not numbers:
        return False

    dp = [set() for _ in range(len(numbers))]
    dp[0].add(numbers[0])

    for i in range(1, len(numbers)):
        for prev_result in dp[i - 1]:
            # Addition
            dp[i].add(str(int(prev_result) + int(numbers[i])))
            # Multiplication
            dp[i].add(str(int(prev_result) * int(numbers[i])))
            # # Concatenation
            # dp[i].add(str(prev_result) + str(numbers[i]))

    return str(test_value) in dp[-1]


def calculate_total_calibration(equations: List[str]) -> Tuple[int, List[int]]:
    total = 0
    valid_equations = []
    for line in equations:
        parsed = parse_equation(line)
        if parsed is None:
            continue
        test_value, numbers = parsed
        if is_equation_valid_dp(test_value, numbers):
            total += test_value
            valid_equations.append(test_value)
    return total, valid_equations


def main():
    input_path = "inputs/input_day7.txt"

    try:
        with open(input_path, "r") as file:
            equations = file.readlines()
    except FileNotFoundError:
        print(f"Input file '{input_path}' not found.")
        return

    total, _ = calculate_total_calibration(equations)

    print("Total Calibration Result:", total)


if __name__ == "__main__":
    main()
