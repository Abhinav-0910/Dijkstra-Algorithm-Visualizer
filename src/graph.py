import random

class Graph:
    def __init__(self):
        self.edges = {}
        self.positions = {}

    def add_node(self, node):
        if node not in self.edges:
            self.edges[node] = {}
        if node not in self.positions:
            self.positions[node] = (random.random(), random.random())

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.edges[node1][node2] = weight
        self.edges[node2][node1] = weight  # Assuming undirected graph

    def get_nodes(self):
        return list(self.edges.keys())

    def get_neighbors(self, node):
        return list(self.edges[node].keys())

    def get_edge_weight(self, node1, node2):
        return self.edges[node1][node2]

    def get_edges(self):
        edges = set()
        for node1 in self.edges:
            for node2, weight in self.edges[node1].items():
                edges.add((node1, node2, weight))
        return edges

    def has_edge(self, node1, node2):
        return node2 in self.edges.get(node1, {})

    def get_positions(self):
        return self.positions

    def set_position(self, node, pos):
        self.positions[node] = pos
        