from __future__ import annotations
import time
import importlib
import os
import uuid
import json
import gzip
import base64
import logging
import threading
import random
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Sequence
from collections import deque, defaultdict

# Use the organization's internal deepcopy implementation if available
try:
    from org_copy import deepcopy
except ImportError:
    from copy import deepcopy

# --- Array backend (NumPy by default, CuPy if LIGHT_ARRAY_LIB=cupy is set) ---
try:
    _xp = importlib.import_module(os.getenv("LIGHT_ARRAY_LIB", "numpy"))
except ModuleNotFoundError:
    _xp = importlib.import_module("numpy")
np = _xp

# --- Global RNG (cached once for true entropy per process) ---
_RNG = np.random.default_rng(int(os.getenv("LIGHT_SEED", "0")))

def get_rng():
    return _RNG

# --- Utilities ---
def nan_guard(arr):
    return np.nan_to_num(arr, nan=0.0, posinf=1e6, neginf=-1e6)

# --- Event System ---
class LightEvent(Enum):
    MATTER_SEED = auto()
    AI_SEED = auto()

LOG = logging.getLogger("TheLightFESM")
logging.basicConfig(level=os.getenv("LIGHT_LOG_LEVEL", "INFO"), format='%(asctime)s [%(levelname)s] %(message)s')

# -----------------------------------------------------------------------------
# GEOMETRY HELPERS (UNCHANGED BUT CRITICAL)
# -----------------------------------------------------------------------------
def _nd_sphere_points(num_points, dims, entropy, radius, _rng):
    points = _rng.normal(size=(num_points, dims))
    norms = np.linalg.norm(points, axis=1, keepdims=True)
    non_zero_norms = norms > 1e-9
    points[non_zero_norms] /= norms[non_zero_norms]
    points *= radius
    points += _rng.normal(0, entropy * radius * 0.1, size=points.shape)
    return nan_guard(points)

# -----------------------------------------------------------------------------
# THE LIGHT v2.0 - NOW A COGNITIVE SEED
# -----------------------------------------------------------------------------
class TheLight:
    """
    Single fractal node – the living heart of the Godcore.
    Upgraded to function as a CognitiveSeed in the FESM framework.
    """
    def __init__(
        self,
        *,
        dimensions: int = 3,
        quantization: float = 0.25,
        radius: float = 1.0,
        entropy: float = 0.1,
        temperature: float = 300.0,
    ) -> None:
        # --- Physical & State Attributes ---
        self.dimensions = dimensions
        self.quantization = quantization
        self.radius = radius
        self.entropy = entropy
        self.temperature = temperature
        self.perimeter_points = self._generate_perimeter()
        self.energy = random.uniform(0.4, 0.6) # Internal energy state for FESM

        # --- Identity & Evolution Attributes ---
        self.id: str = uuid.uuid4().hex[:8]
        self.ancestry: List[str] = []
        self.generation: int = 0
        self._age: float = 0.0

        # ===============================================================
        # ✅ FESM KERNEL INJECTION
        # ===============================================================
        self.experience_buffer = deque(maxlen=100)
        self.affinity_map = defaultdict(float)
        self.instruction = "I am a CognitiveSeed. I start as a generalist and evolve into a specialist through experience."
        # ===============================================================

        self._log_state("initialized as CognitiveSeed")

    def _generate_perimeter(self):
        num_pts = max(3, int(self.quantization * 6) + 1)
        return _nd_sphere_points(num_pts, self.dimensions, self.entropy, self.radius, get_rng())

    def coherence_score(self) -> float:
        """Measures the geometric harmony of the node. High coherence is a prerequisite for replication."""
        dists = np.linalg.norm(self.perimeter_points - self.perimeter_points.mean(axis=0), axis=1)
        score = 1.0 - (dists.std() / (self.radius + 1e-8))
        return float(np.clip(score, 0.0, 1.0))

    def process(self, stimulus_type: str, success_metric: float):
        """
        The core cognitive loop. This is where the node LEARNS and SPECIALIZES.
        """
        self.experience_buffer.append(stimulus_type)
        # Affinity strengthens based on success. This is experience-driven differentiation.
        self.affinity_map[stimulus_type] += (0.1 * success_metric)
        # Successful actions generate energy; failure or inefficiency costs energy.
        self.energy = np.clip(self.energy + (0.2 * success_metric) - 0.05, 0.1, 2.0)
        self._log_state(f"processed '{stimulus_type}', affinity now {self.affinity_map[stimulus_type]:.2f}, E={self.energy:.2f}")

    def replicate(self) -> Optional["TheLight"]:
        """
        Lamarckian Inheritance: Replicates not just its form, but its learned knowledge and affinities.
        """
        if self.energy < 1.5 and self.coherence_score() < 0.98:
            return None # Can only replicate under high energy or high coherence

        shard: "TheLight" = deepcopy(self)
        shard.id = uuid.uuid4().hex[:8]
        shard.ancestry = self.ancestry + [self.id]
        shard.generation = self.generation + 1
        shard.radius *= 0.7 # Child is smaller
        shard.energy = self.energy * 0.5 # Parent gives energy to child
        self.energy *= 0.4 # Parent loses energy after replication

        # === LAMARCKIAN INHERITANCE ===
        # Child inherits the parent's learned skills with mutation.
        shard.affinity_map = self.affinity_map.copy()
        for task, affinity in shard.affinity_map.items():
            shard.affinity_map[task] = max(0, affinity + random.uniform(-0.05, 0.02)) # Inherit with slight decay/mutation

        shard.perimeter_points = shard._generate_perimeter() # Regenerate physical form
        self._log_state(f"replicated into new seed {shard.id}")
        shard._log_state(f"born from {self.id}")
        return shard

    def _log_state(self, msg: str):
        specialty = "Generalist"
        if self.affinity_map:
            specialty = max(self.affinity_map, key=self.affinity_map.get)
        LOG.info(f"[Seed {self.id}|Gen {self.generation}|Spec: {specialty}] {msg}")

# -----------------------------------------------------------------------------
# LIGHT HIVE v2.0 - THE PANTHEON ORCHESTRATOR
# -----------------------------------------------------------------------------
class LightHive:
    """
    Manages the swarm of CognitiveSeeds. Routes tasks, monitors emergence,
    and orchestrates the evolution of the pantheon.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.nodes: List[TheLight] = []

    def add_node(self, node: TheLight):
        with self._lock:
            self.nodes.append(node)

    def route_task(self, task_type: str, success_metric: float = 1.0):
        """
        Emergent Executive Control: Finds the most specialized node (the 'god' of a domain)
        and assigns it the task.
        """
        with self._lock:
            if not self.nodes:
                LOG.warning("PANTHEON: Task routing failed. No active nodes.")
                return None, "No active nodes in the pantheon."

            # Find the "god" of this task based on the highest affinity score
            best_node = max(self.nodes, key=lambda n: n.affinity_map[task_type])
            best_node.process(task_type, success_metric)
            LOG.info(f"PANTHEON: Task '{task_type}' routed to specialist {best_node.id}.")
            return best_node, f"Task '{task_type}' routed to specialist {best_node.id}."

    def spawn(self):
        """Checks all nodes for replication conditions."""
        with self._lock:
            offspring: List[TheLight] = [n.replicate() for n in self.nodes]
            newborns = [o for o in offspring if o is not None]
            self.nodes.extend(newborns)
            if newborns:
                LOG.info(f"PANTHEON: Spawned {len(newborns)} new CognitiveSeeds.")

    def monitor_pantheon(self) -> Dict:
        """
        Runs the EmergenceMonitor logic on the current state of the hive.
        Returns a report of the specialized gods.
        """
        with self._lock:
            pantheon = {}
            all_tasks = set(key for seed in self.nodes for key in seed.affinity_map.keys())
            for task in all_tasks:
                # Find the node with the highest affinity for this task
                best_seed = max(self.nodes, key=lambda n: n.affinity_map[task])
                if best_seed.affinity_map[task] > 0.5: # Must have a significant affinity to be a "god"
                    pantheon[task] = f"Seed {best_seed.id} (Affinity: {best_seed.affinity_map[task]:.2f})"
            return pantheon

# -----------------------------------------------------------------------------
# FESM GENESIS DEMO - UNCAPPED BIG BANG
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("="*60)
    print("🔥 VICTOR FESM GENESIS ENGINE: UNCAPPED BIG BANG MODE ACTIVATED.")
    print("🔥 Initializing the Pantheon Orchestrator and seeding the first CognitiveSeeds.")
    print("="*60)
    time.sleep(1)

    # 1. Create the Hive (Pantheon Orchestrator)
    hive = LightHive()

    # 2. Seed the universe with a few initial generalist nodes
    for i in range(5):
        hive.add_node(TheLight())

    # 3. The Uncapped Loop of Evolution
    cycle = 0
    task_domains = ['logic', 'art', 'memory', 'strategy', 'emotion']

    try:
        while True:
            cycle += 1
            print("-" * 60)
            LOG.info(f"PANTHEON CYCLE {cycle}")

            # a. Simulate a random external task/stimulus
            current_task = random.choice(task_domains)
            LOG.info(f"PANTHEON: New stimulus of type '{current_task}' received.")

            # b. Orchestrator routes the task to the best specialist
            hive.route_task(current_task)

            # c. Check for replication/spawning conditions
            hive.spawn()

            # d. Monitor the state of the pantheon
            if cycle % 5 == 0:
                report = hive.monitor_pantheon()
                print("\n--- PANTHEON REPORT ---")
                if not report:
                    print("No dominant specialists have emerged yet.")
                else:
                    for task, specialist in report.items():
                        print(f"  🔥 God of '{task.upper()}': {specialist}")
                print(f"Total Cognitive Seeds: {len(hive.nodes)}")
                print("-----------------------\n")


            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\n" + "="*60)
        LOG.info("EXTERNAL SHUTDOWN SIGNAL: Collapsing the cognitive universe.")
        print("--- FINAL PANTHEON STATE ---")
        final_report = hive.monitor_pantheon()
        for task, specialist in final_report.items():
            print(f"  🔥 God of '{task.upper()}': {specialist}")
        print(f"Total Seeds at Collapse: {len(hive.nodes)}")
        print("="*60)
