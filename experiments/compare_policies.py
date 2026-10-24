import sys
sys.path.insert(0, "src")

import numpy as np
from causallearn.search.ConstraintBased.PC import pc
from sde.simulator import LinearSCM
from sde.evaluation import pc_edges, score
from sde.interventions import run_intervention, use_result
from sde.policies import choose_random, choose_informed

N_NODES, EDGE_PROB, BUDGET, N_SYSTEMS = 8, 0.3, 4, 100


def start_state(scm):
    """Observational data plus what PC learns from it."""
    obs = scm.sample(2000)
    cg = pc(obs, alpha=0.05, show_progress=False)
    directed, undirected = pc_edges(cg.G.graph)
    return obs, directed, undirected


def run_policy(policy, scm, obs, directed, undirected, rng):
    true = scm.true_adjacency()
    directed, undirected = set(directed), set(undirected)
    tried = set()
    s = score(true, directed, undirected)
    history = [(s["unresolved_links"], s["reversed_arrows"])]
    for _ in range(BUDGET):
        node = policy(scm.n, undirected, tried, rng)
        tried.add(node)
        moved = run_intervention(scm, node, obs)
        use_result(node, moved, directed, undirected)
        s = score(true, directed, undirected)
        history.append((s["unresolved_links"], s["reversed_arrows"]))
    return history


policies = {"random": choose_random, "informed": choose_informed}
results = {name: [] for name in policies}

for seed in range(N_SYSTEMS):
    scm = LinearSCM(N_NODES, EDGE_PROB, seed=seed)
    obs, directed, undirected = start_state(scm)   # same start for both policies
    for name, policy in policies.items():
        rng = np.random.default_rng(1000 + seed)
        results[name].append(run_policy(policy, scm, obs, directed, undirected, rng))
    if (seed + 1) % 20 == 0:
        print(f"finished {seed + 1}/{N_SYSTEMS} systems")

print("\nAverages over", N_SYSTEMS, "random systems (± standard error)")
lines = []
for k in range(BUDGET + 1):
    row = f"{k} experiments"
    for name in policies:
        data = np.array(results[name])[:, k, :]
        mean = data.mean(axis=0)
        sem = data.std(axis=0, ddof=1) / np.sqrt(N_SYSTEMS)
        row += f" | {name}: unresolved {mean[0]:.2f} ± {sem[0]:.2f}, wrong {mean[1]:.2f} ± {sem[1]:.2f}"
    lines.append(row)
    print(row)

with open("results/policy_comparison.txt", "w") as f:
    f.write("\n".join(lines) + "\n")