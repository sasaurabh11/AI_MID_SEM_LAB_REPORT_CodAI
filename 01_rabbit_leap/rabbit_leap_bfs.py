from collections import deque

def bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path + [state]

        if state in visited:
            continue

        visited.add(state)

        empty_index = state.index('_')
        moves = [-1, 1, -2, 2]

        for move in moves:
            new_index = empty_index + move
            if 0 <= new_index < len(state):
                new_state = list(state)
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                successor = tuple(new_state)
                if successor not in visited:
                    queue.append((successor, path + [state]))

    return None

start = ('L', 'L', 'L', '_', 'R', 'R', 'R')
goal = ('R', 'R', 'R', '_', 'L', 'L', 'L')

solution_bfs = bfs(start, goal)

print("BFS Solution:")
for step in solution_bfs:
    print(step)
