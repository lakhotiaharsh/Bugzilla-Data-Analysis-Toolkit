import networkx as nx
import statistics
import csv
from pathlib import Path

def compute_metrics(pajek_file, community=None):
    """
    Compute global graph metrics from a Pajek .net file.
    """
    # Load graph
    G = nx.read_pajek(pajek_file)
    G = nx.Graph(G)  # convert to undirected if not already
    
    n = len(G.nodes())
    m = len(G.edges())
    
    # ---------------------------
    # Centrality measures
    # ---------------------------
    degree_dict = dict(G.degree())
    if n > 2:
        max_degree = max(degree_dict.values())
        degree_centralization = sum(max_degree - d for d in degree_dict.values()) / ((n - 1) * (n - 2))
    else:
        degree_centralization = 0

    betweenness = nx.betweenness_centrality(G, normalized=True)
    if n > 2:
        max_betweenness = max(betweenness.values())
        betweenness_centralization = sum(max_betweenness - b for b in betweenness.values()) / ((n - 1)*(n - 2)/2)
    else:
        betweenness_centralization = 0

    closeness = nx.closeness_centrality(G)
    if n > 2:
        max_closeness = max(closeness.values())
        closeness_centralization = sum(max_closeness - c for c in closeness.values()) / (n - 2)
    else:
        closeness_centralization = 0

    eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
    if n > 2:
        max_eigenvector = max(eigenvector.values())
        eigenvector_centralization = sum(max_eigenvector - e for e in eigenvector.values()) / (n - 2)
    else:
        eigenvector_centralization = 0
    
    # ---------------------------
    # Global metrics
    # ---------------------------
    global_clustcoeff = nx.transitivity(G)
    assortativity = nx.degree_assortativity_coefficient(G)
    diameter = nx.diameter(G) if nx.is_connected(G) else float("inf")
    avg_degree = statistics.mean(dict(G.degree()).values()) if n > 0 else 0
    density = nx.density(G)
    avg_path_length = nx.average_shortest_path_length(G) if nx.is_connected(G) else float("inf")
    
    # Modularity
    if community is None:
        from networkx.algorithms.community import greedy_modularity_communities
        community = list(greedy_modularity_communities(G)) if n > 0 else []
    modularity = nx.algorithms.community.quality.modularity(G, community) if len(community) > 0 else 0
    
    return {
        "vertices": n,
        "edges": m,
        "degree_centralization": degree_centralization,
        "betweenness_centralization": betweenness_centralization,
        "closeness_centralization": closeness_centralization,
        "eigenvector_centralization": eigenvector_centralization,
        "global_clustcoeff": global_clustcoeff,
        "assortativity": assortativity,
        "diameter": diameter,
        "avg_degree": avg_degree,
        "modularity": modularity,
        "density": density,
        "avg_path_length": avg_path_length
    }

if __name__ == "__main__":
    results = []
    base_path = Path("E:/fyp")
    
    for period in range(1, 6):  # periods 1 to 5
        file_path = base_path / f"graph202{period}.net"
        metrics = compute_metrics(file_path)
        metrics["period"] = period
        results.append(metrics)
    
    # Write to CSV
    output_csv = "allmetrics.csv"
    with open(output_csv, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["period"] + list(results[0].keys() - {"period"}))
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Metrics saved to {output_csv}")
    #print(compute_metrics(base_path))
