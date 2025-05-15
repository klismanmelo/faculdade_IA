import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, cost_map, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current, path = heapq.heappop(open_set)

        if current == goal:
            return path

        visited.add(current)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if (0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and
                maze[ny][nx] != '#' and neighbor not in visited):

                tile = maze[ny][nx]
                cost = cost_map.get(tile, 1)
                tentative_g = g_score[current] + cost

                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))

    return []
