import numpy as np
import networkx as nx
from sde.simulator import LinearSCM


def test_graph_is_dag():
    scm = LinearSCM(6, seed=1)
    g = nx.from_numpy_array(scm.true_adjacency(), create_using=nx.DiGraph)
    assert nx.is_directed_acyclic_graph(g)


def test_intervention_fixes_value():
    scm = LinearSCM(5, seed=2)
    x = scm.sample(100, intervene={2: 3.0})
    assert np.allclose(x[:, 2], 3.0)