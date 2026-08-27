import math
import random

from support.narrative_data import NODES, INITIAL_STATE

class VariableNode:
    def __init__(self, name, mean, variance, lo=0, hi=100, description="",
                 observed=False):
        self.name = name
        self.mean = float(mean)
        self.variance = max(float(variance), 1.0)
        self.lo = lo
        self.hi = hi
        self.description = description
        self.observed = observed
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
        if self.observed:
            self.messages.clear()
            return
        if not self.messages:
            return
        prior_prec = 1.0 / self.variance
        prior_mean_times_prec = self.mean * prior_prec
        total_prec = prior_prec
        total_weighted = prior_mean_times_prec
        for (m, v) in self.messages.values():
            prec = 1.0 / max(v, 1.0)
            total_prec += prec
            total_weighted += m * prec
        if total_prec > 0:
            new_mean = total_weighted / total_prec
            new_var = 1.0 / total_prec
            self.set_belief(new_mean, new_var)

    def to_dict(self):
        return {
            "name": self.name,
            "mean": round(self.mean, 2),
            "variance": round(self.variance, 2),
            "std": round(self.std, 2),
            "lo": self.lo,
            "hi": self.hi,
            "description": self.description,
            "observed": self.observed,
        }


class FactorNode:
    def __init__(self, name, variable_names, factor_fn, description="", rng=None):
        self.name = name
        self.variable_names = variable_names
        self.factor_fn = factor_fn
        self.description = description
        self.last_output = None
        self.rng = rng if rng is not None else random

    def compute_messages(self, variables):
        msgs = {}
        for target in self.variable_names:
            msg_mean, msg_var = self._importance_sample_for(target, variables)
            msgs[target] = (msg_mean, msg_var)
        return msgs

    def _importance_sample_for(self, target, variables, n_samples=300):
        weighted_values = []
        weights = []

        target_var = variables[target]

        for _ in range(n_samples):
            values = {}
            for vname in self.variable_names:
                v = variables[vname]
                values[vname] = self.rng.gauss(v.mean, v.std)
                values[vname] = max(v.lo, min(v.hi, values[vname]))

            try:
                score = self.factor_fn(values)
                if not isinstance(score, (int, float)):
                    score = 1.0
                score = max(score, 0.001)
            except Exception:
                score = 0.001

            weighted_values.append(values[target])
            weights.append(score)

        total_w = sum(weights)
        if total_w <= 0 or not weighted_values:
            return target_var.mean, target_var.variance

        mean = sum(w * v for w, v in zip(weights, weighted_values)) / total_w
        var = sum(w * (v - mean) ** 2 for w, v in zip(weights, weighted_values)) / total_w

        prior_prec = 1.0 / target_var.variance
        data_prec = 1.0 / max(var, 1.0)
        blend = 0.6
        blended_mean = (blend * data_prec * mean + (1 - blend) * prior_prec * target_var.mean) / (blend * data_prec + (1 - blend) * prior_prec)
        blended_var = 1.0 / (blend * data_prec + (1 - blend) * prior_prec)

        return blended_mean, max(blended_var, 1.0)

    def to_dict(self):
        return {
            "name": self.name,
            "variables": self.variable_names,
            "description": self.description,
            "last_output": self.last_output,
        }


class FactorGraph:
    def __init__(self, rng=None):
        self.rng = rng if rng is not None else random
        self.variables = {}
        self.factors = {}
        self.edges = []
        self.iterations_run = 0
        self.converged = False

    def add_variable(self, name, mean, variance, lo=0, hi=100, description="",
                     observed=False):
        self.variables[name] = VariableNode(name, mean, variance, lo, hi,
                                            description, observed)

    def add_factor(self, name, variable_names, factor_fn, description=""):
        f = FactorNode(name, variable_names, factor_fn, description, rng=self.rng)
        self.factors[name] = f
        for v in variable_names:
            self.edges.append((name, v))

    def infer(self, iterations=8, tol=0.05):
        self.converged = False
        for i in range(iterations):
            prev_means = {n: v.mean for n, v in self.variables.items()}
            for fname, factor in self.factors.items():
                msgs = factor.compute_messages(self.variables)
                for vname, (m, v) in msgs.items():
                    if vname in self.variables:
                        self.variables[vname].receive_message(fname, m, v)
            for vname, var in self.variables.items():
                var.update_belief()
            self.iterations_run = i + 1
            delta = max(
                (abs(self.variables[n].mean - m) for n, m in prev_means.items()),
                default=0.0,
            )
            if delta < tol:
                self.converged = True
                break

    def snapshot_beliefs(self):
        return {n: (v.mean, v.variance) for n, v in self.variables.items()}

    def get_variable(self, name):
        return self.variables.get(name)

    def to_dict(self):
        return {
            "variables": {n: v.to_dict() for n, v in self.variables.items()},
            "factors": {n: f.to_dict() for n, f in self.factors.items()},
            "edges": self.edges,
            "inference": {
                "iterations_run": self.iterations_run,
                "converged": self.converged,
            },
        }


def _clamp(val, lo, hi):
    return max(lo, min(hi, val))


_HIDDEN_VAR_SPECS = (
    ("threat_level", lambda ctx: min(ctx["base_threat"] + ctx["fatigue"] * 0.3, 95),
     18, "How dangerous the current situation is"),
    ("npc1_trust", lambda ctx: _clamp(40 + ctx["morality"] * 0.2 + ctx["rng"].gauss(0, 5), 10, 90),
     25, "Trustworthiness of the first NPC"),
    ("npc2_trust", lambda ctx: _clamp(45 + ctx["morality"] * 0.15 + ctx["rng"].gauss(0, 5), 10, 90),
     25, "Trustworthiness of the second NPC"),
    ("resource_scarcity", lambda ctx: min(ctx["base_scarcity"], 90),
     15, "How scarce resources are right now"),
    ("knowledge_value", lambda ctx: 40 + ctx["n_choices"] * 3,
     20, "Value of information at stake"),
    ("moral_weight", lambda ctx: ctx["morality"],
     20, "Moral significance of the coming decision"),
)


def build_scene_graph(node_id, player_state, history, carried_beliefs=None,
                      rng=None):
    rng = rng if rng is not None else random
    carried = carried_beliefs or {}

    hp = player_state.get("hp", 50)
    resolve = player_state.get("resolve", 50)
    morality = player_state.get("morality", 50)

    n_choices = len(history)
    fatigue = max(0, min(100, n_choices * 12))
    base_threat = 40 + n_choices * 5
    base_scarcity = 15 + n_choices * 8

    ctx = {
        "morality": morality,
        "fatigue": fatigue,
        "base_threat": base_threat,
        "base_scarcity": base_scarcity,
        "n_choices": n_choices,
        "rng": rng,
    }

    graph = FactorGraph(rng=rng)

    graph.add_variable("hp", hp, 2, 0, 100,
                       "Player health points (observed)", observed=True)
    graph.add_variable("resolve", resolve, 2, 0, 100,
                       "Player resolve (observed)", observed=True)
    graph.add_variable("morality_stat", morality, 2, 0, 100,
                       "Player morality (observed)", observed=True)

    for name, default_mean_fn, default_var, desc in _HIDDEN_VAR_SPECS:
        prior = carried.get(name)
        if prior is not None:
            mean0 = prior[0]
            var0 = max(prior[1] * 0.5, 4.0)
        else:
            mean0 = default_mean_fn(ctx)
            var0 = default_var
        graph.add_variable(name, mean0, var0, 0, 100, desc)

    def f_danger(vals):
        t = vals["threat_level"]
        h = vals["hp"]
        danger = t * (1.0 + max(0, (100 - h)) / 200.0)
        return _clamp(danger, 0, 100)

    graph.add_factor(
        "f_danger",
        ["threat_level", "hp"],
        f_danger,
        "Amplifies threat when player HP is low",
    )

    def f_betrayal_npc1(vals):
        trust = vals["npc1_trust"]
        threat = vals["threat_level"]
        betrayal = (100 - trust) * 0.4 + threat * 0.3
        return _clamp(betrayal, 0, 100)

    graph.add_factor(
        "f_betrayal_npc1",
        ["npc1_trust", "threat_level"],
        f_betrayal_npc1,
        "Higher threat + lower trust = more likely betrayal",
    )

    def f_betrayal_npc2(vals):
        trust = vals["npc2_trust"]
        threat = vals["threat_level"]
        betrayal = (100 - trust) * 0.35 + threat * 0.25
        return _clamp(betrayal, 0, 100)

    graph.add_factor(
        "f_betrayal_npc2",
        ["npc2_trust", "threat_level"],
        f_betrayal_npc2,
        "Trust vs danger balance for second NPC",
    )

    def f_morality_trust(vals):
        morality_v = vals["morality_stat"]
        t1 = vals["npc1_trust"]
        t2 = vals["npc2_trust"]
        avg_trust = (t1 + t2) / 2.0
        alignment = 100 - abs(morality_v - avg_trust)
        return _clamp(alignment, 0, 100)

    graph.add_factor(
        "f_morality_trust",
        ["morality_stat", "npc1_trust", "npc2_trust"],
        f_morality_trust,
        "High morality aligns with trusting NPCs",
    )

    def f_cross_trust(vals):
        t1 = vals["npc1_trust"]
        t2 = vals["npc2_trust"]
        balance = 100 - abs(t1 - t2) * 0.8
        return _clamp(balance, 0, 100)

    graph.add_factor(
        "f_cross_trust",
        ["npc1_trust", "npc2_trust"],
        f_cross_trust,
        "Balances trust between the two NPCs",
    )

    def f_cost(vals):
        scarcity = vals["resource_scarcity"]
        moral = vals["moral_weight"]
        resolve_v = vals.get("resolve", 50)
        cost = scarcity * 0.4 + moral * 0.3 + max(0, 100 - resolve_v) * 0.2
        return _clamp(cost, 0, 100)

    graph.add_factor(
        "f_cost",
        ["resource_scarcity", "moral_weight", "resolve"],
        f_cost,
        "Scarcity and moral weight amplify stat costs",
    )

    def f_utility(vals):
        knowledge = vals["knowledge_value"]
        threat = vals["threat_level"]
        moral = vals["moral_weight"]
        survival = max(0, 100 - threat) * 0.4 + knowledge * 0.3 + (100 - moral) * 0.15
        return _clamp(survival, 0, 100)

    graph.add_factor(
        "f_utility",
        ["knowledge_value", "threat_level", "moral_weight"],
        f_utility,
        "Balances survival against moral outcomes",
    )

    return graph


def sample_stat_changes(graph, base_changes):
    rng = graph.rng
    cost_var = graph.get_variable("resource_scarcity")
    scarcity = cost_var.mean / 100.0 if cost_var else 0.2

    moral_var = graph.get_variable("moral_weight")
    moral_w = moral_var.mean / 100.0 if moral_var else 0.5

    hp_cost_mult = 1.0 + scarcity * 0.5
    resolve_cost_mult = 1.0 + moral_w * 0.3

    threat_var = graph.get_variable("threat_level")
    threat = threat_var.mean if threat_var else 50.0
    threat_noise = rng.gauss(0, threat * 0.05)

    result = {}
    for stat, base_val in base_changes.items():
        if stat == "hp":
            scaled = base_val * hp_cost_mult + threat_noise
        elif stat == "resolve":
            scaled = base_val * resolve_cost_mult
        else:
            scaled = base_val
        jitter = rng.gauss(0, abs(base_val) * 0.15) if base_val != 0 else 0
        result[stat] = round(scaled + jitter)

    return result


def compute_hidden_consequences(graph, choice_index):
    rng = graph.rng
    consequences = []
    npc1 = graph.get_variable("npc1_trust")
    npc2 = graph.get_variable("npc2_trust")
    threat = graph.get_variable("threat_level")

    if choice_index == "a" and npc1:
        betrayal_prob = (100 - npc1.mean) * 0.4
        roll = rng.random() * 100
        if roll < betrayal_prob:
            consequences.append({
                "type": "npc_betrayal",
                "npc": "npc1",
                "probability": round(betrayal_prob, 1),
                "message": "Your chosen ally may not be as loyal as they seem...",
            })
    elif choice_index == "b" and npc2:
        betrayal_prob = (100 - npc2.mean) * 0.4
        roll = rng.random() * 100
        if roll < betrayal_prob:
            consequences.append({
                "type": "npc_betrayal",
                "npc": "npc2",
                "probability": round(betrayal_prob, 1),
                "message": "Trust is a fragile currency in Aethelgard...",
            })

    if threat and threat.mean > 65:
        roll = rng.random() * 100
        if roll < 20:
            consequences.append({
                "type": "ambush",
                "probability": round((threat.mean - 65) * 0.6, 1),
                "message": "The danger of this place lurks closer than you think...",
            })

    return consequences


def normalize_choice_key(choice_key):
    if not isinstance(choice_key, str):
        return ""
    k = choice_key.strip().lower()
    if k.startswith("choice_"):
        k = k[len("choice_"):]
    return k if k in ("a", "b") else ""


class GameEngine:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
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
        self.belief_carry = {}

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

    def get_player_stats(self):
        return dict(self.state)

    def build_graph_for_current_scene(self):
        self.active_graph = build_scene_graph(
            self.current_node_id, self.state, self.history,
            carried_beliefs=self.belief_carry, rng=self.rng,
        )
        self.active_graph.infer(iterations=8, tol=0.05)
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
            return True

        if node.get("is_ending"):
            return False

        choice_index = normalize_choice_key(choice_key)
        choice_data = node.get(f"choice_{choice_index}") if choice_index else None
        if not choice_data:
            return False

        self.history.append({
            "node_id": self.current_node_id,
            "choice_made": choice_index,
            "pre_state": dict(self.state),
        })

        if self.active_graph is None:
            graph = self.build_graph_for_current_scene()
        else:
            graph = self.active_graph
        base_stat_changes = choice_data.get("stat_changes", {})
        sampled_changes = sample_stat_changes(graph, base_stat_changes)

        for variable, delta in sampled_changes.items():
            if variable in self.state:
                self.state[variable] = max(0, min(100, self.state[variable] + delta))

        consequences = compute_hidden_consequences(graph, choice_index)
        self.hidden_consequences.extend(consequences)

        self.belief_carry = graph.snapshot_beliefs()

        self.last_choice_key = choice_index

        post_key = f"post_choice_{choice_index}"
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
        self.belief_carry = {}
