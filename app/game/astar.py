import heapq

def astar(grid, start, goal):
    """
    A* pathfinding algorithm for a grid.

    Args:
        grid: 2D list where 0 = walkable, 1 = blocked (obstacle).
        start: (x, y) tuple for the starting position.
        goal: (x, y) tuple for the target position.

    Returns:
        List of (x, y) tuples representing the path, or an empty list if no path found.
    """
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Cardinal directions (no diagonals)


    def heuristic(a, b):
        """Calculate Manhattan distance as the heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def is_valid(pos):
        """Check if a position is within bounds and walkable."""
        x, y = pos
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0


    open_set = []
    heapq.heappush(open_set, (0, start))

    g_cost = {start: 0}
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if not is_valid(neighbor):
                continue

            tentative_g_cost = g_cost[current] + 1

            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_cost, neighbor))
                came_from[neighbor] = current

    return []
