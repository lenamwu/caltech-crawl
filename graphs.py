import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

with open('crawled_data.json', 'r') as file:
    links_data = json.load(file)

G = nx.DiGraph()
for source, targets in links_data.items():
    for target in targets:
        G.add_edge(source, target)

G_undirected = G.to_undirected()

def generate_histograms(G):
    out_degrees = [G.out_degree(n) for n in G.nodes()]
    in_degrees = [G.in_degree(n) for n in G.nodes()]

    plt.figure()
    plt.hist(out_degrees, bins=range(1, max(out_degrees)+1), log=True, edgecolor='black')
    plt.title('Histogram of Outgoing Hyperlinks')
    plt.xlabel('Number of Outgoing Hyperlinks')
    plt.ylabel('Frequency')
    plt.savefig('outgoing_hyperlinks_histogram.png')
    plt.close()

    plt.figure()
    plt.hist(in_degrees, bins=range(1, max(in_degrees)+1), log=True, edgecolor='black')
    plt.title('Histogram of Incoming Hyperlinks')
    plt.xlabel('Number of Incoming Hyperlinks')
    plt.ylabel('Frequency')
    plt.savefig('incoming_hyperlinks_histogram.png')
    plt.close()

generate_histograms(G)

def generate_ccdf(data, title, xlabel, ylabel, filename):
    sorted_data = np.sort(data)
    ccdf = 1. - np.arange(len(sorted_data)) / float(len(sorted_data))

    plt.figure()
    plt.loglog(sorted_data, ccdf, marker='o', linestyle='none')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)
    plt.close()

out_degrees = [G.out_degree(n) for n in G.nodes()]
in_degrees = [G.in_degree(n) for n in G.nodes()]
generate_ccdf(out_degrees, "CCDF of Outgoing Links", "Out-degree", "CCDF", "ccdf_outgoing_links.png")
generate_ccdf(in_degrees, "CCDF of Incoming Links", "In-degree", "CCDF", "ccdf_incoming_links.png")

def calculate_network_statistics(G):
    avg_clustering = nx.average_clustering(G_undirected)
    overall_clustering = nx.transitivity(G_undirected)
    largest_cc = max(nx.connected_components(G_undirected), key=len)
    G_largest_cc = G_undirected.subgraph(largest_cc)
    avg_diameter = nx.average_shortest_path_length(G_largest_cc)
    max_diameter = nx.diameter(G_largest_cc)
    
    print(f"Average Clustering Coefficient: {avg_clustering}")
    print(f"Overall Clustering Coefficient: {overall_clustering}")
    print(f"Average Diameter of the Largest Component: {avg_diameter}")
    print(f"Maximal Diameter of the Largest Component: {max_diameter}")

calculate_network_statistics(G)
