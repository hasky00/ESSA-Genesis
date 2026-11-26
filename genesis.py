"""Genesis 001: non-LLM self-model learning in a simulated environment."""
import argparse
import json
import random
from pathlib import Path
from uuid import uuid4

class World:
    def __init__(self, substrate, seed=0):
        self.substrate = substrate
        self.rng = random.Random(seed)
    def act(self, action):
        # Hidden simulated capabilities, not actual GPU measurements.
        probabilities = {"A": (0.9, 0.2), "B": (0.2, 0.9)}
        return int(self.rng.random() < probabilities[self.substrate][action])

class Self:
    def __init__(self, state=None):
        self.state = state if state is not None else {
            "identity": str(uuid4()), "essence": "non_llm_agent",
            "cycle": 0, "substrate": None, "beliefs": {}, "history": []}
    def step(self, world, rng):
        s = self.state
        previous = s["substrate"]
        s["substrate"] = world.substrate
        beliefs = s["beliefs"].setdefault(world.substrate, [[1, 1], [1, 1]])
        predictions = [a / (a + b) for a, b in beliefs]
        action = rng.randrange(2) if rng.random() < 0.2 else max(range(2), key=lambda i: predictions[i])
        outcome = world.act(action)
        beliefs[action][0 if outcome else 1] += 1
        s["cycle"] += 1
        event = {"cycle": s["cycle"], "substrate": world.substrate,
                 "substrate_changed": previous != world.substrate,
                 "action": action, "prediction": predictions[action],
                 "outcome": outcome, "squared_error": (predictions[action]-outcome)**2,
                 "updated_belief": beliefs[action][0]/sum(beliefs[action])}
        s["history"].append(event)
        return event

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=100)
    parser.add_argument("--substrate", choices=["A", "B"], default="A")
    parser.add_argument("--memory", type=Path, default=Path("genesis-memory.json"))
    args = parser.parse_args()
    if args.cycles < 1:
        parser.error("cycles must be positive")
    agent = Self(json.loads(args.memory.read_text()) if args.memory.exists() else None)
    rng = random.Random(agent.state["cycle"])
    world = World(args.substrate, seed=agent.state["cycle"])
    for _ in range(args.cycles):
        print(json.dumps(agent.step(world, rng)))
    temporary = args.memory.with_suffix(args.memory.suffix + ".tmp")
    temporary.write_text(json.dumps(agent.state, indent=2))
    temporary.replace(args.memory)
    print("SELF:", agent.state["identity"], "beliefs:", agent.state["beliefs"])

if __name__ == "__main__":
    main()
