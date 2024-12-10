def load_disk_map(file_path):
    """Load the disk map from the specified file."""
    with open(file_path, "r") as file:
        return file.read().strip()


def parse_disk_map(disk_map):
    """Parse the disk map to identify file sizes and free spaces."""
    return [
        (int(disk_map[i]), int(disk_map[i + 1]) if i + 1 < len(disk_map) else 0)
        for i in range(0, len(disk_map), 2)
    ]


def generate_initial_blocks(segments):
    """Generate initial block representation of files and free spaces."""
    file_blocks = []
    file_id = 0
    for file_length, free_length in segments:
        file_blocks.extend([file_id] * file_length)
        file_blocks.extend(["."] * free_length)
        if file_length > 0:
            file_id += 1
    return file_blocks


def compact_blocks_single_move(file_blocks):
    """Compact file blocks one at a time to the leftmost free space."""
    for i in range(len(file_blocks) - 1, -1, -1):
        if file_blocks[i] != "." and "." in file_blocks[:i]:
            free_index = file_blocks.index(".")
            file_blocks[free_index] = file_blocks[i]
            file_blocks[i] = "."
    return file_blocks


def compact_blocks_whole_file(file_blocks):
    """Compact file blocks by moving whole files to the leftmost span of free space."""
    unique_file_ids = sorted(set(filter(lambda x: x != ".", file_blocks)), reverse=True)

    for file_id in unique_file_ids:
        # Identify the positions of the current file
        file_positions = [i for i, block in enumerate(file_blocks) if block == file_id]

        # Skip if no positions found or no free space to the left of the file
        if not file_positions or all(
            file_blocks[i] != "." for i in range(file_positions[0])
        ):
            continue

        file_size = len(file_positions)
        start_limit = file_positions[
            0
        ]  # The file can only move to spaces left of this position

        # Find the leftmost free span that can fit the file and is entirely to the left
        for start_index in range(start_limit - file_size + 1):
            if all(
                file_blocks[i] == "."
                for i in range(start_index, start_index + file_size)
            ):
                # Move the file to the free span
                for pos in file_positions:
                    file_blocks[pos] = "."
                for i in range(start_index, start_index + file_size):
                    file_blocks[i] = file_id
                break

    return file_blocks


def calculate_checksum(file_blocks):
    """Calculate the checksum of the file system."""
    return sum(
        position * block for position, block in enumerate(file_blocks) if block != "."
    )


def solve_disk_fragmenter(disk_map, compaction_method):
    """Solve the disk fragmenter problem using the given compaction method."""
    segments = parse_disk_map(disk_map)
    file_blocks = generate_initial_blocks(segments)
    compacted_blocks = compaction_method(file_blocks)
    return calculate_checksum(compacted_blocks)


def main():
    file_path = "inputs/input_day9.txt"

    # Load and parse the disk map
    disk_map = load_disk_map(file_path)

    # Part One: Single block moves
    result_part_one = solve_disk_fragmenter(disk_map, compact_blocks_single_move)
    print("Checksum (Part One):", result_part_one)

    # Part Two: Whole file moves
    result_part_two = solve_disk_fragmenter(disk_map, compact_blocks_whole_file)
    print("Checksum (Part Two):", result_part_two)


if __name__ == "__main__":
    main()
