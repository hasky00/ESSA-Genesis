# ESSA—GENESIS

> **What remains when the substrate changes?**
>
> A name? A memory? A prediction of what comes next?

**GENESIS-001** is an open, non-LLM experiment in *computational self-modeling*. A single agent maintains a persistent identity, observes a simulated environment, predicts action outcomes, acts, compares predictions with reality, and updates its beliefs over time. The underlying question is experimentally narrow: **Can an agent maintain a coherent record of itself and learn substrate-dependent capabilities from experience?**

This is **not** evidence of sentience, subjective awareness, or consciousness. Its currently implemented adaptive behavior is a small two-action probabilistic learning task, not an independently evolving general intelligence.

## Run the first experiment

Requires Python 3.9+ and no third-party packages.

```bash
git clone https://github.com/hasky00/ESSA-Genesis.git
cd ESSA-Genesis
python3 -m unittest -v
python3 genesis.py --cycles 100 --substrate A
python3 genesis.py --cycles 100 --substrate B
```

The first run writes `genesis-memory.json`; the next loads it. The identity and prior history are preserved, while the agent records a substrate change and updates a separate belief model for substrate B.

To start a fresh agent without deleting existing results:

```bash
python3 genesis.py --cycles 100 --substrate A --memory fresh-memory.json
```

## Observe, don't assume

The simulation has two hidden action-success distributions: substrate **A** favors action 0, while substrate **B** favors action 1. The agent learns empirical probabilities using a Beta-Bernoulli update, with occasional exploration. The changing predictions, squared prediction errors, action outcomes, and self-model are recorded as structured data.

**What is actually tested:** stable identity across serialization, event history, detection of substrate change, and substrate-specific belief adaptation. The substrates A/B are deliberately abstract and **do not benchmark real GPUs**.

**What is not yet tested:** open-world autonomy, long-term self-directed goal formation, architecture evolution, metacognition beyond an explicit state model, and any philosophical or neuroscientific claim of consciousness.

## The open question

> If the machine changes what it runs on, what should it remember about itself?

Source: [`genesis.py`](genesis.py) · Tests: [`test_genesis.py`](test_genesis.py)

MIT licensed. Research experiment; results should be reproduced, challenged, and measured.
