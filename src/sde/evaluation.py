def pc_edges(g):
    """Turn causal-learn's matrix into (directed arrows, undirected links)."""
    n = g.shape[0]
    directed, undirected = set(), set()
    for i in range(n):
        for j in range(i + 1, n):
            if g[i, j] == -1 and g[j, i] == 1:
                directed.add((i, j))
            elif g[i, j] == 1 and g[j, i] == -1:
                directed.add((j, i))
            elif g[i, j] == -1 and g[j, i] == -1:
                undirected.add((i, j))
    return directed, undirected


def score(true_adj, directed, undirected):
    """Compare a learned graph to the truth. Returns counts."""
    n = true_adj.shape[0]
    true_edges = {(i, j) for i in range(n) for j in range(n) if true_adj[i, j]}
    true_pairs = {frozenset(e) for e in true_edges}
    found_pairs = {frozenset(e) for e in directed} | {frozenset(e) for e in undirected}

    return {
        "correct_arrows": len(directed & true_edges),
        "reversed_arrows": len({(j, i) for i, j in directed} & true_edges),
        "unresolved_links": len(undirected),
        "missing_edges": len(true_pairs - found_pairs),
        "extra_edges": len(found_pairs - true_pairs),
    }