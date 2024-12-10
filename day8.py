from collections import defaultdict


def load_grid(file_path):
    """Load the grid from the input file."""
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file]


def find_antennas(grid):
    """Find all antennas and group them by frequency."""
    antennas = defaultdict(list)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != ".":
                antennas[cell].append((x, y))
    return antennas


def calculate_antinodes(grid, antennas):
    """
    Calculate antinodes for Part 1 rules:
    - Antinodes occur at points perfectly in line with two antennas of the same frequency,
      and one antenna is twice as far from the other.
    """
    antinodes = set()
    height, width = len(grid), len(grid[0])

    for _, positions in antennas.items():
        for i, (x1, y1) in enumerate(positions):
            for x2, y2 in positions[i + 1 :]:
                dx, dy = x2 - x1, y2 - y1

                # Check left side antinode
                ax, ay = x1 - dx, y1 - dy
                if 0 <= ax < width and 0 <= ay < height:
                    antinodes.add((ax, ay))

                # Check right side antinode
                ax, ay = x2 + dx, y2 + dy
                if 0 <= ax < width and 0 <= ay < height:
                    antinodes.add((ax, ay))

    return len(antinodes)


def calculate_antinodes2(grid, antennas):
    """
    Calculate antinodes for Part 2 rules:
    - Antinodes occur at any position in line with at least two antennas of the same frequency.
    - Positions occupied by antennas themselves are also antinodes if in line with others.
    """
    antinodes = set()
    height, width = len(grid), len(grid[0])

    for _, positions in antennas.items():
        for i, (x1, y1) in enumerate(positions):
            for j, (x2, y2) in enumerate(positions):
                if i >= j:  # Avoid duplicate calculations
                    continue

                dx, dy = x2 - x1, y2 - y1

                # Include the two antennas as antinodes
                antinodes.add((x1, y1))
                antinodes.add((x2, y2))

                # Extend line in both directions to find antinodes
                k = 1
                while True:
                    ax, ay = x1 - k * dx, y1 - k * dy  # Backward direction
                    if 0 <= ax < width and 0 <= ay < height:
                        antinodes.add((ax, ay))
                    else:
                        break
                    k += 1

                k = 1
                while True:
                    ax, ay = x2 + k * dx, y2 + k * dy  # Forward direction
                    if 0 <= ax < width and 0 <= ay < height:
                        antinodes.add((ax, ay))
                    else:
                        break
                    k += 1

    return len(antinodes)


def main():
    file_path = "inputs/day8_input.txt"
    grid = load_grid(file_path)

    # Find antennas grouped by frequency
    antennas = find_antennas(grid)

    # Part 1
    part1_count = calculate_antinodes(grid, antennas)
    print(f"Part 1: {part1_count}")

    # Part 2
    part2_count = calculate_antinodes2(grid, antennas)
    print(f"Part 2: {part2_count}")


if __name__ == "__main__":
    main()
