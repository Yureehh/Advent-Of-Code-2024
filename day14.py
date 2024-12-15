def parse_robot_line(line):
    parts = line.strip().split()
    # Extract position
    p_part = parts[0].split("=")[1]
    px, py = p_part.split(",")
    px, py = int(px), int(py)

    # Extract velocity
    v_part = parts[1].split("=")[1]
    vx, vy = v_part.split(",")
    vx, vy = int(vx), int(vy)
    return px, py, vx, vy


def load_robots(file_path):
    robots = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                px, py, vx, vy = parse_robot_line(line)
                robots.append((px, py, vx, vy))
    return robots


def positions_at_time(robots, width, height, t):
    """
    Compute the final wrapped positions of all robots at a given time t.
    """
    return [((px + vx * t) % width, (py + vy * t) % height) for (px, py, vx, vy) in robots]


def compute_safety_factor_at_time(robots, width, height, t):
    """
    Compute the safety factor after t seconds.
    """
    center_x = width // 2
    center_y = height // 2

    quadrant_counts = [0, 0, 0, 0]  # top-left, top-right, bottom-left, bottom-right
    for (fx, fy) in positions_at_time(robots, width, height, t):
        if fx == center_x or fy == center_y:
            continue
        if fx < center_x and fy < center_y:
            quadrant_counts[0] += 1
        elif fx > center_x and fy < center_y:
            quadrant_counts[1] += 1
        elif fx < center_x and fy > center_y:
            quadrant_counts[2] += 1
        elif fx > center_x and fy > center_y:
            quadrant_counts[3] += 1

    safety_factor = 1
    for c in quadrant_counts:
        safety_factor *= c
    return safety_factor


def find_minimum_bounding_area_time(robots, width, height, max_time=20000, stable_threshold=50):
    pass


def print_pattern(robots, width, height, t):
    """
    Print the pattern of robot positions at time t so we can visualize the arrangement.
    This allows us to 'recognize' if it forms a Christmas tree pattern.
    """
    pos = positions_at_time(robots, width, height, t)
    xs = [p[0] for p in pos]
    ys = [p[1] for p in pos]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    grid_width = max_x - min_x + 1
    grid_height = max_y - min_y + 1

    # Create a 2D grid initialized with '.'
    grid = [["." for _ in range(grid_width)] for _ in range(grid_height)]

    # Place robots
    for (x, y) in pos:
        grid_y = y - min_y
        grid_x = x - min_x
        grid[grid_y][grid_x] = "#"

    # Print the grid row by row (top to bottom)
    for row in range(grid_height):
        print("".join(grid[row]))


if __name__ == "__main__":
    # Configuration
    file_path = "inputs/input_day14.txt"  # Ensure this path is correct
    width = 101
    height = 103
    T = 100  # For part 1

    # Load robots
    robots = load_robots(file_path)

    # Part 1: Compute safety factor after T seconds
    safety_factor = compute_safety_factor_at_time(robots, width, height, T)
    print("Part 1 Safety Factor:", safety_factor)

    # Part 2: Find minimal bounding area time (assumed Christmas tree pattern)
    earliest_time = find_minimum_bounding_area_time(robots, width, height)
    print("Part 2 Earliest Easter Egg (Christmas Tree) Time:", earliest_time)

    # Print the pattern at this time to visually confirm the Christmas tree shape
    print("Visualizing the Christmas Tree pattern at time =", earliest_time)
    print_pattern(robots, width, height, earliest_time)
