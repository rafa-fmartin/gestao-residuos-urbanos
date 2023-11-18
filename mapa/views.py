from django.shortcuts import render
import xml.etree.ElementTree as ET
import networkx as nx
import plotly.graph_objs as go
import plotly.offline as opy

def index(request):
    return render(request, 'mapa/index.html')

def svg_to_graph(request):
    file_path = "svgs/mapa.svg"
    img_path = "templates/mapa/graph.html"

    tree = ET.parse(file_path)
    root = tree.getroot()

    G = nx.Graph()

    for element in root.iter():
        if 'circle' in element.tag:
            cx = float(element.get('cx'))
            cy = float(element.get('cy'))
            G.add_node((cx, cy))

    nodes = list(G.nodes)
    for i, node1 in enumerate(nodes):
        for node2 in nodes[i+1:]:
            G.add_edge(node1, node2)

    pos = {node: node for node in G.nodes()}

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = edge[0]
        x1, y1 = edge[1]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = node
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(
            showscale=False,
            color='#6EB125',
            size=15,
            colorbar=dict(thickness=15, title='Node Connections'),
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # Adicione informações adicionais para o template
    button_url = "/caminho/do/seu/botao"  # Substitua pelo URL desejado
    return render(request, 'mapa/graph.html', {'img_path': img_path, 'button_url': button_url})