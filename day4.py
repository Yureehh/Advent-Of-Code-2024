# Input path
import itertools

input_path = "inputs/input_day4.txt"


def is_valid_position(x, y, rows, cols):
    """Check if a position is within the grid boundaries."""
    return 0 <= x < rows and 0 <= y < cols


# Part 1: Count all occurrences of "XMAS"
def count_xmas_occurrences(grid, word="XMAS"):
    directions = [
        (-1, 0),
        (1, 0),  # vertical: up, down
        (0, -1),
        (0, 1),  # horizontal: left, right
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),  # diagonal: all directions
    ]
    word_length = len(word)
    rows, cols = len(grid), len(grid[0])
    count = 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == word[0]:  # Found the starting letter
                for dx, dy in directions:
                    match = True
                    for i in range(word_length):
                        nx, ny = row + dx * i, col + dy * i
                        if not (
                            is_valid_position(nx, ny, rows, cols)
                            and grid[nx][ny] == word[i]
                        ):
                            match = False
                            break
                    if match:
                        count += 1

    return count


# Part 2: Count all occurrences of "X-MAS" pattern
def count_x_mas_occurrences(grid):
    rows, cols = len(grid), len(grid[0])
    return sum(
        bool(
            grid[row][col] == "A"
            and (
                is_valid_position(row - 1, col - 1, rows, cols)
                and grid[row - 1][col - 1] in ("M", "S")
                and is_valid_position(row + 1, col + 1, rows, cols)
                and grid[row + 1][col + 1] in ("M", "S")
                and grid[row - 1][col - 1] != grid[row + 1][col + 1]
            )
            and (
                is_valid_position(row - 1, col + 1, rows, cols)
                and grid[row - 1][col + 1] in ("M", "S")
                and is_valid_position(row + 1, col - 1, rows, cols)
                and grid[row + 1][col - 1] in ("M", "S")
                and grid[row - 1][col + 1] != grid[row + 1][col - 1]
            )
        )
        for row, col in itertools.product(range(1, rows - 1), range(1, cols - 1))
    )


# Load the grid from the file
def load_grid(input_path):
    with open(input_path, "r") as file:
        return [line.strip() for line in file.readlines()]


# Main execution
grid = load_grid(input_path)

# Part 1
total_xmas_occurrences = count_xmas_occurrences(grid)
print("Total occurrences of 'XMAS':", total_xmas_occurrences)

# Part 2
total_x_mas_occurrences = count_x_mas_occurrences(grid)
print("Total occurrences of 'X-MAS':", total_x_mas_occurrences)
