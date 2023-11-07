from django.shortcuts import render
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt

def index(request):
    return render (request, 'mapa/index.html')

def svg_to_graph(request):
    file_path = "svgs/mapa.svg"
    img_path = "setup/static/assets/imagens/graph.png"
    tree = ET.parse(file_path)
    root = tree.getroot()

    G = nx.Graph()

    for element in root.iter():
        if 'circle' in element.tag:
            cx = float(element.get('cx'))
            cy = float(element.get('cy'))
            G.add_node((cx, cy))

    #for node in G.nodes:
    #    G.nodes[node]['color'] = "#6EB125"

    pos = {node: node for node in G.nodes()}
    nx.draw(G, pos, with_labels=False, node_size=50, node_color='#6EB125')
    plt.axis('equal')
    plt.savefig(img_path, format='png')
    plt.close()

    return render(request, 'mapa/graph.html', {'img_path': img_path})