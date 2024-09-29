def dfs(start, goal):
    stack = [(start, [])]
    visited = set()

    while stack:
        state, path = stack.pop()

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
                    stack.append((successor, path + [state]))

    return None

start = ('L', 'L', 'L', '_', 'R', 'R', 'R')
goal = ('R', 'R', 'R', '_', 'L', 'L', 'L')

solution_dfs = dfs(start, goal)

print("DFS Solution:")
for step in solution_dfs:
    print(step)
