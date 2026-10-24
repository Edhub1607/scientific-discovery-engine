from scipy import stats


def run_intervention(scm, node, observational, n_samples=200, value=3.0):
    """Force `node` to `value`; return the set of other nodes that clearly moved."""
    x = scm.sample(n_samples, intervene={node: value})
    moved = set()
    for j in range(scm.n):
        if j == node:
            continue
        p = stats.ttest_ind(x[:, j], observational[:, j], equal_var=False).pvalue
        if p < 0.001:
            moved.add(j)
    return moved


def use_result(node, moved, directed, undirected):
    """Orient any unresolved link that touches the intervened node."""
    for (a, b) in list(undirected):
        if node == a:
            directed.add((a, b) if b in moved else (b, a))
            undirected.remove((a, b))
        elif node == b:
            directed.add((b, a) if a in moved else (a, b))
            undirected.remove((a, b))