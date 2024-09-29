import heapq
import random

def a_star_fn(start_state):
    class Node:
        def __init__(self, state, parent=None, g=0, h=0):
            self.state = state
            self.parent = parent
            self.g = g 
            self.h = h  
            self.f = g + h 

        def __lt__(self, other):
            return self.f < other.f

    def calculate_heuristic(state, end):
        h = 0
        for i in range(len(state)):
            if state[i] != 0:

                target_index = end.index(state[i])

                target_row, target_col = divmod(target_index, 3)
                curr_row, curr_col = divmod(i, 3)
                h += abs(curr_row - target_row) + abs(curr_col - target_col)
        return h

    def find_successors(node, end):
        successors = []
        zero_index = node.state.index(0)

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_row = zero_index // 3 + dr
            new_col = zero_index % 3 + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col

                new_state = node.state[:]
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]

                g = node.g + 1
                h = calculate_heuristic(new_state, end)

                successors.append(Node(new_state, node, g, h))
        return successors

    def reconstruct_path(node):
        path = []
        while node:

            path.append(node.state)
            node = node.parent

        return path[::-1]

    current_node = Node(start_state)

    for _ in range(20):
        successors = find_successors(current_node, start_state)

        if successors:
            current_node = random.choice(successors)

    end = current_node.state
    print(f"Generated Goal State: {end}")

    start_node = Node(start_state, None, 0, calculate_heuristic(start_state, end))
    frontier = []

    heapq.heappush(frontier, start_node)
    visited = set()

    while frontier:
        current_node = heapq.heappop(frontier)
        visited.add(tuple(current_node.state))

        if current_node.state == end:
            return reconstruct_path(current_node)

        for successor in find_successors(current_node, end):
            if tuple(successor.state) not in visited:
                heapq.heappush(frontier, successor)

    return None

start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

solution = a_star_fn(start_state)

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
