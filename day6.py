import concurrent.futures
import copy

input_path = "inputs/input_day6.txt"

def load_grid(input_path):
    with open(input_path, "r") as file:
        return [list(line.rstrip("\n")) for line in file.readlines()]


def find_start_and_direction(grid):
    """Find the guard's starting position and direction."""
    directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in directions:
                start_direction = directions[grid[r][c]]
                return r, c, start_direction
    return None, None, None


def simulate_guard(grid):
    """
    Simulate the guard's movement and return:
    - A dictionary with:
      'stuck': bool (True if guard loops/stuck, False otherwise)
      'visited_count': number of distinct positions visited
    """
    rows = len(grid)
    cols = len(grid[0])

    start_row, start_col, start_direction = find_start_and_direction(grid)
    if start_row is None:
        # No start found
        return {'stuck': False, 'visited_count': 0}

    # Make starting cell walkable
    grid[start_row][start_col] = "."

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    if start_direction in directions:
        dir_index = directions.index(start_direction)
    else:
        dir_index = 0  # Default to north if not found

    visited_positions = set()  # for visited cells
    visited_positions.add((start_row, start_col))

    # Track states: (row, col, dir_index)
    # If we hit the same state twice, we're in a loop.
    visited_states = set()
    visited_states.add((start_row, start_col, dir_index))

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
            return {'stuck': False, 'visited_count': len(visited_positions)}

        steps_turned = 0
        # Turn right while blocked
        while forward_status == "blocked":
            dir_index = (dir_index + 1) % 4
            dr, dc = directions[dir_index]
            forward_status = is_forward_status(current_row, current_col, dr, dc)
            steps_turned += 1
            if steps_turned == 4:
                # Stuck in place (no direction to go)
                return {'stuck': True, 'visited_count': len(visited_positions)}

        if forward_status == "out_of_bounds":
            # Guard leaves grid
            return {'stuck': False, 'visited_count': len(visited_positions)}

        # Move forward
        current_row += dr
        current_col += dc
        visited_positions.add((current_row, current_col))

        # Check for looping state
        current_state = (current_row, current_col, dir_index)
        if current_state in visited_states:
            # We've been here facing the same direction before -> loop
            return {'stuck': True, 'visited_count': len(visited_positions)}
        visited_states.add(current_state)

def count_positions_visited(grid):
    """Part One: How many distinct positions will the guard visit before leaving?"""
    sim_result = simulate_guard(copy.deepcopy(grid))
    return sim_result['visited_count']


def find_valid_obstruction_positions(grid):
    """
    Find all possible positions to place a new obstruction:
    - It cannot be placed on the guard's starting position.
    - It must be placed on a '.' cell.
    """
    rows = len(grid)
    cols = len(grid[0])
    start_row, start_col, _ = find_start_and_direction(grid)
    valid_positions = []
    for r in range(rows):
        for c in range(cols):
            # Must be a free cell and not the start
            if (r, c) != (start_row, start_col) and grid[r][c] == ".":
                valid_positions.append((r, c))
    return valid_positions


def does_obstruction_cause_loop(grid, r, c):
    """
    Place a single obstruction at (r, c) and check if guard gets stuck in a loop.
    Return True if placing obstruction causes a loop, False otherwise.
    """
    test_grid = copy.deepcopy(grid)
    test_grid[r][c] = "#"
    sim_result = simulate_guard(test_grid)
    return sim_result['stuck']


def count_loop_positions(original_grid):
    """
    Part Two:
    Count how many distinct positions you could place a single new obstruction
    such that the guard will get stuck in a loop.
    """
    valid_positions = find_valid_obstruction_positions(original_grid)
    loop_count = 0

    # Parallelize to speed up if large grids
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(does_obstruction_cause_loop, original_grid, r, c)
                   for r, c in valid_positions]
        for future in concurrent.futures.as_completed(futures):
            print("Starting future number", loop_count)
            if future.result():
                loop_count += 1

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
