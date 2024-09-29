from collections import deque

def solve_missionaries_and_cannibals(start, end):

    def check(state):
        missionaries, cannibals
        return not (missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3 or 
                    (missionaries > 0 and missionaries < cannibals) or 
                    (3 - missionaries > 0 and 3 - missionaries < 3 - cannibals))

    qe = deque([(start, [])])
    visited = set()
    
    while qe:
        (state, path) = qe.popleft()
        
        if state in visited:
            continue

        visited.add(state)
        path = path + [state]

        if state == end:
            return path

        par = []
        missionaries, cannibals, boat = state
        moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
        
        index = 0
        if boat == 1:
            while index < len(moves):
                move = moves[index]
                new_state = (missionaries - move[0], cannibals - move[1], 0)
                if check(new_state):
                    par.append(new_state)
                index += 1

        else:
            while index < len(moves):
                move = moves[index]
                new_state = (missionaries + move[0], cannibals + move[1], 1)
                if check(new_state):
                    par.append(new_state)
                index += 1

        index = 0
        while index < len(par):
            qe.append((par[index], path))
            index += 1
            
    return None

start = (3, 3, 1)
end = (0, 0, 0)

solve = solve_missionaries_and_cannibals(start, end)

if solve:
    print("Solution: ")
    for step in solve:
        print(step)
else:
    print("Error.")
