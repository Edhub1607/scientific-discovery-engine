def choose_random(n, undirected, tried, rng):
    """Pick any node we haven't tried yet."""
    options = [v for v in range(n) if v not in tried]
    return int(rng.choice(options))


def choose_informed(n, undirected, tried, rng):
    """Pick the untried node that touches the most unresolved links."""
    counts = {v: 0 for v in range(n) if v not in tried}
    for a, b in undirected:
        for v in (a, b):
            if v in counts:
                counts[v] += 1
    best = max(counts.values())
    return int(rng.choice([v for v, c in counts.items() if c == best]))