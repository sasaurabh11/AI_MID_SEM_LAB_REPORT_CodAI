def solve_missionaries_and_cannibals_dfs(start, end):
    from collections import deque

    def check(state):
        missionaries, cannibals, _ = state
        return not (missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3 or 
                    (missionaries > 0 and missionaries < cannibals) or 
                    (3 - missionaries > 0 and 3 - missionaries < 3 - cannibals))

    def dfs(state, path):
        if state == end:
            return path

        path.append(state)

        successors = []
        missionaries, cannibals, boat = state
        moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]

        if boat == 1:
            for move in moves:
                new_state = (missionaries - move[0], cannibals - move[1], 0)
                if check(new_state) and new_state not in path:
                    successors.append(new_state)

        else:
            for move in moves:
                new_state = (missionaries + move[0], cannibals + move[1], 1)
                if check(new_state) and new_state not in path:
                    successors.append(new_state)


        for succ in successors:
            result = dfs(succ, path.copy())
            if result is not None:
                return result
        
        return None

    return dfs(start, [])

start = (3, 3, 1)
end = (0, 0, 0)

solve = solve_missionaries_and_cannibals_dfs(start, end)

if solve:
    print("Solution: ")
    for step in solve:
        print(step)
else:
    print("No solution found.")
