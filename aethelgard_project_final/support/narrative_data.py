import json
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "narrative.json")

with open(_DATA_PATH, "r", encoding="utf-8") as f:
    _raw = json.load(f)

INITIAL_STATE = _raw["INITIAL_STATE"]
NODES = _raw["NODES"]
