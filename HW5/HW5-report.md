# HW5 - Graph Partitioning
### Ethan Novak
### CS 432, Spring 2025
### Sunday March 23, 2025 11:59pm

# Q1 Answer

I created a Python script that draws the Karate Club graph. The script loads the Karate Club graph directly from NetworkX. The script then checks if the nodes belong to John A's faction or Mr. Hi's faction. If the node belongs to Mr. Hi, the node is colored black, and if the node belongs to John A, the node is colored green. The graph is drawn with nx.draw(), and the graph is displayed with matplotlib. 

```
# This script can also be found at HW5/q1.py.

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

```

The graph that the script generates can be seen below:

![Q1 Graph](q1Graph.png)

Q: How many nodes eventually go with John and how many with Mr. Hi?

A: 17 nodes correspond with John A, and 17 nodes also correspond with Mr. Hi. 

# Q2 Answer

# Q3 Answer

# References

* Zachary's Karate Club, <https://en.wikipedia.org/wiki/Zachary%27s_karate_club>
