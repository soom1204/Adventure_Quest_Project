import math
import random
from narrative_data import NODES, INITIAL_STATE


class VariableNode:
    def __init__(self, name, mean, variance, lo=0, hi=100, description=""):
        self.name = name
        self.mean = float(mean)
        self.variance = max(float(variance), 1.0)
        self.lo = lo
        self.hi = hi
        self.description = description
        self.messages = {}
        self.belief_history = [(self.mean, self.variance)]

    @property
    def std(self):
        return math.sqrt(self.variance)

    def set_belief(self, mean, variance):
        self.mean = max(self.lo, min(self.hi, float(mean)))
        self.variance = max(1.0, float(variance))
        self.belief_history.append((self.mean, self.variance))

    def receive_message(self, sender_name, mean, variance):
        self.messages[sender_name] = (mean, variance)

    def update_belief(self):
        if not self.messages:
            return
        prior_prec = 1.0 / self.variance
        total_prec = prior_prec
        total_weighted = self.mean * prior_prec
        for (m, v) in self.messages.values():
            prec = 1.0 / max(v, 1.0)
            total_prec = prec
            total_weighted += m * prec
        if total_prec > 0:
            self.set_belief(total_weighted / total_prec, 1.0 / total_prec)

    def to_dict(self):
        return {
            "name": self.name, "mean": round(self.mean, 2),
            "variance": round(self.variance, 2), "std": round(self.std, 2),
            "lo": self.lo, "hi": self.hi, "description": self.description,
        }


class FactorNode:
    def __init__(self, name, variable_names, factor_fn, description=""):
        self.name = name
        self.variable_names = variable_names
        self.factor_fn = factor_fn
        self.description = description
        self.last_output = None

    def compute_messages(self, variables):
        msgs = {}
        for target in self.variable_names:
            msgs[target] = self._importance_sample(target, variables)
        return msgs

    def _importance_sample(self, target, variables, n_samples=300):
        weighted_values, weights = [], []
        target_var = variables[target]
        for _ in range(n_samples):
            values = {}
            for vname in self.variable_names:
                v = variables[vname]
                values[vname] = max(v.lo, min(v.hi, random.gauss(v.mean, v.std)))
            try:
                score = max(self.factor_fn(values), 0.001)
            except Exception:
                score = 0.001
            weighted_values.append(values[target])
            weights.append(score)
        total_w = sum(weights)
        if total_w <= 0 or not weighted_values:
            return target_var.mean, target_var.variance
        mean = sum(w * v for w, v in zip(weights, weighted_values)) / total_w
        var = sum(w * (v - mean) ** 2 for w, v in zip(weights, weighted_values)) / total_w
        n = mean
        prior_prec = 1.0 / target_var.variance
        data_prec = 1.0 / max(var, 1.0)
        blend = 0.6
        bmean = (blend * data_prec * mean + (1 - blend) * prior_prec * target_var.mean) / (blend * data_prec + (1 - blend) * prior_prec)
        bvar = 1.0 / (blend * data_prec + (1 - blend) * prior_prec)
        return bmean, max(bvar, 1.0)

    def to_dict(self):
        return {"name": self.name, "variables": self.variable_names,
                "description": self.description, "last_output": self.last_output}


class FactorGraph:
    def __init__(self):
        self.variables = {}
        self.factors = {}
        self.edges = []

    def add_variable(self, name, mean, variance, lo=0, hi=100, description=""):
        self.variables[name] = VariableNode(name, mean, variance, lo, hi, description)

    def add_factor(self, name, variable_names, factor_fn, description=""):
        f = FactorNode(name, variable_names, factor_fn, description)
        self.factors[name] = f
        for v in variable_names:
            self.edges.append((name, v))

    def infer(self, iterations=4):
        for _ in range(iterations):
            for fname, factor in self.factors.items():
                msgs = factor.compute_messages(self.variables)
                for vname, (m, v) in msgs.items():
                    if vname in self.variables:
                        self.variables[vname].receive_message(fname, m, v)
            for var in self.variables.values():
                var.update_belief()

    def get_variable(self, name):
        return self.variables.get(name)

    def to_dict(self):
        return {
            "variables": {n: v.to_dict() for n, v in self.variables.items()},
            "factors": {n: f.to_dict() for n, f in self.factors.items()},
            "edges": self.edges,
        }


def _clamp(val, lo, hi):
    return max(lo, min(hi, val))


def build_scene_graph(node_id, player_state, history):
    hp = player_state.get("hp", 50)
    morality = player_state.get("morality", 50)
    resolve = player_state.get("resolve", 50)
    graph = FactorGraph()

    n_choices = len(history)
    fatigue = max(0, min(100, n_choices * 12))

    graph.add_variable("hp", hp, 2, 0, 100, "Player health (observed)")
    graph.add_variable("resolve", resolve, 2, 0, 100, "Player resolve (observed)")
    graph.add_variable("morality_stat", morality, 2, 0, 100, "Player morality (observed)")

    graph.add_variable("threat_level", min(40 + n_choices * 5 + fatigue * 0.3, 95), 18, 0, 100, "Current danger level")
    npc1_base = _clamp(40 + morality * 0.2 + random.gauss(0, 5), 10, 90)
    npc2_base = _clamp(45 + morality * 0.15 + random.gauss(0, 5), 10, 90)
    graph.add_variable("npc1_trust", npc1_base, 25, 0, 100, "First NPC trustworthiness")
    graph.add_variable("npc2_trust", npc2_base, 25, 0, 100, "Second NPC trustworthiness")
    graph.add_variable("resource_scarcity", min(15 + n_choices * 8, 90), 15, 0, 100, "Resource scarcity")
    graph.add_variable("knowledge_value", 40 + n_choices * 3, 20, 0, 100, "Value of information")
    graph.add_variable("moral_weight", morality, 20, 0, 100, "Moral significance of decision")

    def f_danger(vals):
        return _clamp(vals["threat_level"] * (1.0 + max(0, 100 - vals["hp"]) / 200.0), 0, 100)

    graph.add_factor("f_danger", ["threat_level", "hp"], f_danger, "Amplifies threat when HP is low")

    def f_betrayal_npc1(vals):
        return _clamp((100 - vals["npc1_trust"]) * 0.4 + vals["threat_level"] * 0.3, 0, 100)

    graph.add_factor("f_betrayal_npc1", ["npc1_trust", "threat_level"], f_betrayal_npc1, "Trust vs threat for NPC1")

    def f_betrayal_npc2(vals):
        return _clamp((100 - vals["npc2_trust"]) * 0.35 + vals["threat_level"] * 0.25, 0, 100)

    graph.add_factor("f_betrayal_npc2", ["npc2_trust", "threat_level"], f_betrayal_npc2, "Trust vs threat for NPC2")

    def f_cost(vals):
        return _clamp(vals["resource_scarcity"] * 0.4 + vals["moral_weight"] * 0.3 + max(0, 100 - vals.get("resolve", 50)) * 0.2, 0, 100)

    graph.add_factor("f_cost", ["resource_scarcity", "moral_weight", "resolve"], f_cost, "Scarcity and moral weight amplify costs")

    return graph


def sample_stat_changes(graph, choice_key, base_changes):
    result = {}
    for stat, base_val in base_changes.items():
        jitter = random.gauss(0, abs(base_val) * 0.1) if base_val != 0 else 0
        result[stat] = round(base_val + jitter)

    if graph and graph.variables:
        threat = graph.variables.get("threat_level")
        scarcity = graph.variables.get("resource_scarcity")
        if threat and "hp" in result:
            threat_bonus = round((threat.mean - 50) * 0.1)
            result["hp"] = result["hp"] + threat_bonus
        if scarcity and "resolve" in result:
            scarcity_penalty = round((scarcity.mean - 50) * 0.08)
            result["resolve"] = result["resolve"] - scarcity_penalty

    return result


def compute_hidden_consequences(graph, choice_key):
    if not graph or not graph.variables:
        return []
    consequences = []
    threat = graph.variables.get("threat_level")
    if threat and threat.mean > 70:
        consequences.append("The high threat level weighs on your mind...")
    npc1_trust = graph.variables.get("npc1_trust")
    if npc1_trust and npc1_trust.mean < 30:
        consequences.append("Your distrust of others grows...")
    return consequences


class GameEngine:
    def __init__(self):
        self.state = dict(INITIAL_STATE)
        self.current_node_id = "intro"
        self.current_dialogue_index = 0
        self.history = []
        self.in_post_choice = False
        self.post_choice_dialogues = []
        self.post_choice_index = 0
        self.pending_next_node = None
        self.last_choice_key = None
        self.active_graph = None
        self.last_graph_result = None
        self.hidden_consequences = []

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
        seq = node.get("dialogue_sequence", [])
        if 0 <= self.current_dialogue_index < len(seq):
            return seq[self.current_dialogue_index]
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
        seq = node.get("dialogue_sequence", [])
        if self.current_dialogue_index < len(seq) - 1:
            self.current_dialogue_index += 1
            return True
        return False

    def is_dialogue_finished(self):
        if self.in_post_choice:
            return self.post_choice_index >= len(self.post_choice_dialogues) - 1
        node = self.get_current_node()
        if not node:
            return True
        return self.current_dialogue_index >= len(node.get("dialogue_sequence", [])) - 1

    def is_post_choice_active(self):
        return self.in_post_choice

    def get_stage(self):
        nid = self.current_node_id
        if nid == "intro": return 0
        if nid.startswith("ending"): return 5
        if len(nid) == 1: return 1
        if len(nid) == 2: return 1
        if len(nid) == 3: return 3
        if len(nid) == 4: return 4
        return 5

    def get_player_stats(self):
        return dict(self.state)

    def build_graph_for_current_scene(self):
        self.active_graph = build_scene_graph(self.current_node_id, self.state, self.history)
        self.active_graph.infer(iterations=4)
        self.last_graph_result = self.active_graph.to_dict()
        return self.active_graph

    def get_graph_state(self):
        if self.active_graph is None:
            return None
        return self.active_graph.to_dict()

    def make_choice(self, choice_key):
        node = self.get_current_node()
        if not node:
            return False
        if node.get("is_intro"):
            self.current_node_id = str(node.get("next_node"))
            self.current_dialogue_index = 0
        if node.get("is_ending"):
            return False
        choice_data = node.get(choice_key)
        if not choice_data:
            return False

        self.history.append({"node_id": self.current_node_id, "choice_made": choice_key, "pre_state": dict(self.state)})

        if self.active_graph is None:
            graph = self.build_graph_for_current_scene()
        else:
            graph = self.active_graph
        base_stat_changes = choice_data.get("stat_changes", {})
        sampled_changes = sample_stat_changes(graph, choice_key, base_stat_changes)

        hidden = compute_hidden_consequences(graph, choice_key)
        self.hidden_consequences.extend(hidden)

        for variable, delta in sampled_changes.items():
            if variable in self.state:
                self.state[variable] = max(0, min(100, self.state[variable] + delta))

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
        self.active_graph = None
        self.last_graph_result = None
        self.hidden_consequences = []
