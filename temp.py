pip install networkx
import pandas as pd
import networkx as nx
df = pd.read_excel('your_excel_file.xlsx')  # Replace with your file path
graph = nx.Graph()
for index, row in df.iterrows():
    node_id = index  # Unique identifier for each tag
    graph.add_node(node_id, label=row['text'], x=[row['x1'], row['x2'], row['x3'], row['x4']],
                   y=[row['y1'], row['y2'], row['y3'], row['y4']])
def is_nearby(tag1, tag2):
    x1_min = min(tag1['x'])
    x1_max = max(tag1['x'])
    x2_min = min(tag2['x'])
    x2_max = max(tag2['x'])
    y1_min = min(tag1['y'])
    y1_max = max(tag1['y'])
    y2_min = min(tag2['y'])
    y2_max = max(tag2['y'])

    if x1_max < x2_min or x1_min > x2_max:
        return False  # Tags are not nearby in the x-axis
    if y1_max < y2_min or y1_min > y2_max:
        return False  # Tags are not nearby in the y-axis

    return True  # Tags are nearby in both x and y axes
for node_id1, tag1 in graph.nodes(data=True):
    for node_id2, tag2 in graph.nodes(data=True):
        if node_id1 != node_id2 and is_nearby(tag1, tag2):
            graph.add_edge(node_id1, node_id2)
grouped_tags = list(nx.connected_components(graph))
