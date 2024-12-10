def load_grid(file_path):
    with open(file_path, "r") as file:
        return [list(map(int, list(line.strip()))) for line in file]


def get_neighbors(r, c, rows, cols):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def find_reachable_nines(grid, start_r, start_c):
    """Part One BFS: Returns count of unique 9-cells reachable from (start_r, start_c)"""
    rows = len(grid)
    cols = len(grid[0])
    from collections import deque

    queue = deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    reachable_nines = set()

    while queue:
        r, c = queue.popleft()
        if grid[r][c] == 9:
            reachable_nines.add((r, c))
            # continue checking other paths as other 9s may be reachable
            continue

        current_height = grid[r][c]
        next_height = current_height + 1
        for nr, nc in get_neighbors(r, c, rows, cols):
            if grid[nr][nc] == next_height and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return len(reachable_nines)


def part_one_score(grid):
    rows = len(grid)
    cols = len(grid[0])
    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    total_score = 0
    for r, c in trailheads:
        score = find_reachable_nines(grid, r, c)
        total_score += score
    return total_score


def part_two_score(grid):
    """Count total distinct paths starting from each trailhead to any 9"""
    rows = len(grid)
    cols = len(grid[0])
    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    from functools import lru_cache

    @lru_cache(None)
    def count_paths(r, c):
        if grid[r][c] == 9:
            return 1
        current_height = grid[r][c]
        total = 0
        for nr, nc in get_neighbors(r, c, rows, cols):
            if grid[nr][nc] == current_height + 1:
                total += count_paths(nr, nc)
        return total

    total_rating = 0
    for r, c in trailheads:
        total_rating += count_paths(r, c)
    return total_rating


def main():
    file_path = "inputs/input_day10.txt"
    grid = load_grid(file_path)

    # Part One:
    score_part_one = part_one_score(grid)
    print(score_part_one)

    # Part Two:
    score_part_two = part_two_score(grid)
    print(score_part_two)


if __name__ == "__main__":
    main()
