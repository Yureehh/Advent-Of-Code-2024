def run_3bit_computer(initial_A, initial_B, initial_C, program):
    A = initial_A
    B = initial_B
    C = initial_C

    ip = 0
    output_values = []

    def get_combo_value(x):
        if x <= 3:
            return x
        elif x == 4:
            return A
        elif x == 5:
            return B
        elif x == 6:
            return C
        else:
            raise ValueError("Invalid operand value 7 encountered.")

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1] if ip + 1 < len(program) else 0

        if opcode == 0:  # adv
            div_val = get_combo_value(operand)
            A = A // (2**div_val)
            ip += 2
        elif opcode == 1:  # bxl
            B = B ^ operand
            ip += 2
        elif opcode == 2:  # bst
            val = get_combo_value(operand)
            B = val % 8
            ip += 2
        elif opcode == 3:  # jnz
            if A != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            B = B ^ C
            ip += 2
        elif opcode == 5:  # out
            val = get_combo_value(operand)
            output_values.append(val % 8)
            ip += 2
        elif opcode == 6:  # bdv
            div_val = get_combo_value(operand)
            B = A // (2**div_val)
            ip += 2
        elif opcode == 7:  # cdv
            div_val = get_combo_value(operand)
            C = A // (2**div_val)
            ip += 2
        else:
            raise ValueError(f"Invalid opcode encountered: {opcode}")

    return output_values


def find_min_A_for_self_output(B, C, program):
    # We'll do exponential search first
    # Start from 1 and go up by a factor of 10 each time until we find a match
    # Keep track of the last non-matching A
    last_non_match_A = 0
    test_A = 1
    target_output = program

    # Exponential search
    while True:
        print(f"Testing A = {test_A}")
        candidate_output = run_3bit_computer(test_A, B, C, program)
        if candidate_output == target_output:
            # Found a match at test_A
            # Now do binary search between last_non_match_A and test_A
            low = last_non_match_A
            high = test_A
            break
        else:
            # No match, move on
            last_non_match_A = test_A
            test_A *= 10
            # If we reach some absurdly large number without match, consider a safeguard break
            # but per puzzle conditions we assume a match eventually

    # Binary search to find the minimal A
    while low + 1 < high:
        mid = (low + high) // 2
        candidate_output = run_3bit_computer(mid, B, C, program)
        if candidate_output == target_output:
            high = mid  # match found, try smaller A
        else:
            low = mid  # no match, increase A

    # High should now be the smallest A producing the match
    return high


if __name__ == "__main__":
    file_path = "inputs/input_day16.txt"  # Ensure this path is correct

    # Parse the input file
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    initial_A = None
    initial_B = None
    initial_C = None
    program = None

    for line in lines:
        if line.startswith("Register A:"):
            initial_A = int(line.split(":")[1].strip())
        elif line.startswith("Register B:"):
            initial_B = int(line.split(":")[1].strip())
        elif line.startswith("Register C:"):
            initial_C = int(line.split(":")[1].strip())
        elif line.startswith("Program:"):
            prog_str = line.split(":")[1].strip()
            program = [int(x) for x in prog_str.split(",")]

    if initial_A is None or initial_B is None or initial_C is None or program is None:
        raise ValueError("Input file does not contain the required format.")

    # Part 1: Run with given initial registers
    part1_output = run_3bit_computer(initial_A, initial_B, initial_C, program)
    part1_result = ",".join(map(str, part1_output))
    print("Part 1 Output:", part1_result)

    # Part 2: Find the lowest positive A that outputs a copy of the program
    part2_result = find_min_A_for_self_output(initial_B, initial_C, program)

    # Print both part 1 and part 2 results
    print("Part 2 Lowest Positive A:", part2_result)
