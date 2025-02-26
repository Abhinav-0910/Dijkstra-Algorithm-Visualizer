def dijkstra(graph, start_node):
    distances = {node: float('infinity') for node in graph.get_nodes()}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph.get_nodes()}
    unvisited = list(graph.get_nodes())

    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current_node)

        if distances[current_node] == float('infinity'):
            break

        for neighbor in graph.get_neighbors(current_node):
            weight = graph.get_edge_weight(current_node, neighbor)
            tentative_distance = distances[current_node] + weight

            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                previous_nodes[neighbor] = current_node

    return distances, previous_nodes