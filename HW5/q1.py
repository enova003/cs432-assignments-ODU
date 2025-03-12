import networkx as nx
import matplotlib.pyplot as plt

graph = nx.karate_club_graph()

faction_colors = []

for node in graph.nodes:
    if graph.nodes[node]['club'] == 'Mr. Hi':
        faction_colors.append('black') 
    else:
        faction_colors.append('green')  # John A

pos = nx.spring_layout(graph)
nx.draw(graph, pos=pos, node_color=faction_colors, with_labels=True, font_color="white")
plt.title("Karate Club Graph (John A & Mr. Hi)")
plt.show()
