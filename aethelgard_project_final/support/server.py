import os
import uuid
from flask import Flask, jsonify, request, send_from_directory, session
from support.ai_engine import GameEngine

app = Flask(__name__, static_folder=None)
app.secret_key = os.urandom(32)

engines = {}

STAGE_NAMES = ["Prologue", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "The End"]


def get_engine():
    eid = session.get("engine_id")
    if eid and eid in engines:
        return engines[eid]
    eid = uuid.uuid4().hex
    session["engine_id"] = eid
    engines[eid] = GameEngine()
    return engines[eid]


def determine_characters(seq, idx):
    mc, n1, n2 = None, None, None
    n1_name, n2_name = "NPC", "NPC"
    for i in range(min(idx + 1, len(seq))):
        ln = seq[i]
        spk = ln.get("speaker", "")
        if spk == "mc":
            mc = ln.get("expression", "ch_mc_base.png")
        elif spk == "npc1":
            n1 = ln.get("character", n1)
            n1_name = ln.get("name", n1_name)
        elif spk == "npc2":
            n2 = ln.get("character", n2)
            n2_name = ln.get("name", n2_name)
    return mc, n1, n2, n1_name, n2_name


def build_state(eng):
    node = eng.get_current_node()
    if not node:
        return None

    if eng.is_post_choice_active():
        seq = eng.post_choice_dialogues
        idx = eng.post_choice_index
    else:
        seq = node.get("dialogue_sequence", [])
        idx = eng.current_dialogue_index

    dialogue = None
    if idx < len(seq):
        dialogue = seq[idx]

    mc, n1, n2, n1_name, n2_name = determine_characters(seq, idx)

    characters = {}
    if mc:
        characters["mc"] = f"/assets/characters/{mc}"
    if n1:
        characters["npc1"] = {"image": f"/assets/characters/{n1}", "name": n1_name}
    if n2:
        characters["npc2"] = {"image": f"/assets/characters/{n2}", "name": n2_name}

    bg_image = node.get("bg_image", "")
    if bg_image and bg_image != "INTRO_STATE":
        bg_image = f"/assets/backgrounds/{bg_image}"

    stage = eng.get_stage()
    is_intro = node.get("is_intro", False)
    is_ending = node.get("is_ending", False)
    finished = eng.is_dialogue_finished()

    choices = None
    if not eng.is_post_choice_active() and finished and not is_intro and not is_ending:
        ca = node.get("choice_a")
        cb = node.get("choice_b")
        if ca and cb:
            choices = {
                "a": {"text": ca["text"], "expression": ca.get("character", "")},
                "b": {"text": cb["text"], "expression": cb.get("character", "")},
            }

    dialogue_data = None
    if dialogue:
        dialogue_data = {
            "speaker": dialogue.get("speaker", ""),
            "text": dialogue.get("text", ""),
        }
        if dialogue.get("speaker") == "narration":
            dialogue_data["type"] = "narration"
        elif dialogue.get("speaker") == "mc":
            dialogue_data["type"] = "speech"
            dialogue_data["character"] = f"/assets/characters/{dialogue.get('expression', '')}" if dialogue.get("expression") else ""
            dialogue_data["name"] = "Investigator"
        else:
            dialogue_data["type"] = "speech"
            dialogue_data["character"] = f"/assets/characters/{dialogue.get('character', '')}" if dialogue.get("character") else ""
            dialogue_data["name"] = dialogue.get("name", "NPC")

    graph_state = None
    if choices is not None:
        eng.build_graph_for_current_scene()
        graph_state = eng.get_graph_state()

    return {
        "node_id": eng.current_node_id,
        "title": node.get("title", ""),
        "bg_image": bg_image,
        "is_intro": is_intro,
        "is_ending": is_ending,
        "dialogue": dialogue_data,
        "characters": characters,
        "stats": eng.get_player_stats(),
        "stage": stage,
        "stage_name": STAGE_NAMES[stage] if stage < len(STAGE_NAMES) else "The End",
        "dialogue_finished": finished,
        "has_choices": choices is not None,
        "choices": choices,
        "factor_graph": graph_state,
        "hidden_consequences": eng.hidden_consequences[-3:],
    }


_PACKAGE_DIR = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.abspath(os.path.join(_PACKAGE_DIR, ".."))
WEB_DIR = os.path.join(_PACKAGE_DIR, "web")
ASSETS_DIR = os.path.join(_PROJECT_ROOT, "data", "assets")


@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/web/<path:filename>")
def web_assets(filename):
    return send_from_directory(WEB_DIR, filename)


@app.route("/assets/<path:filename>")
def game_assets(filename):
    if "backgrounds" in filename:
        fname = os.path.basename(filename)
        return send_from_directory(os.path.join(ASSETS_DIR, "backgrounds"), fname)
    elif "characters" in filename:
        fname = os.path.basename(filename)
        return send_from_directory(os.path.join(ASSETS_DIR, "characters"), fname)
    return send_from_directory(ASSETS_DIR, filename)


@app.route("/api/new-game", methods=["POST"])
def new_game():
    eng = get_engine()
    eng.reset_game()
    return jsonify(build_state(eng))


@app.route("/api/advance", methods=["POST"])
def advance():
    eng = get_engine()

    if eng.is_post_choice_active():
        if eng.is_dialogue_finished():
            eng.complete_post_choice()
        else:
            eng.advance_dialogue()
    elif eng.get_current_node() and eng.get_current_node().get("is_intro"):
        has_more = eng.advance_dialogue()
        if not has_more:
            eng.make_choice(None)
    else:
        if not eng.is_dialogue_finished():
            eng.advance_dialogue()

    return jsonify(build_state(eng))


@app.route("/api/choice", methods=["POST"])
def choice():
    eng = get_engine()
    data = request.get_json(force=True) or {}
    key = data.get("key", "choice_a")
    eng.make_choice(key)
    return jsonify(build_state(eng))


@app.route("/api/reset", methods=["POST"])
def reset():
    eng = get_engine()
    eng.reset_game()
    return jsonify(build_state(eng))


def run(host="0.0.0.0", port=5000):
    print("\n  Aethelgard - Web Edition")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(host=host, port=port, debug=False)
