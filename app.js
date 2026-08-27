/* Aphmau Soundboard — Web Audio playback with <audio> fallback */
(function () {
  "use strict";

  const SOUNDS = [
    // ⚡ "WHAT THE—?!" collection
    { id: "what-the-1", label: "What the?! #1", emoji: "😱", group: "whatthe" },
    { id: "what-the-2", label: "What the?! #2", emoji: "🤨", group: "whatthe" },
    { id: "what-the-3", label: "What the…? #3", emoji: "😳", group: "whatthe" },
    { id: "what-the-4", label: "What the?! #4", emoji: "🫨", group: "whatthe" },
    { id: "what-the-5", label: "What the?! #5", emoji: "😵", group: "whatthe" },
    { id: "what-the-6", label: "What the—?! #6", emoji: "👻", group: "whatthe" },

    // 💜 Classics
    { id: "oh-my-gosh", label: "Oh my gosh!", emoji: "🙀", group: "classics" },
    { id: "wait-what", label: "Wait wait… WHAT?", emoji: "⏸️", group: "classics" },
    { id: "no-no-no", label: "No no no!", emoji: "🙅", group: "classics" },
    { id: "oh-no-you-dont", label: "Oh no you don't!", emoji: "☝️", group: "classics" },
    { id: "so-cute", label: "She's SO cute!", emoji: "🥺", group: "classics" },
    { id: "what-is-that", label: "What is that?", emoji: "👀", group: "classics" },
    { id: "lets-go", label: "Let's go!", emoji: "🏃", group: "classics" },

    // 🔥 Maximum sass
    { id: "are-you-kidding-me", label: "Are you KIDDING me?", emoji: "🤬", group: "sass" },
    { id: "excuse-me", label: "Excuse me?!", emoji: "💅", group: "sass" },
    { id: "shut-up", label: "Shut up!", emoji: "🤐", group: "sass" },
    { id: "leave-me-alone", label: "Leave me alone!", emoji: "🚪", group: "sass" },
    { id: "get-out", label: "Get out!", emoji: "👉", group: "sass" },
    { id: "stop-it", label: "Stop it!", emoji: "✋", group: "sass" },

    // 🌙 Sleepy time
    { id: "time-for-bed", label: "Time for bed, you two!", emoji: "📣", group: "sleepy" },
    { id: "good-night", label: "Have a good night!", emoji: "🌙", group: "sleepy" },
    { id: "go-to-bed", label: "I have to go to bed", emoji: "🛏️", group: "sleepy" },
    { id: "back-to-sleep", label: "I'm really really tired…", emoji: "😴", group: "sleepy" },
    { id: "take-a-nap", label: "About to take a nap!", emoji: "💤", group: "sleepy" },
    { id: "wake-up", label: "Hey, wake up!", emoji: "⏰", group: "sleepy" },
    { id: "fell-asleep", label: "I almost fell asleep…", emoji: "🥱", group: "sleepy" },
    { id: "right-to-sleep", label: "Fell right to sleep!", emoji: "👶", group: "sleepy" },
    { id: "slumber-party", label: "Bestest slumber party EVER!", emoji: "🎉", group: "sleepy" },
    { id: "first-sleepover", label: "My first sleepover!", emoji: "🏠", group: "sleepy" },
    { id: "pajamas", label: "Still in my pajamas!", emoji: "🩳", group: "sleepy" },
  ];

  const grids = {
    whatthe: document.getElementById("grid-whatthe"),
    classics: document.getElementById("grid-classics"),
    sass: document.getElementById("grid-sass"),
    sleepy: document.getElementById("grid-sleepy"),
  };

  let audioCtx = null;
  const buffers = new Map();
  const fallbackPool = new Map();

  function ensureContext() {
    if (!audioCtx) {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (Ctx) audioCtx = new Ctx();
    }
    if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
    return audioCtx;
  }

  async function loadBuffer(id) {
    if (buffers.has(id)) return buffers.get(id);
    const ctx = ensureContext();
    if (!ctx) return null;
    try {
      const res = await fetch(`sounds/${id}.mp3`);
      const data = await res.arrayBuffer();
      const buf = await ctx.decodeAudioData(data);
      buffers.set(id, buf);
      return buf;
    } catch (err) {
      return null;
    }
  }

  function playFallback(id, onEnd) {
    let el = fallbackPool.get(id);
    if (!el) {
      el = new Audio(`sounds/${id}.mp3`);
      fallbackPool.set(id, el);
    }
    el.currentTime = 0;
    el.onended = onEnd;
    el.play().catch(() => onEnd());
  }

  async function play(id, btn) {
    if (navigator.vibrate) navigator.vibrate(15);
    btn.classList.add("playing");
    const done = () => btn.classList.remove("playing");

    const buf = await loadBuffer(id);
    if (buf && audioCtx) {
      const src = audioCtx.createBufferSource();
      src.buffer = buf;
      src.connect(audioCtx.destination);
      src.onended = done;
      src.start(0);
      // Safety net in case onended doesn't fire
      setTimeout(done, buf.duration * 1000 + 250);
    } else {
      playFallback(id, done);
    }
  }

  const allButtons = [];
  for (const sound of SOUNDS) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "sound-btn";
    btn.innerHTML = `<span class="emoji" aria-hidden="true">${sound.emoji}</span><span class="label">${sound.label}</span>`;
    btn.setAttribute("aria-label", `Play: ${sound.label}`);
    btn.addEventListener("click", () => play(sound.id, btn));
    grids[sound.group].appendChild(btn);
    allButtons.push({ sound, btn });
  }

  document.getElementById("random-btn").addEventListener("click", () => {
    const pick = allButtons[Math.floor(Math.random() * allButtons.length)];
    play(pick.sound.id, pick.btn);
  });

  // Warm the cache after the first user gesture (autoplay policies require one)
  const warm = () => {
    ensureContext();
    SOUNDS.forEach((s) => loadBuffer(s.id));
    window.removeEventListener("pointerdown", warm);
  };
  window.addEventListener("pointerdown", warm, { once: true });
})();
