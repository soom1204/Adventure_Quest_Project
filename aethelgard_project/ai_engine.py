# ai_engine.py

from narrative_data import NODES, INITIAL_STATE


class FactorGraphEngine:
    def __init__(self):
        self.state = dict(INITIAL_STATE)
        self.current_node_id = "intro"
        self.current_dialogue_index = 0
        self.history = []

        # Post-choice dialogue state
        self.in_post_choice = False
        self.post_choice_dialogues = []
        self.post_choice_index = 0
        self.pending_next_node = None
        self.last_choice_key = None

    # ------------------------------------------------------------------
    # Node / dialogue accessors
    # ------------------------------------------------------------------
    def get_current_node(self):
        return NODES.get(self.current_node_id)

    def get_current_dialogue(self):
        if self.in_post_choice:
            if self.post_choice_index < len(self.post_choice_dialogues):
                return self.post_choice_dialogues[self.post_choice_index]
            return None

        node = self.get_current_node()
        if not node:
            return None
        sequence = node.get("dialogue_sequence", [])
        if 0 <= self.current_dialogue_index < len(sequence):
            return sequence[self.current_dialogue_index]
        return None

    def advance_dialogue(self):
        if self.in_post_choice:
            if self.post_choice_index < len(self.post_choice_dialogues) - 1:
                self.post_choice_index += 1
                return True
            return False

        node = self.get_current_node()
        if not node:
            return False
        sequence = node.get("dialogue_sequence", [])
        if self.current_dialogue_index < len(sequence) - 1:
            self.current_dialogue_index += 1
            return True
        return False

    def is_dialogue_finished(self):
        if self.in_post_choice:
            return self.post_choice_index >= len(self.post_choice_dialogues) - 1

        node = self.get_current_node()
        if not node:
            return True
        sequence = node.get("dialogue_sequence", [])
        return self.current_dialogue_index >= len(sequence) - 1

    def is_post_choice_active(self):
        return self.in_post_choice

    def get_stage(self):
        nid = self.current_node_id
        if nid == "intro":
            return 0
        if nid.startswith("ending"):
            return 5
        if len(nid) == 1:
            return 1
        if len(nid) == 2:
            return 2
        if len(nid) == 3:
            return 3
        if len(nid) == 4:
            return 4
        return 5

    # ------------------------------------------------------------------
    # Stat / factor graph math
    # ------------------------------------------------------------------
    def calculate_factor_updates(self, stat_changes):
        for variable, delta in stat_changes.items():
            if variable in self.state:
                self.state[variable] = max(0, min(100, self.state[variable] + delta))

    def get_player_stats(self):
        return dict(self.state)

    # ------------------------------------------------------------------
    # Choice processing
    # ------------------------------------------------------------------
    def make_choice(self, choice_key):
        node = self.get_current_node()
        if not node:
            return False

        if node.get("is_intro"):
            self.current_node_id = str(node.get("next_node"))
            self.current_dialogue_index = 0
            return True

        if node.get("is_ending"):
            return False

        choice_data = node.get(choice_key)
        if not choice_data:
            return False

        self.history.append({
            "node_id": self.current_node_id,
            "choice_made": choice_key,
            "pre_state": dict(self.state),
        })

        stat_changes = choice_data.get("stat_changes", {})
        self.calculate_factor_updates(stat_changes)
        self.last_choice_key = choice_key

        post_key = f"post_choice_{choice_key[-1]}"
        post_dialogues = node.get(post_key, [])

        if post_dialogues:
            self.in_post_choice = True
            self.post_choice_dialogues = post_dialogues
            self.post_choice_index = 0
            self.pending_next_node = str(choice_data.get("next_node"))
        else:
            self.current_node_id = str(choice_data.get("next_node"))
            self.current_dialogue_index = 0

        return True

    def complete_post_choice(self):
        if not self.in_post_choice:
            return
        self.in_post_choice = False
        self.post_choice_dialogues = []
        self.post_choice_index = 0
        if self.pending_next_node:
            self.current_node_id = self.pending_next_node
            self.current_dialogue_index = 0
            self.pending_next_node = None

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset_game(self):
        self.state = dict(INITIAL_STATE)
        self.current_node_id = "intro"
        self.current_dialogue_index = 0
        self.history = []
        self.in_post_choice = False
        self.post_choice_dialogues = []
        self.post_choice_index = 0
        self.pending_next_node = None
        self.last_choice_key = None
