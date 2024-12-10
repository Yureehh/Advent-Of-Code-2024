# Input path
input_path = "inputs/day2_input.txt"

max_difference = 3


# Function to check if a level is safe (ascending or descending with constraints)
def is_safe_level(level):
    ascending = True
    descending = True
    for i in range(1, len(level)):
        diff = level[i] - level[i - 1]
        if diff <= 0 or diff > max_difference:
            ascending = False
        if diff >= 0 or -diff > max_difference:
            descending = False
        if not ascending and not descending:
            return False  # Early exit if neither condition is met
    return True


# Function to check if a level is safe with one element removed
def is_safe_level_with_dampener(level):
    for i in range(len(level)):
        new_level = level[:i] + level[i + 1 :]  # Remove one element
        if is_safe_level(new_level):
            return True
    return False


# Read levels into a list for reusability
with open(input_path) as f:
    levels = [
        [int(x) for x in line.split() if x] for line in f
    ]  # Preprocess lines into lists of integers

# Calculate safe levels
safe_levels_count = sum(is_safe_level(level) for level in levels)
safe_levels_count_with_dampener = sum(
    is_safe_level_with_dampener(level) for level in levels
)

print(f"Safe Levels Count: {safe_levels_count}")
print(f"Safe Levels Count with Dampener: {safe_levels_count_with_dampener}")
