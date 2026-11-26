import json
import random
import unittest
from genesis import Self, World

class GenesisTests(unittest.TestCase):
    def test_learning_and_continuity(self):
        agent = Self()
        identity = agent.state["identity"]
        for substrate in ("A", "B"):
            world = World(substrate, seed=42)
            rng = random.Random(42)
            for _ in range(1000):
                agent.step(world, rng)
            agent = Self(json.loads(json.dumps(agent.state)))
            self.assertEqual(agent.state["identity"], identity)
        self.assertEqual(agent.state["cycle"], 2000)
        self.assertEqual(len(agent.state["history"]), 2000)
        for substrate, preferred in (("A", 0), ("B", 1)):
            beliefs = agent.state["beliefs"][substrate]
            means = [a/(a+b) for a,b in beliefs]
            self.assertGreater(means[preferred], means[1-preferred])
        self.assertTrue(agent.state["history"][1000]["substrate_changed"])

if __name__ == "__main__":
    unittest.main()
