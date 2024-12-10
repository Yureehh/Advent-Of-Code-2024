# Input path
input_path = "inputs/day5_input.txt"


def load_rules_and_updates(input_path):
    """
    Load rules and updates from a file. Rules are listed first, followed by updates, separated by a blank line.

    :param input_path: Path to the input file.
    :return: A tuple containing two lists: rules and updates.
    """
    with open(input_path, "r") as file:
        lines = file.read().splitlines()

    separator_index = lines.index("") if "" in lines else len(lines)
    rules = lines[:separator_index]
    updates = lines[separator_index + 1 :]

    return rules, updates


def is_safe_rule(number, right_number, rule_set):
    """
    Check if a rule is safe.

    :param number: The number to check.
    :param right_number: The number to check against.
    :param rule_set: Set of rules for faster lookup.
    :return: True if the rule is safe, False otherwise.
    """
    return f"{right_number}|{number}" not in rule_set


def check_part1(updates, rules):
    """
    Check the updates against the rules for part 1.

    :param updates: List of updates.
    :param rules: List of rules.
    :return: The total value of valid updates.
    """
    rule_set = {rule for rule in rules}  # Use a set for O(1) lookups
    total = 0
    wrong_updates = []

    for update in updates:
        update_values = update.split(",")
        is_update_safe = all(
            is_safe_rule(number, right_number, rule_set)
            for i, number in enumerate(update_values)
            for right_number in update_values[i + 1 :]
        )

        if is_update_safe:
            middle_value = int(update_values[len(update_values) // 2])
            total += middle_value
        else:
            wrong_updates.append(update)

    return total, wrong_updates


# Part 2
def adjust_updates(rules, wrong_updates):
    """
    Adjust the updates based on the rules for part 2, restarting from the same number after adjustments.

    :param rules: List of rules.
    :param wrong_updates: List of wrong updates.
    :return: A tuple containing the adjusted updates and the total of middle values.
    """
    rule_set = {rule for rule in rules}  # Convert rules to a set for fast lookups
    adjusted_updates = []
    total = 0

    for update in wrong_updates:
        update_values = update.split(",")
        i = 0
        while i < len(update_values) - 1:
            number = update_values[i]
            right_number = update_values[i + 1]

            # Check if the current pair violates a rule
            if not is_safe_rule(number, right_number, rule_set):
                # Move the current number just after the right number
                update_values.pop(i)
                update_values.insert(i + 1, number)
                # Restart from the same index
                i = max(0, i - 1)
            else:
                # Move to the next pair
                i += 1

        adjusted_updates.append(",".join(update_values))

    # Sum the middle values of the adjusted updates
    for update in adjusted_updates:
        update_values = update.split(",")
        middle_value = int(update_values[len(update_values) // 2])
        total += middle_value

    return adjusted_updates, total


# Main execution
if __name__ == "__main__":
    rules, updates = load_rules_and_updates(input_path)
    total, wrong_updates = check_part1(updates, rules)
    print(f"Part 1: The total value of valid updates is {total}.")

    adjusted_updates, total = adjust_updates(rules, wrong_updates)
    print(f"Part 2: The total value of valid updates after adjustment is {total}.")
