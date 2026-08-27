INITIAL_STATE = {
    "hp": 100,
    "resolve": 100,
    "morality": 50,
}

NODES = {
    "intro": {
        "title": "Prologue: The Echoes of Aethelgard",
        "bg_image": "INTRO_STATE",
        "is_intro": True,
        "dialogue_sequence": [
            {
                "speaker": "narration",
                "text": "The year is 2026. Aethelgard, the shining pinnacle of the old world, has fallen completely silent behind locked iron gates.",
            },
            {
                "speaker": "narration",
                "text": "Rumors speak of a sudden psychological madness that consumed the kingdom within, leaving behind nothing but ruins and desperate survivors.",
            },
            {
                "speaker": "narration",
                "text": "You are an Investigator. Your mission: navigate the fading paths, face the moral weights of those left behind, and uncover the truth.",
            },
            {
                "speaker": "narration",
                "text": "Every decision you make will constrain your state-space. Protecting your morality will drain your physical endurance. Choose wisely.",
            },
        ],
        "next_node": "1",
    },

    "1": {
        "title": "The Silent Gates",
        "bg_image": "bg_1_silent_gates.png",
        "dialogue_sequence": [
            {
                "speaker": "mc",
                "expression": "ch_mc_base.png",
                "text": "The iron gates are colder than I expected. The wind passing through these stone arches smells like ozone and damp soil.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "Aethelgard. Standing before what's left of it... you'd never guess thousands of people lived here just weeks ago.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "Wait. I hear shouting near the entry wall. Someone is still alive.",
            },
            {
                "speaker": "npc1",
                "name": "Captain Vance",
                "character": "ch_guard_base.png",
                "text": "Hey! You there with the coat! Step away from those lower grates. If you want to survive, follow me up the sunlit upper walls. It's clean and unblocked!",
            },
            {
                "speaker": "npc2",
                "name": "Elian the Archivist",
                "character": "ch_archivist_base.png",
                "text": "Do not listen to that deserter, traveler! The upper masonry is completely unstable. Help me carry these historical archives through the aqueducts instead!",
            },
            {
                "speaker": "npc1",
                "name": "Captain Vance",
                "character": "ch_guard_paranoid.png",
                "text": "I know every stone in this city, old man. I mapped the patrol routes for twelve years. The aqueducts are flooded and toxic.",
            },
            {
                "speaker": "npc2",
                "name": "Elian the Archivist",
                "character": "ch_archivist_sorrowful.png",
                "text": "And I spent thirty years cataloging every text in that archive. Without them, the world will never know what happened here.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "Both paths look dangerous. The guard seems confident, but he abandoned his post. The archivist is honest, but he moves slowly. Who do I trust?",
            },
        ],
        "choice_a": {
            "text": "Trust Captain Vance and take the sunlit upper walls.",
            "next_node": "1a",
            "stat_changes": {"hp": +10, "resolve": +10, "morality": -15},
            "char_expression": "ch_guard_smug.png",
        },
        "choice_b": {
            "text": "Trust Elian and help him carry the heavy archives.",
            "next_node": "1b",
            "stat_changes": {"hp": -20, "resolve": -10, "morality": +20},
        },
    },

    "1a": {
        "title": "The Sunlit Courtyard",
        "bg_image": "bg_1a_sunlit_courtyard.png",
        "dialogue_sequence": [
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "The path up here is warm, sunlight streaming through shattered stained glass. But the gate behind us is sealed shut.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "The archivist... he was right behind us. I heard him calling out. And now silence. Vance, you monster.",
            },
            {
                "speaker": "npc1",
                "name": "Chancellor Malakor",
                "character": "ch_chancellor_base.png",
                "text": "Help... please... The ceiling gave way when the structural pillars split. I'm pinned under this stone rubble... I can't breathe...",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "That's the King's Chancellor. Malakor. I'd recognize that silk robe anywhere. He's crushed under a collapsed pillar.",
            },
            {
                "speaker": "npc2",
                "name": "Garrick the Rebel",
                "character": "ch_rebel_base.png",
                "text": "Psst! Leave that old politician to rot, traveler. He hoarded food while the people starved. Follow me and I'll open the secret royal armory for you.",
            },
            {
                "speaker": "npc1",
                "name": "Chancellor Malakor",
                "character": "ch_chancellor_pleading.png",
                "text": "Don't listen to him... I have information about why the city fell. Please... I can barely feel my legs...",
            },
            {
                "speaker": "npc2",
                "name": "Garrick the Rebel",
                "character": "ch_rebel_scheming.png",
                "text": "Information doesn't fill your stomach, traveler. The armory has weapons, food, armor. Help me, and you walk out of here loaded.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "The chancellor knows why Aethelgard fell. But he's pinned under tons of stone. Lifting that pillar will cost me everything. The rebel's path is easy... but at what cost?",
            },
        ],
        "choice_a": {
            "text": "Heave the heavy stone pillar to save Chancellor Malakor.",
            "next_node": "coming_soon",
            "stat_changes": {"hp": -25, "resolve": -15, "morality": +25},
            "char_expression": "ch_chancellor_pleading.png",
        },
        "choice_b": {
            "text": "Abandon Malakor and follow Garrick to the armory.",
            "next_node": "coming_soon",
            "stat_changes": {"hp": +15, "resolve": +20, "morality": -20},
            "char_expression": "ch_rebel_scheming.png",
        },
    },
    "1b": {
        "title": "The Collapsed Aqueducts",
        "bg_image": "bg_1b_collapsed_aqueducts.png",
        "dialogue_sequence": [
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "These stone tunnels are pitch black. My boots are soaking wet and my hands are cut up from the iron edges.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "The archivist managed to light an oil lamp. The glow reveals a massive underground waterway... mostly collapsed.",
            },
            {
                "speaker": "npc1",
                "name": "Sylas the Smuggler",
                "character": "ch_smuggler_base.png",
                "text": "*Groans* Damn iron scraps... I'm bleeding out here. Give me that medical bandage from your pack, traveler, and I'll map out a route straight to a pristine vault.",
            },
            {
                "speaker": "npc2",
                "name": "Kira the Herbalist",
                "character": "ch_herbalist_base.png",
                "text": "Cold... so cold... The air down here is toxic... please... I just need something to bind my wounds...",
            },
            {
                "speaker": "npc1",
                "name": "Sylas the Smuggler",
                "character": "ch_smuggler_pain.png",
                "text": "Don't waste it on her, traveler. She's delirious. She won't last the night anyway. I can get us BOTH out alive.",
            },
            {
                "speaker": "npc2",
                "name": "Kira the Herbalist",
                "character": "ch_herbalist_confused.png",
                "text": "I... I can still help. I know which roots are safe to eat. Without me, you'll starve in the lower tunnels...",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "One bandage. That's all I have left. The smuggler offers a shortcut out. The herbalist offers survival knowledge. But only one of them can be saved.",
            },
        ],
        "choice_a": {
            "text": "Give your final bandage to the shivering Herbalist.",
            "next_node": "coming_soon",
            "stat_changes": {"hp": -15, "resolve": -20, "morality": +20},
            "char_expression": "ch_herbalist_grateful.png",
        },
        "choice_b": {
            "text": "Bandage the Smuggler to secure the route to the vault.",
            "next_node": "coming_soon",
            "stat_changes": {"hp": +20, "resolve": +15, "morality": -25},
            "char_expression": "ch_smuggler_confident.png",
        },
    },

    "coming_soon": {
        "title": "Stage 3 — Coming Soon",
        "bg_image": "INTRO_STATE",
        "is_ending": True,
        "dialogue_sequence": [
            {
                "speaker": "narration",
                "text": "The investigation continues deeper into Aethelgard... This section of the story is still being developed.",
            },
            {
                "speaker": "narration",
                "text": "The factor graph inference engine will dynamically shape the final encounters based on accumulated player decisions. Stay tuned.",
            },
        ],
    },
}
