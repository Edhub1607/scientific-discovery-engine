import sys
sys.path.insert(0, "src")

from causallearn.search.ConstraintBased.PC import pc
from sde.simulator import LinearSCM
from sde.evaluation import pc_edges, score

# 1. Build a hidden system and collect OBSERVATIONAL data (no interventions)
scm = LinearSCM(6, edge_prob=0.4, seed=3)
data = scm.sample(2000)

# 2. Ask the PC algorithm to guess the graph from that data alone
cg = pc(data, alpha=0.05, show_progress=False)
g = cg.G.graph

# 3. Print the truth, then PC's answer
true = scm.true_adjacency()
n = scm.n

print("TRUE arrows:")
for i in range(n):
    for j in range(n):
        if true[i, j]:
            print(f"  {i} -> {j}")

print("\nPC found:")
for i in range(n):
    for j in range(i + 1, n):
        if g[i, j] == -1 and g[j, i] == 1:
            print(f"  {i} -> {j}")
        elif g[i, j] == 1 and g[j, i] == -1:
            print(f"  {j} -> {i}")
        elif g[i, j] == -1 and g[j, i] == -1:
            print(f"  {i} -- {j}   (connected, direction UNKNOWN)")

# 4. Score PC against the truth
directed, undirected = pc_edges(g)
print("\nScore:", score(true, directed, undirected))