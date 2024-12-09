# Input path
input_path = 'inputs/day6_input.txt'

def load_grid(input_path):
    with open(input_path, 'r') as file:
        return [list(line.rstrip('\n')) for line in file.readlines()]

def count_positions_visited(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Identify the initial position and direction of the guard
    direction_map = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    start_row, start_col = None, None
    start_direction = None

    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if cell in direction_map:
                start_row, start_col = r, c
                start_direction = direction_map[cell]
                # Replace guard symbol with '.' to make it walkable
                grid[r][c] = '.'
                break
        if start_row is not None:
            break

    # Directions in order: up, right, down, left (clockwise)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_index = directions.index(start_direction)

    visited = set()
    visited.add((start_row, start_col))
    current_row, current_col = start_row, start_col

    def is_forward_status(r, c, dr, dc):
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            return "out_of_bounds"
        if grid[nr][nc] == '#':
            return "blocked"
        return "clear"

    while True:
        # Current direction
        dr, dc = directions[dir_index]
        forward_status = is_forward_status(current_row, current_col, dr, dc)

        if forward_status == "out_of_bounds":
            # Guard would leave the grid on next move, so we stop
            break

        # If blocked by an obstacle, turn right until clear or all directions tried
        steps_turned = 0
        while forward_status == "blocked":
            dir_index = (dir_index + 1) % 4
            dr, dc = directions[dir_index]
            forward_status = is_forward_status(current_row, current_col, dr, dc)
            steps_turned += 1
            if steps_turned == 4:
                # No direction possible
                return len(visited)

        # If after turning we find out-of-bounds is next step, break
        if forward_status == "out_of_bounds":
            break

        # Move forward if clear
        current_row += dr
        current_col += dc

        # If we moved successfully inside the grid, add to visited
        visited.add((current_row, current_col))

    return len(visited)

# Part 1
grid = load_grid(input_path)
total_positions_visited = count_positions_visited(grid)
print("Total positions visited:", total_positions_visited)
