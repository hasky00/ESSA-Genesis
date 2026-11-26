"""Genesis 002: hidden regime changes and prediction-error detection."""
import argparse
import json
import random
from pathlib import Path
from genesis import Self

class DynamicWorld:
    substrate = "C"
    def __init__(self, seed, phase_length):
        self.rng = random.Random(seed)
        self.phase_length = phase_length
        self.tick = 0
    def act(self, action):
        phase = min(self.tick // self.phase_length, 2)
        p = ((.9,.2),(.2,.9),(.7,.4))[phase][action]
        self.tick += 1
        return int(self.rng.random() < p)

def run(state, phase_length=1000, seed=42):
    agent = Self(state)
    s = agent.state
    world = DynamicWorld(seed, phase_length)
    policy = random.Random(seed + 1)
    # One-sided cumulative surprise detector, with a warm-up after reset.
    score = 0.0
    age = 0
    alarms = []
    s["beliefs"]["C"] = [[1,1],[1,1]]
    for tick in range(3 * phase_length):
        beliefs = s["beliefs"]["C"]
        p = [a/(a+b) for a,b in beliefs]
        action = policy.randrange(2) if policy.random() < .2 else max(range(2), key=lambda i:p[i])
        outcome = world.act(action)
        age += 1
        score = max(0., score + p[action] - outcome - .1) if age > 50 else 0.
        alarm = score >= 8
        if alarm:
            alarms.append(tick + 1)
            s["beliefs"]["C"] = [[1,1],[1,1]]
            score, age = 0., 0
        beliefs = s["beliefs"]["C"]
        beliefs[action][0 if outcome else 1] += 1
        s["cycle"] += 1
        s["substrate"] = "C"
        s["history"].append({"cycle":s["cycle"],"substrate":"C","action":action,
            "prediction":p[action],"outcome":outcome,"squared_error":(p[action]-outcome)**2,
            "alarm":alarm,"experiment":"002"})
    return s, {"seed":seed,"phase_length":phase_length,"alarms":alarms,
        "hidden_changes_after":[phase_length,2*phase_length],"final_beliefs":s["beliefs"]["C"]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memory",type=Path,default=Path("genesis-memory.json"))
    parser.add_argument("--output",type=Path,default=Path("genesis-002-memory.json"))
    parser.add_argument("--phase-length",type=int,default=1000)
    parser.add_argument("--seed",type=int,default=42)
    args = parser.parse_args()
    if args.phase_length < 100 or args.output.resolve() == args.memory.resolve() or args.output.exists():
        parser.error("phase length must be >=100; output must be a new file")
    state = json.loads(args.memory.read_text())
    state, result = run(state,args.phase_length,args.seed)
    args.output.write_text(json.dumps(state,indent=2))
    print(json.dumps({"identity":state["identity"],"total_cycles":state["cycle"],**result},indent=2))

if __name__ == "__main__":
    main()
