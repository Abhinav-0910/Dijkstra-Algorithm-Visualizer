import streamlit as st
import matplotlib.pyplot as plt
import time
import networkx as nx
import random
from graph import Graph
from dijkstra import dijkstra
from visualization import draw_graph
from matplotlib.animation import FuncAnimation

# Helper function to reconstruct path
def reconstruct_path(previous_nodes, start, end):
    path = []
    current = end
    while current != start:
        if current is None:
            return None
        path.append(current)
        current = previous_nodes[current]
    path.append(start)
    return path[::-1]

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = Graph()
    st.session_state.fixed_layout = {}
    st.session_state.show_graph = False

st.set_page_config(layout="wide")

st.title("Dijkstra's Algorithm Visualizer")

# Create two columns for layout
left_column, right_column = st.columns([2, 3])

with left_column:
    # Input section
    input_section = st.container()
    with input_section:
        st.header("Add Edge")
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            node1 = st.text_input("Node 1")
        with col2:
            node2 = st.text_input("Node 2")
        with col3:
            weight = st.number_input("Weight", min_value=0.0, step=0.1)
        if st.button("Add Edge"):
            if node1 and node2 and weight is not None:
                st.session_state.graph.add_edge(node1, node2, weight)
                st.success(f"Edge added: {node1} - {node2} (weight: {weight})")
                st.session_state.new_edge = (node1, node2)
                st.session_state.show_graph = True
                
                # Update fixed layout if new nodes are added
                for node in [node1, node2]:
                    if node not in st.session_state.fixed_layout:
                        # Find a position not too close to existing nodes
                        while True:
                            new_pos = (random.uniform(0, 1), random.uniform(0, 1))
                            if all(((new_pos[0]-pos[0])**2 + (new_pos[1]-pos[1])**2)**0.5 > 0.2 
                                   for pos in st.session_state.fixed_layout.values()):
                                st.session_state.fixed_layout[node] = new_pos
                                break
            else:
                st.error("Please enter both nodes and weight.")

        st.header("Run Dijkstra's Algorithm")
        col1, col2 = st.columns([1,1])
        with col1:
            start_node = st.text_input("Start Node")
        with col2:
            end_node = st.text_input("End Node")
        if st.button("Find Shortest Path"):
            if start_node and end_node:
                if start_node in st.session_state.graph.get_nodes() and end_node in st.session_state.graph.get_nodes():
                    distances, previous_nodes = dijkstra(st.session_state.graph, start_node)
                    path = reconstruct_path(previous_nodes, start_node, end_node)
                    if path:
                        st.success(f"Shortest path: {' -> '.join(path)}")
                        st.success(f"Total distance: {distances[end_node]}")
                        st.session_state.shortest_path = path
                        st.session_state.total_distance = distances[end_node]
                    else:
                        st.info(f"No path found between {start_node} and {end_node}")
                        st.session_state.shortest_path = None
                        st.session_state.total_distance = None
                else:
                    st.error("Start or end node not in graph.")
            else:
                st.error("Please enter both start and end nodes.")

with right_column:
    # Graph section
    graph_section = st.container()
    with graph_section:
        if st.session_state.show_graph:
            st.header("Graph Visualization")
            graph_placeholder = st.empty()

            def update_graph(highlight_path=None, new_edge=None, total_distance=None):
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.set_facecolor('#2F3E46')  # Dark background color
                fig.patch.set_facecolor('#2F3E46')  # Dark background color for the entire figure
                draw_graph(st.session_state.graph, ax, highlight_path=highlight_path, total_distance=total_distance, new_edge=new_edge, pos=st.session_state.fixed_layout)
                graph_placeholder.pyplot(fig)
                plt.close(fig)

            # Initial graph update
            update_graph()

            # Animate new edge if added
            if 'new_edge' in st.session_state:
                new_edge = st.session_state.new_edge
                # Highlight the nodes first
                update_graph(highlight_path=[new_edge[0], new_edge[1]])
                time.sleep(0.5)
                # Then show the new edge
                update_graph(new_edge=new_edge)
                time.sleep(1)  # Increased delay for better visibility
                del st.session_state.new_edge
                update_graph()  # Redraw the graph without highlighting

            # Animate shortest path if found
            if 'shortest_path' in st.session_state:
                path = st.session_state.shortest_path
                total_distance = st.session_state.total_distance
                if path:
                    for i in range(1, len(path)):
                        update_graph(highlight_path=path[:i+1], total_distance=total_distance)
                        time.sleep(0.5)  # Add a small delay for animation effect
                del st.session_state.shortest_path
                del st.session_state.total_distance

# Add a button to reset the graph to the dummy graph
if st.button("Dummy Graph"):
    st.session_state.graph = Graph()
    st.session_state.graph.add_edge('A', 'B', 4)
    st.session_state.graph.add_edge('A', 'C', 2)
    st.session_state.graph.add_edge('B', 'D', 3)
    st.session_state.graph.add_edge('C', 'D', 1)
    st.session_state.graph.add_edge('C', 'E', 5)
    st.session_state.graph.add_edge('D', 'E', 2)
    st.session_state.graph.add_edge('D', 'F', 6)  # New edge
    st.session_state.graph.add_edge('E', 'G', 4)  # New edge
    st.session_state.graph.add_edge('F', 'G', 3)  # New edge
    st.session_state.show_graph = True
    st.session_state.show_graph = True
    
    # Recreate the fixed layout
    G = nx.Graph()
    for node in st.session_state.graph.get_nodes():
        G.add_node(node)
    for edge in st.session_state.graph.get_edges():
        G.add_edge(edge[0], edge[1])
    st.session_state.fixed_layout = nx.spring_layout(G, k=0.5, iterations=50)
    
    st.rerun() 
    
# ... existing code ...

# Add a horizontal line before the new section
st.markdown("<hr style='margin-top: 30px; margin-bottom: 30px;'>", unsafe_allow_html=True)

# New section for real-life applications
st.header("Real-Life Applications of Dijkstra's Algorithm")

# Custom CSS for card-like appearance with hover effect and smooth edges
st.markdown("""
<style>
.card {
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    width: 100%;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    border: 1px solid #e0e0e0;
    background-color: transparent;
    height: 450px; /* Set a fixed height for all cards */
    display: flex;
    flex-direction: column;
}
.card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    transform: translateY(-5px);
}
.card-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}
.card-image {
    width: 100%;
    height: 200px; /* Set a fixed height for all images */
    object-fit: cover; /* Ensure the image covers the area without distortion */
    border-radius: 10px;
    margin-bottom: 15px;
}
.read-more {
    display: inline-block;
    margin-top: auto; /* Push the "Read More" link to the bottom */
    color: #4CAF50;
    text-decoration: none;
    font-weight: bold;
}
.read-more:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Create three columns for the cards
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown("""
        <div class="card">
            <p class="card-title">GPS Navigation</p>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4JRFOAyFcthM3cO8lEIv1ntqZ6bRMwxCEEA&s" class="card-image" alt="GPS icon">
            <p>Dijkstra's algorithm is used in GPS systems to find the shortest route between two locations, considering factors like distance, traffic, and road conditions.</p>
            <a href="https://en.wikipedia.org/wiki/GPS_navigation_device" target="_blank" class="read-more">Read More</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown("""
        <div class="card">
            <p class="card-title">Network Routing</p>
            <img src="data:image/jpeg;base64,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" class="card-image" alt="Network icon">
            <p>In computer networks, Dijkstra's algorithm helps in finding the most efficient path for data packets to travel from one node to another, minimizing delay and maximizing bandwidth.</p>
            <a href="https://en.wikipedia.org/wiki/Routing" target="_blank" class="read-more">Read More</a>
        </div>
        """, unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown("""
        <div class="card">
            <p class="card-title">Social Networks</p>
            <img src="data:image/png;base64,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" class="card-image" alt="Social network icon">
            <p>Dijkstra's algorithm can be used to find the shortest connection between two people in a social network, helping to analyze relationships and recommend connections.</p>
            <a href="https://en.wikipedia.org/wiki/Social_network_analysis" target="_blank" class="read-more">Read More</a>
        </div>
        """, unsafe_allow_html=True)

# Additional applications
st.write("Other applications include:")
st.write("- Robotics: Path planning for autonomous robots")
st.write("- Telecommunications: Optimal routing in telephone networks")
st.write("- Biology: Modeling the spread of diseases in populations")
st.write("- Urban Planning: Designing efficient public transportation routes")