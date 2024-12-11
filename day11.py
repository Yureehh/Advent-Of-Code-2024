from collections import Counter

def load_stones(file_path):
    """Load the stones from the input file."""
    with open(file_path, "r") as file:
        stones = file.read().strip().split()
    return Counter(stones)  # Use Counter to keep track of stone counts

def transform_stones(stone_counts):
    """Transform the stones according to the rules, optimized with a Counter."""
    new_counts = Counter()

    for stone, count in stone_counts.items():
        if stone == "0":
            # Rule 1: Replace "0" with "1"
            new_counts["1"] += count
        else:
            length = len(stone)
            if length % 2 == 0:
                # Rule 2: Split even-length stone into two halves
                half = length // 2
                left_str = str(int(stone[:half]))
                right_str = str(int(stone[half:]))
                new_counts[left_str] += count
                new_counts[right_str] += count
            else:
                # Rule 3: Multiply by 2024
                val = int(stone)
                new_val = str(val * 2024)
                new_counts[new_val] += count

    return new_counts

def main():
    file_path = "inputs/input_day11.txt"
    stone_counts = load_stones(file_path)

    # Apply transformations 75 times
    for _ in range(75):
        stone_counts = transform_stones(stone_counts)

    # Calculate the total number of stones
    total_stones = sum(stone_counts.values())
    print(total_stones)

if __name__ == "__main__":
    main()
