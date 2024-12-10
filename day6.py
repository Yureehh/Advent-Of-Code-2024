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
                print(
                    f"Found start at ({start_row}, {start_col}) with direction {grid[start_row][start_col]}"
                )
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
        print(f"Start direction index: {dir_index}")
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
            print(
                f"Guard leaves the grid from ({current_row}, {current_col}) moving ({dr}, {dc})"
            )
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


def run_with_timeout(func, args=(), kwargs=None, timeout=5):
    """
    Run a function with a timeout. If it doesn't complete within 'timeout' seconds, raise TimeoutError.

    This implementation uses ProcessPoolExecutor for cross-platform compatibility.
    """
    if kwargs is None:
        kwargs = {}

    # Make a deep copy of the grid to avoid shared state issues
    args = list(args)
    for i, arg in enumerate(args):
        if isinstance(arg, list):
            args[i] = copy.deepcopy(arg)
    if "grid" in kwargs:
        kwargs["grid"] = copy.deepcopy(kwargs["grid"])

    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise TimeoutError("Function call timed out")


def count_loop_positions(grid):
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
                print(
                    f"Start found at ({start_row}, {start_col}) with direction {grid[start_row][start_col]}"
                )
                break
        if start_row is not None:
            break

    if start_row is None or start_direction is None:
        print("No starting position found in the grid.")
        return 0

    loop_count = 0
    total_cells = sum(row.count(".") for row in grid)
    processed_cells = 0

    # For each '.' cell except the start, place '#' and run count_positions_visited with a timeout
    for r in range(rows):
        for c in range(cols):
            if (r, c) == (start_row, start_col):
                continue
            if grid[r][c] == ".":
                # Make a copy of the grid to modify
                grid_copy = copy.deepcopy(grid)
                # Temporarily place obstacle
                grid_copy[r][c] = "#"
                try:
                    # Run count_positions_visited with a timeout
                    run_with_timeout(
                        count_positions_visited, args=(grid_copy,), timeout=5
                    )
                    print(f"Processed cell ({r}, {c}) without loop.")
                except TimeoutError:
                    # Timeout means infinite loop detected
                    loop_count += 1
                    print(f"Detected loop-causing obstruction at ({r}, {c}).")
                except Exception as e:
                    # Handle other exceptions if necessary
                    print(f"Error processing cell ({r}, {c}): {e}")
                processed_cells += 1
                print(f"Progress: {processed_cells}/{total_cells} cells processed.")
    return loop_count


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
