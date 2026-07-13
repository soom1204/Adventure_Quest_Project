

INITIAL_STATE = {
    "hp": 100,
    "resolve": 100,
    "morality": 50,
}

NODES = {
    # ==================================================================
    # INTRO
    # ==================================================================
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

    # ==================================================================
    # STAGE 1 — THE ENTRANCE
    # ==================================================================
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
            "char_expression": "ch_archivist_sorrowful.png",
        },
        "post_choice_a": [
            {
                "speaker": "npc1",
                "name": "Captain Vance",
                "character": "ch_guard_smug.png",
                "text": "Smart choice, traveler. Keep up and watch your footing on the upper stones.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "Vance moves quickly. As we climb the sunlit ramp, I hear the archivist shouting something behind us...",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "Wait... he's gone quiet. Vance, did you close the lower gate? The one leading to the aqueducts?",
            },
            {
                "speaker": "npc1",
                "name": "Captain Vance",
                "character": "ch_guard_paranoid.png",
                "text": "That gate was going to collapse anyway. I just sped up the process. Don't look back. We're alive. That's what matters.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "My morality weighs on me, but the path ahead is clear and warm. I can't go back now.",
            },
        ],
        "post_choice_b": [
            {
                "speaker": "npc2",
                "name": "Elian the Archivist",
                "character": "ch_archivist_serene.png",
                "text": "Thank you, traveler. These records contain the voices of a thousand scholars. They deserve to be carried out.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "The archives are brutally heavy. Each step through the lower grates tears at my shoulders. The stone is slick and jagged.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "My hands are bleeding from the iron edges. But the archivist is smiling... he's humming an old song.",
            },
            {
                "speaker": "npc2",
                "name": "Elian the Archivist",
                "character": "ch_archivist_serene.png",
                "text": "You have a good heart, Investigator. Not many would carry a dead man's words through a dying city.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "We push deeper into the dark tunnels. My body aches, but at least I know I did the right thing... I think.",
            },
        ],
    },

    # ==================================================================
    # STAGE 2 — THE INNER WALLS
    # ==================================================================
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
            "next_node": "1a1",
            "stat_changes": {"hp": -25, "resolve": -15, "morality": +25},
            "char_expression": "ch_chancellor_pleading.png",
        },
        "choice_b": {
            "text": "Abandon Malakor and follow Garrick to the armory.",
            "next_node": "1a2",
            "stat_changes": {"hp": +15, "resolve": +20, "morality": -20},
            "char_expression": "ch_rebel_scheming.png",
        },
        "post_choice_a": [
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "*straining* The pillar... won't... budge... Come on! Almost... there!",
            },
            {
                "speaker": "npc1",
                "name": "Chancellor Malakor",
                "character": "ch_chancellor_relieved.png",
                "text": "Gods... you actually did it. My ribs are cracked, but I can move. Thank you, Investigator. I owe you my life.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "My shoulder is screaming. Blood is running down my arm. But Malakor is alive. He's reaching into his robe...",
            },
            {
                "speaker": "npc1",
                "name": "Chancellor Malakor",
                "character": "ch_chancellor_relieved.png",
                "text": "Take this map. It shows the old dungeons beneath the city. The truth about the quarantine is buried down there.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "The floor just cracked beneath us. The pillar I moved was load-bearing. We need to move. Now.",
            },
        ],
        "post_choice_b": [
            {
                "speaker": "npc2",
                "name": "Garrick the Rebel",
                "character": "ch_rebel_scheming.png",
                "text": "Good call, traveler. That old fossil had it coming. Follow me, the armory entrance is just through this corridor.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "As we walk away, I hear Malakor's voice fading behind us. 'Please... don't leave me...' I keep walking.",
            },
            {
                "speaker": "npc1",
                "name": "Chancellor Malakor",
                "character": "ch_chancellor_pleading.png",
                "text": "*fading* Someone... anyone... please... I have the quarantine codes... I know why we locked ourselves in...",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "The corridor goes quiet. My resolve hardens, but something in my chest feels hollow. The armory is just ahead.",
            },
        ],
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
            "next_node": "1b1",
            "stat_changes": {"hp": -15, "resolve": -20, "morality": +20},
            "char_expression": "ch_herbalist_grateful.png",
        },
        "choice_b": {
            "text": "Bandage the Smuggler to secure the route to the vault.",
            "next_node": "1b2",
            "stat_changes": {"hp": +20, "resolve": +15, "morality": -25},
            "char_expression": "ch_smuggler_confident.png",
        },
        "post_choice_a": [
            {
                "speaker": "npc2",
                "name": "Kira the Herbalist",
                "character": "ch_herbalist_grateful.png",
                "text": "You... you saved me. I won't forget this. Let me bind your wounds too. These roots can slow the bleeding.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "Kira's hands are shaking, but she works quickly. The herbal paste stings but it helps. Sylas just watches from the shadows.",
            },
            {
                "speaker": "npc1",
                "name": "Sylas the Smuggler",
                "character": "ch_smuggler_pain.png",
                "text": "You'll regret that choice, traveler. The tunnels ahead are a maze. Without my map, you'll wander until you drop.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "Maybe. But Kira is alive. And she knows these tunnels better than any smuggler's map. We push forward together.",
            },
        ],
        "post_choice_b": [
            {
                "speaker": "npc1",
                "name": "Sylas the Smuggler",
                "character": "ch_smuggler_confident.png",
                "text": "Now that's the smart play. Give me a minute to patch up... there. Good as new. Follow me, I know a shortcut.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "Behind us, Kira has gone silent. I turn to look... her breathing is shallow. Her skin is gray.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "She's still alive, but barely. Sylas doesn't look back. 'She made her choice,' he says. No. I made her choice.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "The vault route is clean and well-lit. My body recovers quickly on this path. But the image of her face won't leave my mind.",
            },
        ],
    },

    # ==================================================================
    # STAGE 3 — THE DEEP CITY (IN PROGRESS)
    # ==================================================================
    "1a1": {
        "title": "The Ruined Dungeons",
        "bg_image": "bg_1_silent_gates.png",
        "dialogue_sequence": [
            {
                "speaker": "narration",
                "text": "The dungeon stairwell descends into cold darkness. Rusted chains rattle against the walls as moisture drips from above.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "Malakor's map leads down here, but the structural damage is worse than he warned. Half the cells have caved in.",
            },
        ],
        "choice_a": {
            "text": "Push deeper into the lower cells to find another way through.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": -10, "resolve": +5, "morality": +5},
        },
        "choice_b": {
            "text": "Search the collapsed upper corridor for salvageable supplies.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": +5, "resolve": -5, "morality": -5},
        },
    },
    "1a2": {
        "title": "The Gilded Armory",
        "bg_image": "bg_1_silent_gates.png",
        "dialogue_sequence": [
            {
                "speaker": "narration",
                "text": "The armory corridor opens into a vaulted chamber lined with weapon racks and dented armor. Most of it has been looted.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "Garrick wasn't lying. There's enough gear here to outfit a small militia. But the ceiling groans under the shifting weight.",
            },
        ],
        "choice_a": {
            "text": "Grab what you can carry and move on before the ceiling collapses.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": +10, "resolve": +5, "morality": -10},
        },
        "choice_b": {
            "text": "Leave the armory untouched for any other survivors who might need it.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": -5, "resolve": -5, "morality": +10},
        },
    },
    "1b1": {
        "title": "The Toxic Gardens",
        "bg_image": "bg_1_silent_gates.png",
        "dialogue_sequence": [
            {
                "speaker": "narration",
                "text": "The overgrown gardens emit a faint yellow spore that burns the throat. Kira identifies the safe plants, but the toxic ones dominate.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_exhausted.png",
                "text": "Every breath down here feels like swallowing glass. Kira is guiding us through, but the path is getting narrower.",
            },
        ],
        "choice_a": {
            "text": "Follow Kira deeper into the overgrown tunnels, trusting her knowledge.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": -10, "resolve": -10, "morality": +10},
        },
        "choice_b": {
            "text": "Take the clearer side passage even if it means leaving Kira behind.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": +10, "resolve": +5, "morality": -15},
        },
    },
    "1b2": {
        "title": "The Secret Vault",
        "bg_image": "bg_1_silent_gates.png",
        "dialogue_sequence": [
            {
                "speaker": "narration",
                "text": "The vault is pristine. Rows of sealed documents line the walls. Sylas moves through the space like he's been here before.",
            },
            {
                "speaker": "mc",
                "expression": "ch_mc_focused.png",
                "text": "Thousands of citizen records. Names, addresses, family connections. In the wrong hands, this could destroy lives.",
            },
        ],
        "choice_a": {
            "text": "Help Sylas load the records onto his cart for transport outside.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": +10, "resolve": +10, "morality": -15},
        },
        "choice_b": {
            "text": "Refuse to help and search for a way to secure the records instead.",
            "next_node": "ending_placeholder",
            "stat_changes": {"hp": -5, "resolve": -10, "morality": +15},
        },
    },

    # ==================================================================
    # PLACEHOLDER ENDING (STAGES 4-5 IN PROGRESS)
    # ==================================================================
    "ending_placeholder": {
        "title": "Chapter Incomplete",
        "bg_image": "bg_1_silent_gates.png",
        "is_ending": True,
        "dialogue_sequence": [
            {
                "speaker": "narration",
                "text": "This chapter is still being developed. The remaining story branches, final crossroads, and multiple endings will be available in the next milestone.",
            },
        ],
    },
}
