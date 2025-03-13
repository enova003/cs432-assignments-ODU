import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

def girvan_newman_step(graph):
    betweenness = nx.edge_betweenness_centrality(graph)
    max_betweenness = -1
    edge_to_remove = None
    
    for edge, betweenness_value in betweenness.items():
        if betweenness_value > max_betweenness:
            max_betweenness = betweenness_value
            edge_to_remove = edge
    
    G_new = graph.copy()
    G_new.remove_edge(*edge_to_remove)
    
    return edge_to_remove, G_new, max_betweenness

def visualize_graph(graph, iteration=None, removed_edge=None, betweenness=None):
    faction_colors = []
    for node in graph.nodes:
        if graph.nodes[node]['club'] == 'Mr. Hi':
            faction_colors.append('black') 
        else:
            faction_colors.append('green')  # John A
    
    global pos
    if 'pos' not in globals():
        pos = nx.spring_layout(graph, seed=42)
    
    plt.figure(figsize=(10, 8))
    
    nx.draw(graph, pos=pos, node_color=faction_colors, with_labels=True, font_color="white", node_size=500, width=1.5)
    
    if iteration is not None and removed_edge is not None and betweenness is not None:
        plt.title(f"Iteration {iteration}: Removed edge {removed_edge} (Betweenness: {betweenness:.4f})")
    else:
        plt.title("Karate Club Graph (John A & Mr. Hi)")

    if iteration is not None:
        plt.savefig(f"iteration_{iteration}.png")
    else:
        plt.savefig("original_graph.png")
    
    plt.show()

def count_components(graph):
    return nx.number_connected_components(graph)

def main():
    G = nx.karate_club_graph()
    visualize_graph(G)
 
    iteration = 1
    current_graph = G.copy()
    num_components = count_components(current_graph)
    
    while num_components < 2:
        print(f"Iteration {iteration}")
        edge_removed, current_graph, betweenness = girvan_newman_step(current_graph)
        visualize_graph(current_graph, iteration, edge_removed, betweenness)
        
        num_components = count_components(current_graph)
        print(f"Number of components: {num_components}")
        print(f"Removed edge: {edge_removed} with betweenness: {betweenness:.4f}")
        
        iteration += 1
    
    print(f"\nThe graph was split after {iteration-1} iterations.")
    
    components = list(nx.connected_components(current_graph))
    
    mr_hi_faction = set()
    john_a_faction = set()
    
    for node in G.nodes():
        if G.nodes[node]['club'] == 'Mr. Hi':
            mr_hi_faction.add(node)
        else:
            john_a_faction.add(node)
    
    if len(components) == 2:
        comp1, comp2 = components
        
        match1 = len(comp1.intersection(mr_hi_faction)) + len(comp2.intersection(john_a_faction))
        match2 = len(comp1.intersection(john_a_faction)) + len(comp2.intersection(mr_hi_faction))
        
        total_nodes = len(G.nodes())
        accuracy = max(match1, match2) / total_nodes
        
        print(f"Accuracy of the split compared to actual factions: {accuracy:.2%}")

if __name__ == "__main__":
    main()