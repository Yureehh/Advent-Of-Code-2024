import concurrent.futures
import copy

# Input path
input_path = "inputs/day6_input.txt"


def load_grid(input_path):
    with open(input_path, "r") as file:
        return [list(line.rstrip("\n")) for line in file.readlines()]


def count_positions_visited(grid):
    rows = len(grid)
    cols = len(grid[0])

    direction_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    start_row, start_col = None, None
    start_direction = None

    # Find start
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in direction_map:
                start_row, start_col = r, c
                start_direction = direction_map[grid[r][c]]
                # Make this cell walkable
                grid[r][c] = "."
                break
        if start_row is not None:
            break

    # Check if start was found
    if start_row is None or start_col is None:
        # No starting position found; possibly blocked
        print("Warning: No starting position found in the grid.")
        return 0

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    try:
        dir_index = directions.index(start_direction)
    except ValueError:
        # If start_direction is not in directions, default to North
        dir_index = 0
        print("Start direction not found in directions. Defaulting to North.")

    visited = set()
    visited.add((start_row, start_col))
    current_row, current_col = start_row, start_col

    def is_forward_status(r, c, dr, dc):
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            return "out_of_bounds"
        if grid[nr][nc] == "#":
            return "blocked"
        return "clear"

    while True:
        dr, dc = directions[dir_index]
        forward_status = is_forward_status(current_row, current_col, dr, dc)

        if forward_status == "out_of_bounds":
            # Guard leaves grid
            break

        steps_turned = 0
        while forward_status == "blocked":
            dir_index = (dir_index + 1) % 4
            dr, dc = directions[dir_index]
            forward_status = is_forward_status(current_row, current_col, dr, dc)
            steps_turned += 1
            if steps_turned == 4:
                # Stuck in place
                print(f"Guard is stuck at ({current_row}, {current_col})")
                return len(visited)

        if forward_status == "out_of_bounds":
            print(
                f"Guard leaves the grid from ({current_row}, {current_col}) moving ({dr}, {dc})"
            )
            break

        # Move forward
        current_row += dr
        current_col += dc
        visited.add((current_row, current_col))
        # print(f"Guard moved to ({current_row}, {current_col})")

    return len(visited)


def count_loop_positions(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_chars = "^>v<"

    # Find start position and direction
    start_pos = next(
        (r, c) for r in range(rows) for c in range(cols) if grid[r][c] in "^v<>"
    )
    start_dir = dir_chars.index(grid[start_pos[0]][start_pos[1]])

    # Initialize variables
    pos = start_pos
    dir_index = start_dir
    visited = {}
    step = 0

    # Simulate guard's movement
    while 0 <= pos[0] < rows and 0 <= pos[1] < cols:
        if pos in visited:
            break
        visited[pos] = (step, dir_index)

        # Check forward
        next_pos = (
            pos[0] + directions[dir_index][0],
            pos[1] + directions[dir_index][1],
        )
        if (
            next_pos[0] < 0
            or next_pos[0] >= rows
            or next_pos[1] < 0
            or next_pos[1] >= cols
            or grid[next_pos[0]][next_pos[1]] == "#"
        ):
            dir_index = (dir_index + 1) % 4
        else:
            pos = next_pos

        step += 1

    # Find loop-causing positions
    loop_positions = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "." and (r, c) != start_pos:
                for d in range(4):
                    next_pos = (r + directions[d][0], c + directions[d][1])
                    if next_pos in visited:
                        prev_step, prev_dir = visited[next_pos]
                        if (prev_dir + 1) % 4 == d:
                            loop_positions.add((r, c))
                            break

    return len(loop_positions)


def main():
    # Part 1
    print("Starting Part 1...")
    original_grid = load_grid(input_path)
    total_positions_visited = count_positions_visited(original_grid)
    print("Total positions visited (Part One):", total_positions_visited)

    # Part 2
    print("\nStarting Part 2...")
    original_grid = load_grid(input_path)
    loop_positions_count = count_loop_positions(original_grid)
    print("Total loop-causing obstruction positions (Part Two):", loop_positions_count)


if __name__ == "__main__":
    main()
