import sys
sys.path.insert(0, "src")

import numpy as np
from scipy import stats
from causallearn.search.ConstraintBased.PC import pc
from sde.simulator import LinearSCM
from sde.evaluation import pc_edges, score


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


# Same hidden system as before
scm = LinearSCM(6, edge_prob=0.4, seed=3)
observational = scm.sample(2000)
true = scm.true_adjacency()

# Start from what PC can learn without experiments
cg = pc(observational, alpha=0.05, show_progress=False)
directed, undirected = pc_edges(cg.G.graph)
print("Start (observation only):", score(true, directed, undirected))

# RANDOM policy: try the nodes in a random order, one experiment each
rng = np.random.default_rng(0)
for step, node in enumerate(rng.permutation(scm.n), start=1):
    node = int(node)
    moved = run_intervention(scm, node, observational)
    use_result(node, moved, directed, undirected)
    print(f"Experiment {step} (node {node}):", score(true, directed, undirected))