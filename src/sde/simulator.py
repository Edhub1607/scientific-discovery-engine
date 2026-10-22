import numpy as np


class LinearSCM:
    """A hidden causal system: each variable is a weighted sum of its parents plus noise."""

    def __init__(self, n_nodes, edge_prob=0.3, seed=0):
        self.rng = np.random.default_rng(seed)
        self.n = n_nodes
        # weights[i, j] != 0 means an arrow i -> j
        edges = np.triu(self.rng.random((n_nodes, n_nodes)) < edge_prob, k=1)
        signs = self.rng.choice([-1, 1], size=(n_nodes, n_nodes))
        strengths = self.rng.uniform(0.5, 2.0, size=(n_nodes, n_nodes))
        self.weights = edges * signs * strengths

    def true_adjacency(self):
        return (self.weights != 0).astype(int)

    def sample(self, n_samples, intervene=None):
        """Generate data. intervene={node: value} forces that node to a fixed value."""
        x = np.zeros((n_samples, self.n))
        for j in range(self.n):
            if intervene and j in intervene:
                x[:, j] = intervene[j]
            else:
                noise = self.rng.normal(size=n_samples)
                x[:, j] = x[:, :j] @ self.weights[:j, j] + noise
        return x