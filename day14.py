import heapq

def parse_maze(file_path):
    with open(file_path, 'r') as f:
        maze = [list(line.rstrip('\n')) for line in f]
    return maze

def find_positions(maze):
    start = None
    end = None
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == 'S':
                start = (r, c)
            elif val == 'E':
                end = (r, c)
    return start, end

def dijkstra_min_cost(maze):
    start, end = find_positions(maze)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    start_state = (start[0], start[1], 1)  # row, col, direction (0:N,1:E,2:S,3:W)
    visited = {}
    pq = []
    heapq.heappush(pq, (0, start_state))
    visited[start_state] = 0

    while pq:
        cost, (r, c, d) = heapq.heappop(pq)
        if (r, c) == end:
            # Once we pop a state at end, this is the minimal cost to reach end with that direction
            # We continue to ensure all minimal states are recorded, but this ensures minimal cost found.
            # Actually, we can't just return here because we need visited states for part 2.
            pass

        if cost > visited.get((r, c, d), float('inf')):
            continue

        # Rotate left
        left_dir = (d - 1) % 4
        new_cost = cost + 1000
        if new_cost < visited.get((r, c, left_dir), float('inf')):
            visited[(r, c, left_dir)] = new_cost
            heapq.heappush(pq, (new_cost, (r, c, left_dir)))

        # Rotate right
        right_dir = (d + 1) % 4
        new_cost = cost + 1000
        if new_cost < visited.get((r, c, right_dir), float('inf')):
            visited[(r, c, right_dir)] = new_cost
            heapq.heappush(pq, (new_cost, (r, c, right_dir)))

        # Move forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] != '#':
            new_cost = cost + 1
            if new_cost < visited.get((nr, nc, d), float('inf')):
                visited[(nr, nc, d)] = new_cost
                heapq.heappush(pq, (new_cost, (nr, nc, d)))

    # Find minimal cost to reach end from visited
    min_cost_end = float('inf')
    for d in range(4):
        if (end[0], end[1], d) in visited:
            if visited[(end[0], end[1], d)] < min_cost_end:
                min_cost_end = visited[(end[0], end[1], d)]

    return visited, min_cost_end, start, end

def backtrack_minimal_paths(maze, visited, min_cost_end, start, end):
    # Directions: N=0,E=1,S=2,W=3
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # From the end tile, we consider all directions that achieve min_cost_end
    end_states = []
    for d in range(4):
        if visited.get((end[0], end[1], d), float('inf')) == min_cost_end:
            end_states.append((end[0], end[1], d))

    # We'll do a backward search:
    # A state (r,c,d) is part of a minimal path if:
    # There exists a next state that is also minimal and the cost matches the forward move or rotation cost.
    # next states -> current states (reverse):
    # Forward move cost is 1, rotation cost is 1000.
    # For backward:
    # From (r,c,d):
    #   Potential predecessors:
    #   1) Forward predecessor (if we moved forward to get here):
    #      If we are currently at (r,c,d), then the previous position would be (r - dr, c - dc, d)
    #      with cost(prev) + 1 = cost(current).
    #   2) Rotation predecessors (if we rotated to get current direction d from d'):
    #      If we are at (r,c,d), then a predecessor could be (r,c,d-1 mod 4) or (r,c,d+1 mod 4)
    #      with cost(prev) + 1000 = cost(current).

    queue = end_states[:]
    minimal_states = set(end_states)

    while queue:
        r, c, d = queue.pop()
        cur_cost = visited[(r, c, d)]

        # Check forward predecessor
        dr, dc = directions[d]
        prev_r, prev_c = r - dr, c - dc
        if 0 <= prev_r < len(maze) and 0 <= prev_c < len(maze[0]) and maze[prev_r][prev_c] != '#':
            prev_state = (prev_r, prev_c, d)
            if prev_state in visited and visited[prev_state] + 1 == cur_cost:
                if prev_state not in minimal_states:
                    minimal_states.add(prev_state)
                    queue.append(prev_state)

        # Check rotation predecessors
        # If current direction is d, predecessor could have direction d-1 or d+1 (mod 4)
        left_dir = (d - 1) % 4
        right_dir = (d + 1) % 4
        left_state = (r, c, left_dir)
        right_state = (r, c, right_dir)

        if left_state in visited and visited[left_state] + 1000 == cur_cost:
            if left_state not in minimal_states:
                minimal_states.add(left_state)
                queue.append(left_state)

        if right_state in visited and visited[right_state] + 1000 == cur_cost:
            if right_state not in minimal_states:
                minimal_states.add(right_state)
                queue.append(right_state)

    # Extract all minimal tiles (r,c) from minimal states
    minimal_tiles = set((r, c) for (r, c, d) in minimal_states)
    return minimal_tiles

def solve_part1(file_path):
    maze = parse_maze(file_path)
    visited, min_cost_end, start, end = dijkstra_min_cost(maze)
    return min_cost_end

def solve_part2(file_path):
    maze = parse_maze(file_path)
    visited, min_cost_end, start, end = dijkstra_min_cost(maze)
    minimal_tiles = backtrack_minimal_paths(maze, visited, min_cost_end, start, end)
    return len(minimal_tiles)

if __name__ == "__main__":
    file_path = "inputs/input_day14.txt"
    # Part 1 result
    part1_result = solve_part1(file_path)
    print("Part 1 result:", part1_result)

    # Part 2 result
    part2_result = solve_part2(file_path)
    print("Part 2 result:", part2_result)
