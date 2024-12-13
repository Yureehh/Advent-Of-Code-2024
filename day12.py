def load_grid(file_path):
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file]


def get_neighbors(x, y, grid):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append((nx, ny))
    return neighbors


def explore_region(x, y, grid, visited):
    stack = [(x, y)]
    region_area = 0
    region_perimeter = 0
    region_char = grid[x][y]

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        region_area += 1

        for nx, ny in get_neighbors(cx, cy, grid):
            if grid[nx][ny] == region_char:
                if (nx, ny) not in visited:
                    stack.append((nx, ny))
            else:
                region_perimeter += 1

        # Check border edges since the neighbors are not considered if they are outside the grid
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                region_perimeter += 1

    return region_area, region_perimeter


def calculate_total_price(grid):
    visited = set()
    total_price = 0

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) not in visited:
                area, perimeter = explore_region(x, y, grid, visited)
                price = area * perimeter
                total_price += price

    return total_price


def main():
    file_path = "inputs/input_day12.txt"
    grid = load_grid(file_path)

    # Calculate the total price of fencing all regions
    total_price = calculate_total_price(grid)
    print(f"Total price of fencing all regions: {total_price}")


if __name__ == "__main__":
    main()
