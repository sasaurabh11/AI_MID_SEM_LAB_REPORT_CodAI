import heapq

class Node:
    def __init__(self, p, g, h):
        self.p = p  
        self.g = g  
        self.h = h 
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(s, g, grid):
    open_set = []
    closed_set = set()
    start_node = Node(s, 0, heuristic(s, g))
    heapq.heappush(open_set, start_node)
    came_from = {}

    while open_set:
        curr_node = heapq.heappop(open_set)

        if curr_node.p == g:
            return reconstruct_path(came_from, curr_node.p)

        closed_set.add(curr_node.p)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n_p = (curr_node.p[0] + dx, curr_node.p[1] + dy)

            if (0 <= n_p[0] < len(grid) and
                0 <= n_p[1] < len(grid[0]) and
                grid[n_p[0]][n_p[1]] == 0 and
                n_p not in closed_set):

                g_score = curr_node.g + 1
                h_score = heuristic(n_p, g)
                n_node = Node(n_p, g_score, h_score)

                if not any(open_node.p == n_p and open_node.g <= g_score for open_node in open_set):
                    heapq.heappush(open_set, n_node)
                    came_from[n_p] = curr_node.p

    return None

def reconstruct_path(came_from, curr):
    total_path = [curr]
    while curr in came_from:
        curr = came_from[curr]
        total_path.append(curr)
    return total_path[::-1]

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
]

s = (0, 0) 
g = (4, 4)

path = a_star(s, g, grid)

print("Path from start to goal :", path)
