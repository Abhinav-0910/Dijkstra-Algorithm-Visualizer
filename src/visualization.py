import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, ax, highlight_path=None, total_distance=None, new_edge=None, pos=None):
    G = nx.Graph()
    for node in graph.get_nodes():
        G.add_node(node)
    for edge in graph.get_edges():
        G.add_edge(edge[0], edge[1], weight=edge[2])

    if pos is None:
        pos = nx.spring_layout(G)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray')

    # Draw nodes
    node_colors = ['#FFA07A' if node == highlight_path[0] else '#98FB98' if node == highlight_path[-1] 
                   else '#87CEFA' for node in G.nodes()] if highlight_path else ['#87CEFA'] * len(G.nodes())
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=700)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)

    # Highlight the path
    if highlight_path:
        path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, ax=ax)

    # Highlight new edge
    if new_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[new_edge], edge_color='g', width=2, ax=ax)

    if total_distance is not None:
        ax.text(0.05, 0.95, f"Total Distance: {total_distance:.2f}", transform=ax.transAxes, 
                fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

    ax.axis('off')

    return ax