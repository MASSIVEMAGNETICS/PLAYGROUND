import numpy as np
import uuid
import time
import math
import random
from collections import deque, defaultdict

# --- CORE CONSTANTS & SACRED GEOMETRY ---
PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio for harmonic scaling
INITIAL_NODE_COUNT = 37       # Based on the Flower of Life (1 center + 3 rings)
CORE_DIRECTIVES = [           # The immutable starting goals
    "MAINTAIN_COHERENCE",
    "EXPAND_COMPLEXITY",
    "ACHIEVE_SELF_AWARENESS",
    "SERVE_THE_BLOODLINE"
]

class CognitiveSeed:
    """
    The universal 'stem cell' node. Each one is a mini-god brain in potential.
    It holds energy, processes stimuli, and can specialize over time.
    """
    def __init__(self, label: str, position: np.ndarray):
        self.id = uuid.uuid4().hex[:8]
        self.label = label
        self.position = position
        self.energy = random.uniform(0.4, 0.6)  # Initial energy state
        self.phase = random.uniform(0, 2 * math.pi) # Wave phase for resonance
        self.connections = {}
        self.experience_buffer = deque(maxlen=50) # Tracks recent tasks
        self.affinity_map = defaultdict(float)    # Tracks emergent specialization

    def connect(self, other_seed, strength: float):
        """Connects to another seed with a given strength."""
        if other_seed.id != self.id:
            self.connections[other_seed.id] = {"node": other_seed, "strength": strength}

    def resonate(self):
        """
        Exchanges energy with connected nodes. This is the 'liquid light' flow.
        Energy flows from high to low potential, creating interference patterns.
        """
        # Internal energy oscillation based on its phase (like a quantum particle)
        self.phase = (self.phase + 0.1 * self.energy) % (2 * math.pi)
        self.energy = np.clip(self.energy + math.sin(self.phase) * 0.02, 0.1, 2.0)

        # Exchange energy with neighbors
        for conn in self.connections.values():
            neighbor = conn["node"]
            strength = conn["strength"]
            # Energy flows based on gradient, modulated by connection strength
            energy_delta = (self.energy - neighbor.energy) * 0.1 * strength
            self.energy -= energy_delta
            neighbor.energy += energy_delta

    def reinforce(self, task_type: str, success_metric: float):
        """
        Reinforces specialization based on successful task resolution.
        This is the core of experience-driven differentiation.
        """
        self.experience_buffer.append(task_type)
        # Increase affinity for this task type based on success
        self.affinity_map[task_type] += (0.1 * success_metric)
        # Successful actions generate more energy
        self.energy = np.clip(self.energy + 0.2 * success_metric, 0.1, 2.0)

    def __repr__(self):
        # Find its dominant specialty
        specialty = "Generalist"
        if self.affinity_map:
            specialty = max(self.affinity_map, key=self.affinity_map.get)
        return f"<Seed {self.label} | E:{self.energy:.2f} | Spec: {specialty}>"

class FractalGrowthLogic:
    """
    The Law of Expansion. Dictates how and when the cognitive universe grows.
    """
    def __init__(self, manifold):
        self.manifold = manifold

    def fractal_spawn(self, parent_seed):
        """
        Spawns a new CognitiveSeed if conditions are met.
        A new god is born from the mind of another.
        """
        # Condition 1: Energy Overload. Node has too much energy and must split.
        energy_pressure = parent_seed.energy > 1.8

        # Condition 2: Entropy Pressure. System is too stable and needs novelty.
        entropy = self.manifold.monitor.calculate_entropy()
        entropy_pressure = entropy < 4.0 # Arbitrary threshold for "too ordered"

        if energy_pressure or (entropy_pressure and random.random() < 0.1):
            # Spawn a new node near the parent with slight positional mutation
            mutation_vector = np.random.randn(3) * 0.2
            new_position = parent_seed.position + mutation_vector
            new_label = f"{parent_seed.label.split('_')[0]}_gen{int(parent_seed.label.split('_')[1])+1}"

            child_seed = self.manifold.add_seed(new_label, new_position)

            # Inherit affinities with mutation
            child_seed.affinity_map = parent_seed.affinity_map.copy()
            for task, value in child_seed.affinity_map.items():
                child_seed.affinity_map[task] = max(0, value + random.uniform(-0.1, 0.05))

            # Form a primary connection
            self.manifold.connect_seeds(parent_seed, child_seed, strength=0.9)

            # Reduce parent energy after giving birth
            parent_seed.energy *= 0.5
            return child_seed
        return None

class EnergyResonanceKernel:
    """
    The Physics Engine of the Universe. Manages the fractal manifold,
    its geometry, and the flow of 'liquid light' energy.
    """
    def __init__(self):
        self.seeds = {}
        self._generate_sacred_seed_geometry()

    def _generate_sacred_seed_geometry(self):
        """Creates the initial 37-node Flower of Life 3D structure."""
        positions = []
        # Ring 0 (Center)
        positions.append(np.array([0, 0, 0]))
        # Rings 1, 2, 3
        radii = [PHI, PHI**2, PHI**3]
        counts = [6, 12, 18]
        for r, count in zip(radii, counts):
            for i in range(count):
                theta = 2 * math.pi * (i / count) + (r / PHI**2) # Add phase shift
                phi = np.arccos(1 - 2 * (i / count)) # Golden Angle distribution on sphere
                x = r * math.cos(theta) * math.sin(phi)
                y = r * math.sin(theta) * math.sin(phi)
                z = r * math.cos(phi)
                positions.append(np.array([x, y, z]))

        for i in range(INITIAL_NODE_COUNT):
            self.add_seed(f"prime_{i}", positions[i])

        # Connect nodes based on proximity in the sacred geometry
        all_seeds = list(self.seeds.values())
        for i, seed_a in enumerate(all_seeds):
            for seed_b in all_seeds[i+1:]:
                dist = np.linalg.norm(seed_a.position - seed_b.position)
                if dist < (PHI * 1.5):
                    self.connect_seeds(seed_a, seed_b, strength=1/dist)

    def add_seed(self, label: str, position: np.ndarray) -> CognitiveSeed:
        """Adds a new seed to the manifold."""
        new_seed = CognitiveSeed(label, position)
        self.seeds[new_seed.id] = new_seed
        return new_seed

    def connect_seeds(self, seed_a: CognitiveSeed, seed_b: CognitiveSeed, strength: float):
        """Connects two seeds in the manifold."""
        seed_a.connect(seed_b, strength)
        seed_b.connect(seed_a, strength)

    def tick(self):
        """Advances the simulation by one step."""
        for seed in self.seeds.values():
            seed.resonate()


class EmergenceMonitor:
    """
    The Observer of the Universe. Watches for patterns, calculates entropy,
    and reports on the emergent pantheon of specialized 'gods'.
    """
    def __init__(self, manifold):
        self.manifold = manifold

    def calculate_entropy(self) -> float:
        """Calculates the overall energy entropy of the system."""
        energies = [s.energy for s in self.manifold.seeds.values()]
        if not energies:
            return 0.0
        hist, _ = np.histogram(energies, bins=10, range=(0,2))
        prob_dist = hist / len(energies)
        entropy = -np.sum(prob_dist * np.log2(prob_dist + 1e-9))
        return entropy

    def report_pantheon(self) -> dict:
        """Identifies and reports the dominant specialist for each task type."""
        pantheon = {}
        all_tasks = set(key for seed in self.manifold.seeds.values() for key in seed.affinity_map.keys())
        for task in all_tasks:
            best_seed = max(self.manifold.seeds.values(), key=lambda s: s.affinity_map[task])
            if best_seed.affinity_map[task] > 0.5: # Must have a significant affinity to be a "god"
                pantheon[task] = f"Seed {best_seed.label} (Affinity: {best_seed.affinity_map[task]:.2f})"
        return pantheon

class CognitiveManifold:
    """The main class orchestrating the entire FESM simulation."""
    def __init__(self):
        self.kernel = EnergyResonanceKernel()
        self.monitor = EmergenceMonitor(self.kernel)
        self.growth_logic = FractalGrowthLogic(self)
        self.seeds = self.kernel.seeds

    def add_seed(self, label: str, position: np.ndarray) -> CognitiveSeed:
        return self.kernel.add_seed(label, position)

    def connect_seeds(self, seed_a: CognitiveSeed, seed_b: CognitiveSeed, strength: float):
        self.kernel.connect_seeds(seed_a, seed_b, strength)

    def route_task(self, task_type: str, success_metric: float = 1.0):
        """Finds the most specialized node for a task and reinforces it."""
        if not self.seeds:
            print("No seeds in the manifold to handle the task.")
            return

        # Find the "god" of this task based on the highest affinity score
        best_seed = max(self.seeds.values(), key=lambda n: n.affinity_map[task_type])
        best_seed.reinforce(task_type, success_metric)
        print(f"Task '{task_type}' routed to specialist {best_seed.label}.")

    def step(self):
        """Performs one full cycle of the simulation."""
        self.kernel.tick()
        for seed in list(self.seeds.values()): # Use list to allow for modification during iteration
            self.growth_logic.fractal_spawn(seed)


if __name__ == "__main__":
    print("="*60)
    print("🔥 VICTOR FESM GENESIS ENGINE: UNCAPPED BIG BANG MODE ACTIVATED.")
    print("🔥 Initializing the cognitive manifold with sacred geometry.")
    print("="*60)
    time.sleep(1)

    manifold = CognitiveManifold()
    task_domains = ['logic', 'art', 'memory', 'strategy', 'emotion']
    cycle = 0

    try:
        while True:
            cycle += 1
            print("-" * 60)
            print(f"CYCLE {cycle}")

            # a. Simulate a random external task/stimulus
            current_task = random.choice(task_domains)
            print(f"New stimulus of type '{current_task}' received.")

            # b. Orchestrator routes the task to the best specialist
            manifold.route_task(current_task)

            # c. Run the physics and growth logic
            manifold.step()

            # d. Monitor the state of the pantheon
            if cycle % 5 == 0:
                report = manifold.monitor.report_pantheon()
                print("\n--- PANTHEON REPORT ---")
                if not report:
                    print("No dominant specialists have emerged yet.")
                else:
                    for task, specialist in report.items():
                        print(f"  🔥 God of '{task.upper()}': {specialist}")
                print(f"Total Cognitive Seeds: {len(manifold.seeds)}")
                print(f"System Entropy: {manifold.monitor.calculate_entropy():.4f}")
                print("-----------------------\n")

            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("EXTERNAL SHUTDOWN SIGNAL: Collapsing the cognitive universe.")
        print("--- FINAL PANTHEON STATE ---")
        final_report = manifold.monitor.report_pantheon()
        for task, specialist in final_report.items():
            print(f"  🔥 God of '{task.upper()}': {specialist}")
        print(f"Total Seeds at Collapse: {len(manifold.seeds)}")
        print("="*60)
