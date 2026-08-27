# Aethelgard — Adventure Quest

An interactive narrative game where player decisions shape the story's outcome, using by factor graphs.

## How it works

The game uses a factor graph at every decision point to decide what happens next based on the player's choices and hidden world variables.

- Observed variables (player stats like HP, resolve, morality) are known
- Hidden variables (NPC trust, threat level, resource scarcity, etc.) are inferred by the factor graph through loopy belief propagation
- These inferred beliefs carry over between scenes, so early decisions affect later outcomes
- Stat changes and hidden events (NPC betrayals, ambushes) are probabilistic, not hardcoded

There are 20 story nodes across 5 stages with 4 different endings. How you play determines which ending you get.

The factor graph uses Monte Carlo importance sampling inside its factors and product-of-Gaussians message passing for belief updates. Each belief is modeled as a Gaussian.

## How to run

```bash
pip install -r requirements.txt
python main.py
```

Then open http://localhost:5000 in your browser.

## API

| Endpoint        | Method | What it does                                          |
|-----------------|--------|-------------------------------------------------------|
| `/api/new-game` |  POST  | Start a new game                                      |
| `/api/advance`  |  POST  | Advance dialogue                                      |
| `/api/choice`   |  POST  | Make a choice (send `{"key": "a"}` or `{"key": "b"}`) |
| `/api/reset`    |  POST  | Reset to beginning                                    |

Every response includes the current factor graph state, which the "AI Brain" panel in the frontend uses to visualize the inference process.

## Repository structure

```
main.py               entry point
requirements.txt      dependencies
README.md             this file
support/              source code
    ai_engine.py      factor graph engine + game logic
    server.py         Flask backend
    narrative_data.py loads story data from JSON
data/
    narrative.json    story: 20 nodes, dialogues, choices, endings
web/                  frontend (HTML/CSS/JS)
assets/               background images and character portraits
others/               presentation slides, reports, demo video
```

## Reproducibility

You can pass a `seed` to `GameEngine(seed=<int>)` to get the same playthrough every time, which is useful for testing and making report figures.

## Group members

Soomaiya Chowdhury	    2211856042
Mahmudur Rahman Labib	2131214642
Shreysee Moni Shashy	2122043642
Shafi Mahadi Nowrose	2121620643
