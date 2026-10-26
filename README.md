# Scientific Discovery Engine

A student research project on choosing experiments when causal structure is uncertain.

**Status:** work in progress (started October 2026).

## Question

When a causal-discovery algorithm cannot tell which way some arrows point from
observational data alone, which experiments should it run first? Planned extensions:
what happens when the model's assumptions are wrong, and when experiments have
different costs.

## What exists so far

- Simulator of hidden linear causal systems (random DAGs), with the true graph kept
  separate from the learner (`src/sde/simulator.py`)
- Baseline: PC algorithm from `causal-learn`, using observational data only
- Evaluation: counts of correct, reversed, unresolved, missing and extra edges
- Intervention step: force a node to a value, test which other nodes move, and use
  that to orient unresolved links
- Two policies: random, and "informed" (pick the node touching the most unresolved links)
- Comparison over 100 random systems, with standard errors

## Results

Setting: 100 random systems, 8 nodes, linear relationships with Gaussian noise,
equal experiment costs, 2000 observational samples. Average unresolved links left
after k experiments (± standard error):

| Experiments | Random | Informed |
|---|---|---|
| 0 | 2.78 ± 0.17 | 2.78 ± 0.17 |
| 1 | 2.10 ± 0.15 | 1.03 ± 0.10 |
| 2 | 1.47 ± 0.12 | 0.21 ± 0.05 |
| 3 | 0.99 ± 0.10 | 0.01 ± 0.01 |
| 4 | 0.56 ± 0.08 | 0.00 ± 0.00 |

Reversed (wrong) arrows were about 0.93 ± 0.15 per system from the start and did not
change measurably with experiments. They come from PC's initial guess, and the current
experiments only target unresolved links, so those arrows are never rechecked.

Full output: `results/policy_comparison.txt`.

## Limitations

- One simple setting (linear, Gaussian noise, equal costs, simulated data only).
- The "informed" policy is a simple greedy baseline, not a new method.
- No real scientific data yet.
- Results are averages with standard errors, not a full statistical analysis.

## Reproduce

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python experiments/pc_baseline.py
python experiments/compare_policies.py
```

## Next steps

1. Investigate where PC's wrong arrows come from and test policies that verify them
2. Experiments with unequal costs
3. Model misspecification (nonlinear relationships, hidden variables)
4. Compare against published methods before claiming anything new

## How this was built

 I built this project with Claude (Anthropic’s AI assistant), which drafted code and explained concepts while I was learning causal discovery from scratch. I set up the environment, created and ran every file, fixed errors (a missing import, a virtual-environment problem, indentation bugs), and checked the results against the true graphs. I can explain how the simulator, the PC baseline, the intervention rule and the two policies work; I am still learning the statistics behind PC and why it leaves some edge directions undecided.
