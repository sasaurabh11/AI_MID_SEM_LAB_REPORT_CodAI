from collections import deque

def search(graph, start, end):
    qu = deque([[start_node] for start_node in start])
    
    while qu:
        path = qu.popleft()
        curr = path[-1]
        if end(curr):
            return path
        
        for nbr in graph.get(curr, []):
            new_path = path + [nbr]

            qu.append(new_path)

    return None

if __name__ == "__main__":
    graph = {}

    num_edges = int(input("Enter number of edges : "))

    for _ in range(num_edges):
        u, v = map(int, input("Enter an edge (start end): ").split())

        if u not in graph:
            graph[u] = []

        graph[u].append(v)
    

    stn = list(map(int, input("Enter start node : ").split()))

    target_node = int(input("Enter target node : "))

    result = search(graph, stn, lambda node: node == target_node)
    
    if result:
        print(f"Path to end : {result}")
    else:
        print("No path to end found.")
