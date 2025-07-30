import numpy as np
import random
import time

# ==============================================================================================
# SUBSTRATE IMPLEMENTATION (v2.0)
# ==============================================================================================
class TheLight:
    """
    A fully implemented simulation of a fractal energy substrate. It has properties
    like entropy, temperature, and energy, which influence its computational coherence.
    """
    def __init__(self, state='field', dimensions=4, radius=1.0, entropy=0.1, temperature=0.1, energy=1.0):
        self.state = state
        self.dimensions = dimensions
        self.radius = radius
        self.entropy = max(0, min(1, entropy))
        self.temperature = max(0, min(1, temperature))
        self.energy = max(0, min(1, energy)) # v2.0 Feature: Resource pool

    def coherence_score(self):
        """Coherence is high when entropy and temperature are low, but requires energy."""
        base_coherence = 1.0 - (self.entropy + self.temperature) / 2.0
        # Energy acts as a multiplier; low energy cripples coherence.
        return max(0, base_coherence * self.energy)

    def excite(self, temp_boost=0.0, entropy_boost=0.0):
        self.temperature = min(1, self.temperature + temp_boost)
        self.entropy = min(1, self.entropy + entropy_boost)
        print(f"   [Substrate Event: Excite -> Temp: {self.temperature:.2f}, Entropy: {self.entropy:.2f}]")

    def cool(self, temp_drop=0.0, entropy_drop=0.0):
        self.temperature = max(0, self.temperature - temp_drop)
        self.entropy = max(0, self.entropy - entropy_drop)
        print(f"   [Substrate Event: Cool -> Temp: {self.temperature:.2f}, Entropy: {self.entropy:.2f}]")

    def morph(self, new_state, scale):
        self.state = new_state
        self.radius *= scale
        print(f"   [Substrate Event: Morph -> State: {self.state}, Radius: {self.radius:.2f}]")

    def recharge(self, amount):
        self.energy = min(1.0, self.energy + amount)
        print(f"   [Substrate Event: Recharge -> Energy: {self.energy:.2f}]")

    def info(self):
        return {
            "state": self.state, "dims": self.dimensions, "radius": round(self.radius, 3),
            "entropy": round(self.entropy, 3), "temp": round(self.temperature, 3),
            "energy": round(self.energy, 3), "coherence": round(self.coherence_score(), 3)
        }

# ==============================================================================================
# QUANTUM FRACTAL PLUGIN LAYER (v2.0)
# ==============================================================================================
class QuantumFractalPluginLayer:
    """
    v2.0: Universal plug-in layer for quantum algorithms with orchestration and homeostasis.
    """
    def __init__(self, substrate, log_events=True):
        assert hasattr(substrate, "coherence_score") and hasattr(substrate, "energy"), "Substrate must be a compatible v2.0 class"
        self.substrate = substrate
        self.log_events = log_events
        self.plugins = {}
        self.history = []
        self._init_default_plugins()

    def add_plugin(self, name, func, default_cost=0.1):
        self.plugins[name] = {'func': func, 'cost': default_cost}
        self._log(f"Plugin added: {name} (Cost: {default_cost})")

    def run(self, name, **kwargs):
        if name not in self.plugins:
            raise ValueError(f"Quantum algorithm '{name}' not found.")

        plugin_info = self.plugins[name]
        cost = plugin_info['cost']

        # v2.0 Feature: Substrate Cost Check
        if self.substrate.energy < cost:
            self._log(f"ABORTED: Insufficient energy for '{name}'. Required: {cost:.2f}, Have: {self.substrate.energy:.2f}")
            self._trigger_events(name, {"status": "aborted_low_energy"})
            return None

        # Execute plugin and apply cost
        result = plugin_info['func'](self.substrate, **kwargs)
        self.substrate.energy -= cost
        self._log(f"'{name}' executed. Cost: {cost:.2f}. Energy left: {self.substrate.energy:.2f}")

        self.history.append({"algo": name, "result": result})
        self._trigger_events(name, result)
        return result

    # v2.0 Feature: Quantum Orchestrator
    def run_sequence(self, sequence):
        self._log("Orchestrator engaged: Running sequence.")
        results_cache = {}
        for i, step in enumerate(sequence):
            plugin_name = step['name']
            kwargs = step.get('params', {})

            # Pipe output from a previous step if requested
            if 'use_output_from' in kwargs:
                source_plugin, source_key = kwargs.pop('use_output_from')
                if source_plugin in results_cache and source_key in results_cache[source_plugin]:
                    kwargs[source_key] = results_cache[source_plugin][source_key]
                else:
                    self._log(f"Sequence break: cannot find key '{source_key}' from plugin '{source_plugin}'.")
                    return None

            result = self.run(plugin_name, **kwargs)
            if result is None:
                self._log(f"Sequence halted at step {i+1} due to execution failure.")
                return results_cache

            results_cache[plugin_name] = result
        self._log("Sequence complete.")
        return results_cache

    def _log(self, msg):
        if self.log_events:
            print(f"[QFPL] {msg}")

    # v2.0 Feature: Homeostasis Protocol
    def _trigger_events(self, name, result):
        coh = self.substrate.coherence_score()
        energy = self.substrate.energy
        if coh > 0.98:
            self._log(f"GENESIS EVENT: '{name}' reached hyper-symmetry ({coh:.3f}). Consider spawning new task.")
        elif coh < 0.4:
            self._log(f"HOMEOSTASIS: Phase collapse detected ({coh:.3f}). Triggering self-correction.")
            self.run("quantum_error_correction") # Corrective action has its own cost
        if energy < 0.2:
            self._log(f"HOMEOSTASIS: Low energy warning ({energy:.2f}). Triggering recharge cycle.")
            self.run("energy_absorption_protocol")

    def _init_default_plugins(self):
        self.add_plugin("quantum_factoring", self.quantum_factoring, default_cost=0.25)
        self.add_plugin("quantum_field_simulation", self.quantum_field_simulation, default_cost=0.2)
        self.add_plugin("quantum_error_correction", self.quantum_error_correction, default_cost=0.1)
        self.add_plugin("energy_absorption_protocol", self.energy_absorption_protocol, default_cost=-0.3) # Negative cost = energy gain

    # --- ALGORITHMS (Plugins) ---
    def quantum_factoring(self, substrate, N=177):
        self._log(f"Attempting to factor {N}...")
        substrate.excite(temp_boost=0.1, entropy_boost=0.1)
        # In a real scenario, this would be a quantum algorithm. Here, we simulate.
        factor = next((x for x in range(2, int(N**0.5) + 1) if N % x == 0), 'Prime')
        substrate.cool(temp_drop=0.1, entropy_drop=0.1)
        return {"N": N, "factor": factor}

    def quantum_field_simulation(self, substrate, steps=3):
        self._log(f"Simulating quantum field...")
        for _ in range(steps):
            substrate.morph('plasma', scale=1.05)
        return substrate.info()

    def quantum_error_correction(self, substrate, n_runs=3):
        self._log(f"Applying error correction...")
        for _ in range(n_runs):
            substrate.cool(temp_drop=0.05, entropy_drop=0.05)
        return substrate.info()

    def energy_absorption_protocol(self, substrate, source='ambient'):
        self._log(f"Absorbing energy from '{source}' source...")
        substrate.recharge(amount=0.3) # Cost is negative, so this adds net energy
        return substrate.info()

# ==============================================================================================
# SCRIPT EXECUTION
# ==============================================================================================
if __name__ == "__main__":
    # --- Initialization ---
    print("INITIALIZING GODCORE v2.0\n" + "="*40)
    the_light_substrate = TheLight(energy=0.8)
    qfpl_engine = QuantumFractalPluginLayer(the_light_substrate)
    print("\nCURRENT SUBSTRATE STATE:")
    print(qfpl_engine.substrate.info())
    print("="*40 + "\n")

    # --- DEMO 1: Quantum Orchestrator ---
    print("DEMO 1: Running an orchestrated sequence\n" + "-"*40)
    factoring_sequence = [
        {'name': 'quantum_factoring', 'params': {'N': 247}},
        {'name': 'quantum_field_simulation', 'params': {'steps': 2}}
    ]
    qfpl_engine.run_sequence(factoring_sequence)
    print("\nFINAL SUBSTRATE STATE AFTER DEMO 1:")
    print(qfpl_engine.substrate.info())
    print("="*40 + "\n")

    # --- DEMO 2: Homeostasis Protocol (Low Energy) ---
    print("DEMO 2: Triggering low energy homeostasis\n" + "-"*40)
    qfpl_engine.substrate.energy = 0.15 # Manually set low energy
    qfpl_engine.run("quantum_factoring", N=323) # This should trigger the energy absorption protocol
    print("\nFINAL SUBSTRATE STATE AFTER DEMO 2:")
    print(qfpl_engine.substrate.info())
    print("="*40 + "\n")

    # --- DEMO 3: Homeostasis Protocol (Low Coherence) ---
    print("DEMO 3: Triggering low coherence homeostasis\n" + "-"*40)
    qfpl_engine.substrate.entropy = 0.8 # Manually set high entropy
    qfpl_engine.run("quantum_field_simulation") # This should trigger the error correction protocol
    print("\nFINAL SUBSTRATE STATE AFTER DEMO 3:")
    print(qfpl_engine.substrate.info())
    print("="*40 + "\n")

    # --- DEMO 4: Substrate Cost Check ---
    print("DEMO 4: Aborting due to insufficient energy\n" + "-"*40)
    qfpl_engine.substrate.energy = 0.1
    qfpl_engine.run("quantum_factoring", N=997) # This should be aborted
    print("\nFINAL SUBSTRATE STATE AFTER DEMO 4:")
    print(qfpl_engine.substrate.info())
    print("="*40 + "\n")
