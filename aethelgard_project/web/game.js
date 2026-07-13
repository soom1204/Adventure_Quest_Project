(function () {
    "use strict";

    const $ = (s, p) => (p || document).querySelector(s);
    const $$ = (s, p) => [...(p || document).querySelectorAll(s)];

    const game = $("#game");
    let state = null;
    let busy = false;

    async function api(url, body) {
        const opts = body
            ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }
            : { method: "POST" };
        const res = await fetch(url, opts);
        return res.json();
    }

    async function newGame() {
        state = await api("/api/new-game");
        render();
    }

    async function advance() {
        if (busy) return;
        busy = true;
        state = await api("/api/advance");
        render();
        busy = false;
    }

    async function makeChoice(key) {
        if (busy) return;
        busy = true;
        state = await api("/api/choice", { key });
        render();
        busy = false;
    }

    async function resetGame() {
        if (busy) return;
        busy = true;
        state = await api("/api/reset");
        render();
        busy = false;
    }

    function render() {
        if (!state) return;
        game.innerHTML = "";

        if (state.is_intro) {
            renderIntro();
        } else {
            renderGame();
        }
    }

    function renderIntro() {
        const el = document.createElement("div");
        el.id = "intro-screen";

        const title = document.createElement("div");
        title.className = "intro-title";
        title.textContent = state.title.toUpperCase();
        el.appendChild(title);

        if (state.dialogue) {
            const text = document.createElement("div");
            text.className = "intro-text";
            text.textContent = state.dialogue.text;
            el.appendChild(text);
        }

        const hint = document.createElement("div");
        hint.className = "intro-hint";
        hint.textContent = "~ Click anywhere to continue ~";
        el.appendChild(hint);

        el.addEventListener("click", () => advance());
        game.appendChild(el);
    }

    function renderGame() {
        renderBackground();
        renderCharacters();

        if (state.dialogue) {
            renderDialogue();
        }

        if (state.has_choices) {
            renderChoices();
        } else if (!state.dialogue_finished) {
            renderContinueHint();
        }

        if (state.is_ending) {
            renderEnding();
        }
    }

    function renderBackground() {
        const layer = document.createElement("div");
        layer.id = "bg-layer";
        if (state.bg_image) {
            const img = document.createElement("img");
            img.src = state.bg_image;
            img.alt = "";
            img.draggable = false;
            layer.appendChild(img);
        }
        game.appendChild(layer);
    }

    function renderCharacters() {
        const layer = document.createElement("div");
        layer.id = "characters";

        const chars = state.characters;

        if (chars.mc) {
            const img = document.createElement("img");
            img.className = "char-img char-mc";
            img.src = chars.mc;
            img.alt = "";
            img.draggable = false;
            layer.appendChild(img);
        }

        if (chars.npc1) {
            const img = document.createElement("img");
            img.className = "char-img char-npc1";
            img.src = chars.npc1.image;
            img.alt = "";
            img.draggable = false;
            layer.appendChild(img);
        }

        if (chars.npc2) {
            const img = document.createElement("img");
            img.className = "char-img char-npc2";
            img.src = chars.npc2.image || chars.npc2;
            img.alt = "";
            img.draggable = false;
            layer.appendChild(img);
        }

        const unusedLayer = document.createElement("div");
        unusedLayer.id = "char-effects";

        game.appendChild(layer);
    }

    function renderDialogue() {
        const d = state.dialogue;
        if (!d) return;

        if (d.type === "narration") {
            renderNarration(d);
        } else {
            renderSpeechBubble(d);
        }
    }

    function renderSpeechBubble(d) {
        const isMc = d.speaker === "mc";
        const isNpc2 = d.speaker === "npc2";

        const bubble = document.createElement("div");
        bubble.className = "speech-bubble";
        bubble.style.top = "18%";

        if (isNpc2) {
            bubble.style.right = "2%";
            bubble.style.left = "auto";
        } else {
            bubble.style.left = isMc ? "2%" : "30%";
            bubble.style.right = "auto";
        }

        const nameEl = document.createElement("div");
        nameEl.className = "speaker-name " + (isMc ? "mc" : "npc");
        nameEl.textContent = d.name.toUpperCase();
        bubble.appendChild(nameEl);

        const divider = document.createElement("div");
        divider.className = "speaker-divider";
        bubble.appendChild(divider);

        const textEl = document.createElement("div");
        textEl.className = "speaker-text";
        textEl.textContent = d.text;
        bubble.appendChild(textEl);

        const tail = document.createElement("div");
        tail.className = "speech-tail " + (isNpc2 ? "right" : "left");
        bubble.appendChild(tail);

        bubble.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!state.has_choices) advance();
        });

        game.appendChild(bubble);
    }

    function renderNarration(d) {
        const panel = document.createElement("div");
        panel.className = "narration-panel";
        panel.style.top = "32%";

        const text = document.createElement("div");
        text.className = "narration-text";
        text.textContent = d.text;
        panel.appendChild(text);

        panel.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!state.has_choices && !state.is_ending) advance();
        });

        game.appendChild(panel);
    }

    function renderChoices() {
        const panel = document.createElement("div");
        panel.id = "choice-panel";

        for (const key of ["a", "b"]) {
            const c = state.choices[key];
            const btn = document.createElement("button");
            btn.className = "choice-btn";

            const label = document.createElement("span");
            label.className = "choice-label";
            label.textContent = key === "a" ? "I." : "II.";
            btn.appendChild(label);

            const txt = document.createElement("span");
            txt.textContent = c.text;
            btn.appendChild(txt);

            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                makeChoice("choice_" + key);
            });

            panel.appendChild(btn);
        }

        game.appendChild(panel);
    }

    function renderContinueHint() {
        const hint = document.createElement("div");
        hint.id = "continue-hint";
        hint.textContent = "~ Click to continue ~";
        game.appendChild(hint);
    }

    function renderEnding() {
        const overlay = document.createElement("div");
        overlay.id = "ending-overlay";
        overlay.className = "visible";

        const title = document.createElement("div");
        title.className = "ending-title";
        title.textContent = state.title;
        overlay.appendChild(title);

        if (state.dialogue) {
            const text = document.createElement("div");
            text.className = "ending-text";
            text.textContent = state.dialogue.text;
            overlay.appendChild(text);
        }

        const btn = document.createElement("button");
        btn.id = "play-again-btn";
        btn.textContent = "Play Again";
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            resetGame();
        });
        overlay.appendChild(btn);

        game.appendChild(overlay);
    }

    newGame();
})();
