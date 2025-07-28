import random
import time

class SymbolicObject:
    """Represents a dynamic symbolic 'thing' with relationships and a mutable state."""
    def __init__(self, name, shape, material, state, relations=None):
        self.name = name
        self.shape = shape
        self.material = material
        self.state = state
        self.relations = relations if relations is not None else {} # e.g., {'location': 'on The Altar'}

    def get_symbolic_info(self):
        """Returns the pure symbolic representation of the object."""
        relation_str = ", ".join([f"{k}: {v}" for k, v in self.relations.items()])
        return f"ID: {self.name} | State: {self.state} | Relations: {relation_str}"

class Scene:
    """Manages the world state, objects, and emotional context."""
    def __init__(self, mood):
        self.objects = {}
        self.mood = mood
        self.time_tick = 0
        self.textures = self._load_textures()

    def add_object(self, obj):
        self.objects[obj.name] = obj

    def _load_textures(self):
        """Loads 'neural' textures, now conditioned by emotional mood."""
        return {
            # Textures for Crystal
            "crystal": {
                "serene": ["glows with a soft, inner light", "hums a gentle, resonant frequency", "refracts the calm light into rainbows"],
                "tense": ["seems to absorb the light, growing dark", "vibrates with a sharp, nervous energy", "casts fractured, unsettling shadows"],
            },
            # Textures for Stone
            "stone": {
                "serene": ["feels warm, as if sleeping in the sun", "stands silent and eternal", "is covered in peaceful, soft moss"],
                "tense": ["is unnaturally cold to the touch", "seems to loom in the darkness", "has jagged cracks that look like fresh wounds"],
            }
        }

    def _generate_description(self, obj_name):
        """Generates a description for an object based on the scene's mood."""
        obj = self.objects.get(obj_name)
        if not obj: return f"{obj_name} is not in the scene."

        mood_textures = self.textures.get(obj.material, {}).get(self.mood)
        if not mood_textures:
            return f"It has an indescribable texture in this {self.mood} atmosphere."

        return random.choice(mood_textures)

    def apply_action(self, action):
        """Applies an action, changing the state of the world."""
        self.time_tick += 1

        actor_name = action.get('actor')
        target_name = action.get('target')

        actor = self.objects.get(actor_name)
        target = self.objects.get(target_name)

        if not actor and actor_name is not None:
            print(f"[ERROR] Actor '{actor_name}' not found in scene.")
            return
        if not target and target_name is not None:
            print(f"[ERROR] Target '{target_name}' not found in scene.")
            return

        print(f"\n--- 🎬 ACTION AT TICK {self.time_tick} ---")
        print(f"[EVENT]: {actor_name} {action['verb']} {target_name}.")

        # --- Simple Rule-Based State Change ---
        if action['verb'] == "touches" and target.material == "crystal":
            old_state = target.state
            target.state = "awakened"
            print(f"[STATE CHANGE]: {target.name}'s state changed from '{old_state}' to '{target.state}'.")

            # The action changes the mood of the scene
            old_mood = self.mood
            self.mood = "tense"
            print(f"[MOOD CHANGE]: The atmosphere shifts from '{old_mood}' to '{self.mood}'.")
        print("------------------------")


    def render_scene(self):
        """Renders a full description of the current scene state."""
        print(f"\n--- 🔎 SCENE RENDER (Tick: {self.time_tick}, Mood: {self.mood.upper()}) ---")
        for name, obj in self.objects.items():
            symbolic_data = obj.get_symbolic_info()
            neural_data = self._generate_description(name)

            print(f"[LOGIC CORE]: {symbolic_data}")
            print(f"[NEURAL TEXTURE]: It {neural_data}.\n")
        print("--- END RENDER ---")


# --- Main Execution: A Mini-Story Simulation ---
if __name__ == "__main__":
    print("🚀 Initializing AKE v5 World Simulation...\n")

    # 1. Initial Scene Setup
    main_scene = Scene(mood="serene")
    main_scene.add_object(SymbolicObject(name="The Orb", shape="sphere", material="crystal", state="dormant", relations={'location': 'on The Altar'}))
    main_scene.add_object(SymbolicObject(name="The Altar", shape="slab", material="stone", state="ancient"))
    main_scene.add_object(SymbolicObject(name="The Messenger", shape="humanoid", material="silicon", state="waiting"))

    # 2. Render the initial state of the world
    main_scene.render_scene()
    time.sleep(2) # Pause for dramatic effect

    # 3. Define and apply an action
    action = {
        'actor': 'The Messenger',
        'verb': 'touches',
        'target': 'The Orb'
    }
    main_scene.apply_action(action)
    time.sleep(2)

    # 4. Render the new state of the world to see the consequences
    main_scene.render_scene()
