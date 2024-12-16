def parse_input(file_path):
    warehouse_map = []
    moves = []
    with open(file_path, "r") as f:
        lines = [l.rstrip("\n") for l in f.readlines()]

    # Identify map lines (continuous block starting and ending with '#')
    map_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#") and line.endswith("#"):
            map_lines.append(line)
        else:
            break
        i += 1

    warehouse_map = [list(l) for l in map_lines]

    # The rest lines are moves
    for j in range(i, len(lines)):
        moves.extend(list(lines[j]))
    moves = [m for m in moves if m in ["^", "v", "<", ">"]]

    # Find robot
    robot_r, robot_c = None, None
    for r_idx, row in enumerate(warehouse_map):
        for c_idx, val in enumerate(row):
            if val == "@":
                robot_r, robot_c = r_idx, c_idx
                break
        if robot_r is not None:
            break

    return warehouse_map, robot_r, robot_c, moves


def move_robot_part1(warehouse_map, robot_r, robot_c, direction):
    dir_offsets = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    dr, dc = dir_offsets[direction]

    R = len(warehouse_map)
    C = len(warehouse_map[0])
    nr = robot_r + dr
    nc = robot_c + dc

    if warehouse_map[nr][nc] == "#":
        return warehouse_map, robot_r, robot_c

    if warehouse_map[nr][nc] == "O":
        chain_positions = []
        rr, cc = nr, nc
        while 0 <= rr < R and 0 <= cc < C and warehouse_map[rr][cc] == "O":
            chain_positions.append((rr, cc))
            rr += dr
            cc += dc

        if warehouse_map[rr][cc] in ["#", "O"]:
            return warehouse_map, robot_r, robot_c

        chain_positions.reverse()
        for (br, bc) in chain_positions:
            warehouse_map[br + dr][bc + dc] = "O"
            warehouse_map[br][bc] = "."

        warehouse_map[robot_r][robot_c] = "."
        warehouse_map[nr][nc] = "@"
        return warehouse_map, nr, nc
    else:
        # Empty cell
        warehouse_map[robot_r][robot_c] = "."
        warehouse_map[nr][nc] = "@"
        return warehouse_map, nr, nc


def simulate_part1(warehouse_map, robot_r, robot_c, moves):
    for m in moves:
        warehouse_map, robot_r, robot_c = move_robot_part1(warehouse_map, robot_r, robot_c, m)
    return warehouse_map


def compute_gps_sum_part1(warehouse_map):
    R = len(warehouse_map)
    C = len(warehouse_map[0])
    total = 0
    for r in range(R):
        for c in range(C):
            if warehouse_map[r][c] == "O":
                total += 100 * r + c
    return total


def scale_map(warehouse_map, robot_r, robot_c):
    mapping = {
        '#': "##",
        'O': "[]",
        '.': "..",
        '@': "@."
    }

    R = len(warehouse_map)
    C = len(warehouse_map[0])

    # After scaling, each cell is represented by a 2-char string.
    # We'll keep the same R x C dimension, but each cell now contains two chars.
    scaled_map = []
    for r in range(R):
        new_row = []
        for c in range(C):
            cell = warehouse_map[r][c]
            new_row.append(mapping[cell])
        scaled_map.append(new_row)

    return scaled_map, robot_r, robot_c


def move_robot_part2(scaled_map, robot_r, robot_c, direction):
    dir_offsets = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    dr, dc = dir_offsets[direction]

    R = len(scaled_map)
    C = len(scaled_map[0])
    nr = robot_r + dr
    nc = robot_c + dc

    if scaled_map[nr][nc].startswith("#"):
        return scaled_map, robot_r, robot_c

    if scaled_map[nr][nc].startswith("["):
        chain_positions = []
        rr, cc = nr, nc
        while 0 <= rr < R and 0 <= cc < C and scaled_map[rr][cc].startswith("["):
            chain_positions.append((rr, cc))
            rr += dr
            cc += dc

        if scaled_map[rr][cc].startswith("#") or scaled_map[rr][cc].startswith("["):
            return scaled_map, robot_r, robot_c

        chain_positions.reverse()
        for (br, bc) in chain_positions:
            scaled_map[br + dr][bc + dc] = scaled_map[br][bc]
            scaled_map[br][bc] = ".."

        scaled_map[robot_r][robot_c] = ".."
        scaled_map[nr][nc] = "@."
        return scaled_map, nr, nc
    else:
        scaled_map[robot_r][robot_c] = ".."
        scaled_map[nr][nc] = "@."
        return scaled_map, nr, nc


def simulate_part2(scaled_map, robot_r, robot_c, moves):
    for m in moves:
        scaled_map, robot_r, robot_c = move_robot_part2(scaled_map, robot_r, robot_c, m)
    return scaled_map


def compute_gps_sum_part2(scaled_map):
    R = len(scaled_map)
    C = len(scaled_map[0])
    total = 0
    for r in range(R):
        for c in range(C):
            if scaled_map[r][c].startswith("["):
                # According to the puzzle, use 2*c+1 for the horizontal distance
                total += 100 * r + (2 * c + 1)
    return total



if __name__ == "__main__":
    file_path = "inputs/input_day15.txt"  # Ensure this path is correct

    # Part 1
    warehouse_map, robot_r, robot_c, moves = parse_input(file_path)
    final_map_part1 = simulate_part1([row[:] for row in warehouse_map], robot_r, robot_c, moves)
    result_part1 = compute_gps_sum_part1(final_map_part1)
    print("Part 1 Result:", result_part1)

    # Part 2
    scaled_map, scaled_robot_r, scaled_robot_c = scale_map(warehouse_map, robot_r, robot_c)
    final_map_part2 = simulate_part2([row[:] for row in scaled_map], scaled_robot_r, scaled_robot_c, moves)
    result_part2 = compute_gps_sum_part2(final_map_part2)
    print("Part 2 Result:", result_part2)
