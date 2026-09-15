/* Soundboards — Web Audio playback with <audio> fallback, swipeable boards */
(function () {
  "use strict";

  const SOUNDS = [
    // ═══ Board 0: Aphmau ═══
    // ⚡ "WHAT THE—?!" collection
    { id: "what-the-1", label: "What the?! #1", emoji: "😱", group: "whatthe", board: 0 },
    { id: "what-the-2", label: "What the?! #2", emoji: "🤨", group: "whatthe", board: 0 },
    { id: "what-the-3", label: "What the…? #3", emoji: "😳", group: "whatthe", board: 0 },
    { id: "what-the-4", label: "What the?! #4", emoji: "🫨", group: "whatthe", board: 0 },
    { id: "what-the-5", label: "What the?! #5", emoji: "😵", group: "whatthe", board: 0 },
    { id: "what-the-6", label: "What the—?! #6", emoji: "👻", group: "whatthe", board: 0 },

    // 💜 Classics
    { id: "oh-my-gosh", label: "Oh my gosh!", emoji: "🙀", group: "classics", board: 0 },
    { id: "wait-what", label: "Wait wait… WHAT?", emoji: "⏸️", group: "classics", board: 0 },
    { id: "no-no-no", label: "No no no!", emoji: "🙅", group: "classics", board: 0 },
    { id: "oh-no-you-dont", label: "Oh no you don't!", emoji: "☝️", group: "classics", board: 0 },
    { id: "so-cute", label: "She's SO cute!", emoji: "🥺", group: "classics", board: 0 },
    { id: "what-is-that", label: "What is that?", emoji: "👀", group: "classics", board: 0 },
    { id: "lets-go", label: "Let's go!", emoji: "🏃", group: "classics", board: 0 },

    // 🔥 Maximum sass
    { id: "are-you-kidding-me", label: "Are you KIDDING me?", emoji: "🤬", group: "sass", board: 0 },
    { id: "excuse-me", label: "Excuse me?!", emoji: "💅", group: "sass", board: 0 },
    { id: "shut-up", label: "Shut up!", emoji: "🤐", group: "sass", board: 0 },
    { id: "leave-me-alone", label: "Leave me alone!", emoji: "🚪", group: "sass", board: 0 },
    { id: "get-out", label: "Get out!", emoji: "👉", group: "sass", board: 0 },
    { id: "stop-it", label: "Stop it!", emoji: "✋", group: "sass", board: 0 },

    // 🌙 Sleepy time
    { id: "time-for-bed", label: "Time for bed, you two!", emoji: "📣", group: "sleepy", board: 0 },
    { id: "good-night", label: "Have a good night!", emoji: "🌙", group: "sleepy", board: 0 },
    { id: "go-to-bed", label: "I have to go to bed", emoji: "🛏️", group: "sleepy", board: 0 },
    { id: "back-to-sleep", label: "I'm really really tired…", emoji: "😴", group: "sleepy", board: 0 },
    { id: "take-a-nap", label: "About to take a nap!", emoji: "💤", group: "sleepy", board: 0 },
    { id: "wake-up", label: "Hey, wake up!", emoji: "⏰", group: "sleepy", board: 0 },
    { id: "fell-asleep", label: "I almost fell asleep…", emoji: "🥱", group: "sleepy", board: 0 },
    { id: "right-to-sleep", label: "Fell right to sleep!", emoji: "👶", group: "sleepy", board: 0 },
    { id: "slumber-party", label: "Bestest slumber party EVER!", emoji: "🎉", group: "sleepy", board: 0 },
    { id: "first-sleepover", label: "My first sleepover!", emoji: "🏠", group: "sleepy", board: 0 },
    { id: "pajamas", label: "Still in my pajamas!", emoji: "🩳", group: "sleepy", board: 0 },

    // ═══ Board 1: 思思 (xiexie888888) ═══
    // ⚡ Signature moves
    { id: "zh-qu-xiang-zeng-xing", label: "去香增腥～", pinyin: "qù xiāng zēng xīng~", en: "Remove the flavour, add fishiness!", emoji: "🐟", group: "sisi-sig", board: 1 },
    { id: "zh-wo-shi-dijia", label: "嘿～我是迪迦！", pinyin: "hēi~ wǒ shì Díjiā!", en: "I am Ultraman Tiga!", emoji: "🦸", group: "sisi-sig", board: 1 },
    { id: "zh-hao-da-de-huo", label: "好大的火呀！", pinyin: "hǎo dà de huǒ ya!", en: "Wow, what a big fire!", emoji: "🔥", group: "sisi-sig", board: 1 },
    { id: "zh-full-intro", label: "Hey boy, thank you girl…", emoji: "🎤", group: "sisi-sig", en: "Her full signature intro", board: 1 },
    { id: "zh-hey-boy", label: "Hey boy, thank you girl!", emoji: "👋", group: "sisi-sig", en: "Signature opener", board: 1 },
    { id: "zh-listen-to-me", label: "Listen to me!", emoji: "👂", group: "sisi-sig", en: "Signature opener, pt. 2", board: 1 },
    { id: "zh-i-wanna-tell-you", label: "I wanna tell you…", emoji: "🗣️", group: "sisi-sig", en: "Signature opener, pt. 3", board: 1 },

    // 🐶 The dogs
    { id: "zh-kakashi", label: "卡卡西是我的孩子", pinyin: "Kǎkǎxī shì wǒ de háizi", en: "Kakashi is my child", emoji: "🐕", group: "sisi-dogs", board: 1 },
    { id: "zh-sun-wukong", label: "孙悟空，上！", pinyin: "Sūn Wùkōng, shàng!", en: "Sun Wukong, go!", emoji: "🐒", group: "sisi-dogs", board: 1 },
    { id: "zh-zhu-bajie", label: "猪八戒，握手！", pinyin: "Zhū Bājiè, wòshǒu!", en: "Zhu Bajie, shake!", emoji: "🐷", group: "sisi-dogs", board: 1 },
    { id: "zh-kashi-shang", label: "卡西，上！", pinyin: "Kǎxī, shàng!", en: "Kashi, go!", emoji: "🐾", group: "sisi-dogs", board: 1 },
    { id: "zh-kashi-zuo", label: "卡西，坐！", pinyin: "Kǎxī, zuò!", en: "Kashi, sit!", emoji: "🪑", group: "sisi-dogs", board: 1 },
    { id: "zh-kashi-woshou", label: "卡西，握手！", pinyin: "Kǎxī, wòshǒu!", en: "Kashi, shake!", emoji: "🤝", group: "sisi-dogs", board: 1 },
    { id: "zh-zhen-guai", label: "诶，真乖！", pinyin: "éi, zhēn guāi!", en: "Aww, good dog!", emoji: "🦴", group: "sisi-dogs", board: 1 },
    { id: "zh-guai-guai-guai", label: "乖乖乖！", pinyin: "guāi guāi guāi!", en: "Good, good, good boy!", emoji: "💕", group: "sisi-dogs", board: 1 },
    { id: "zh-kashi-zhenbang", label: "真棒，卡卡西！", pinyin: "zhēn bàng, Kǎkǎxī!", en: "Well done, Kakashi!", emoji: "🏅", group: "sisi-dogs", board: 1 },

    // 🥢 Kitchen & live
    { id: "zh-hao-xiang-ya", label: "好香呀", pinyin: "hǎo xiāng ya", en: "Smells SO good!", emoji: "🍜", group: "sisi-live", board: 1 },
    { id: "zh-gei-ni-chi", label: "给你吃个好东西", pinyin: "gěi nǐ chī ge hǎo dōngxi", en: "Here, try something good!", emoji: "🥢", group: "sisi-live", board: 1 },
    { id: "zh-wa-sai", label: "哇塞！", pinyin: "wāsài!", en: "Whoa!!", emoji: "🤩", group: "sisi-live", board: 1 },
    { id: "zh-chaoji-wudi", label: "超级无敌大的财神爷", pinyin: "chāojí wúdí dà de cáishényé", en: "A super-duper-HUGE God of Wealth!", emoji: "🧧", group: "sisi-live", board: 1 },
    { id: "zh-shide-shide", label: "对对对，是的是的", pinyin: "duì duì duì, shì de shì de", en: "Right right, yes yes!", emoji: "👌", group: "sisi-live", board: 1 },
    { id: "zh-kandaole-ma", label: "看到了吗？", pinyin: "kàndào le ma?", en: "Did you see that?", emoji: "🔍", group: "sisi-live", board: 1 },
    { id: "zh-duoshao-qian", label: "多少钱？", pinyin: "duōshao qián?", en: "How much?", emoji: "💰", group: "sisi-live", board: 1 },
    { id: "zh-gei-dajia-kan", label: "我给大家看一下", pinyin: "wǒ gěi dàjiā kàn yíxià", en: "Let me show you all!", emoji: "📸", group: "sisi-live", board: 1 },
    { id: "zh-xiexie-guanzhu", label: "谢谢关注", pinyin: "xièxie guānzhù", en: "Thanks for following!", emoji: "➕", group: "sisi-live", board: 1 },
    { id: "zh-xiexie-xiongdi", label: "谢谢兄弟们的关注", pinyin: "xièxie xiōngdìmen de guānzhù", en: "Thanks for the follow, bros!", emoji: "🤝", group: "sisi-live", board: 1 },
    { id: "zh-xiexie-dajia", label: "谢谢大家的喜欢", pinyin: "xièxie dàjiā de xǐhuan", en: "Thanks for all the love!", emoji: "💜", group: "sisi-live", board: 1 },

    // ═══ Board 2: Last Asylum: Plague (local-only assets — see scripts/extract_asylum_sfx.py) ═══
    { id: "game-battle-win", label: "Battle won!", emoji: "🏆", group: "asylum", board: 2, localOnly: true },
    { id: "game-battle-loss", label: "Battle lost…", emoji: "💀", group: "asylum", board: 2, localOnly: true },
    { id: "game-chest-open", label: "Chest open!", emoji: "📦", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-get-reward", label: "Reward!", emoji: "🎁", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-get-coin", label: "Coins!", emoji: "🪙", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-get-star", label: "Star get!", emoji: "⭐", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-level-up", label: "Level up!", emoji: "⬆️", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-hero-unlock", label: "Hero unlocked!", emoji: "🗝️", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-feature-unlock", label: "Feature unlocked!", emoji: "✨", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-build-finish", label: "Build complete!", emoji: "🏗️", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-click", label: "Click", emoji: "🔘", group: "asylum-sfx", board: 2, localOnly: true },
    { id: "game-map-unlock", label: "Map unlocked!", emoji: "🗺️", group: "asylum-sfx", board: 2, localOnly: true },

    // ═══ Board 3: Lore Accurate Ganondorf (Udge) — Latin Spanish dub + Suavemente ═══
    { id: "ganon-suavemente", label: "¡Suavemente!", en: "Softly! (Elvis Crespo)", emoji: "💃", group: "ganon-song", board: 3 },
    { id: "ganon-suavemente-besame", label: "Suavemente, bésame…", en: "Softly, kiss me…", emoji: "💋", group: "ganon-song", board: 3 },
    { id: "ganon-a-ver-si-te-gusta", label: "¡A ver si te gusta esto!", en: "Let's see if you like THIS!", emoji: "⚡", group: "ganon-lines", board: 3 },
    { id: "ganon-toma", label: "¡Toma!", en: "Take this!", emoji: "👊", group: "ganon-lines", board: 3 },
    { id: "ganon-ni-siquiera", label: "Ni siquiera he comenzado", en: "I haven't even begun", emoji: "😈", group: "ganon-lines", board: 3 },
    { id: "ganon-que-pasa", label: "¿Qué pasa?", en: "What's the matter?", emoji: "🤨", group: "ganon-lines", board: 3 },
    { id: "ganon-tienes-miedo", label: "¿Tienes miedo?", en: "Scared?", emoji: "😱", group: "ganon-lines", board: 3 },
  ];

  const grids = {
    whatthe: document.getElementById("grid-whatthe"),
    classics: document.getElementById("grid-classics"),
    sass: document.getElementById("grid-sass"),
    sleepy: document.getElementById("grid-sleepy"),
    "sisi-sig": document.getElementById("grid-sisi-sig"),
    "sisi-live": document.getElementById("grid-sisi-live"),
    "sisi-dogs": document.getElementById("grid-sisi-dogs"),
    asylum: document.getElementById("grid-asylum"),
    "asylum-sfx": document.getElementById("grid-asylum-sfx"),
    "ganon-song": document.getElementById("grid-ganon-song"),
    "ganon-lines": document.getElementById("grid-ganon-lines"),
  };
  const NUM_BOARDS = 4;

  let audioCtx = null;
  const buffers = new Map();   // id -> decoded AudioBuffer
  const pending = new Map();   // id -> in-flight decode promise
  const fallbackPool = new Map();

  function getContext() {
    if (!audioCtx) {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (Ctx) {
        try { audioCtx = new Ctx({ latencyHint: "interactive" }); }
        catch (err) { audioCtx = new Ctx(); }
      }
    }
    return audioCtx;
  }

  // Resolves once the context is actually running. Mobile browsers only let
  // this succeed from inside a user gesture, so it's kicked off synchronously
  // in the pointerdown/click handlers below.
  function resumeContext() {
    const ctx = getContext();
    if (!ctx) return Promise.resolve(null);
    if (ctx.state === "running" || typeof ctx.resume !== "function") return Promise.resolve(ctx);
    return ctx.resume().then(() => ctx, () => ctx);
  }

  // Unlock audio on the very first touch, before the click fires: resume the
  // context and (for iOS) start a silent source inside the gesture. By the
  // time the tap becomes a click the output clock is already running, so
  // the first real clip doesn't lose its opening samples.
  function unlock() {
    const ctx = getContext();
    if (!ctx || ctx.state === "running") return;
    resumeContext();
    try {
      const src = ctx.createBufferSource();
      src.buffer = ctx.createBuffer(1, 1, 22050);
      src.connect(ctx.destination);
      src.start(0);
    } catch (err) { /* ignore */ }
  }
  ["pointerdown", "touchstart", "keydown"].forEach((ev) =>
    window.addEventListener(ev, unlock, { capture: true, passive: true })
  );

  function loadBuffer(id) {
    if (buffers.has(id)) return Promise.resolve(buffers.get(id));
    if (pending.has(id)) return pending.get(id);
    const ctx = getContext();
    if (!ctx) return Promise.resolve(null);
    const p = fetch(`sounds/${id}.mp3`)
      .then((res) => (res.ok ? res.arrayBuffer() : Promise.reject(new Error(String(res.status)))))
      .then((data) => new Promise((resolve, reject) => {
        // Callback form for older Safari, which doesn't return a promise
        const ret = ctx.decodeAudioData(data, resolve, reject);
        if (ret && typeof ret.then === "function") ret.then(resolve, reject);
      }))
      .then((buf) => { buffers.set(id, buf); return buf; })
      .catch(() => null)
      .finally(() => pending.delete(id));
    pending.set(id, p);
    return p;
  }

  // Fetch + decode clips a few at a time so every button is ready before
  // it's pressed (decoding doesn't need a user gesture, only playback does).
  function preload(ids) {
    const queue = ids.slice();
    const next = () => {
      const id = queue.shift();
      if (id) loadBuffer(id).then(next, next);
    };
    for (let i = 0; i < 4; i++) next();
  }

  function playFallback(id, onEnd) {
    let el = fallbackPool.get(id);
    if (!el) {
      el = new Audio(`sounds/${id}.mp3`);
      el.preload = "auto";
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

    const wasRunning = !!audioCtx && audioCtx.state === "running";
    const ready = resumeContext();            // synchronously, inside the gesture
    const buf = await loadBuffer(id);
    const ctx = buf ? await ready : null;     // wait for the output clock to run
    if (buf && ctx && ctx.state === "running") {
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.connect(ctx.destination);
      src.onended = done;
      // If we only just resumed, give the hardware a moment to spin up so
      // the first samples aren't rendered into the void.
      src.start(wasRunning ? 0 : ctx.currentTime + 0.05);
      setTimeout(done, buf.duration * 1000 + 300);
    } else {
      playFallback(id, done);
    }
  }

  const allButtons = [];
  for (const sound of SOUNDS) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "sound-btn";
    let inner = `<span class="emoji" aria-hidden="true">${sound.emoji}</span><span class="label">${sound.label}</span>`;
    if (sound.pinyin) inner += `<span class="pinyin">${sound.pinyin}</span>`;
    if (sound.en) inner += `<span class="en">${sound.en}</span>`;
    btn.innerHTML = inner;
    btn.setAttribute("aria-label", `Play: ${sound.en || sound.label}`);
    btn.addEventListener("click", () => play(sound.id, btn));
    grids[sound.group].appendChild(btn);
    allButtons.push({ sound, btn });
  }

  // Local-only sounds (not distributed with the site): grey out any that
  // aren't present, and reveal the how-to note if some are missing.
  Promise.all(
    allButtons
      .filter((b) => b.sound.localOnly)
      .map(async (b) => {
        let ok = false;
        try {
          ok = (await fetch(`sounds/${b.sound.id}.mp3`, { method: "HEAD" })).ok;
        } catch (err) { /* leave missing */ }
        if (!ok) {
          b.missing = true;
          b.btn.classList.add("missing");
          b.btn.disabled = true;
          b.btn.insertAdjacentHTML("beforeend", `<span class="en">extract locally to enable</span>`);
        }
        return ok;
      })
  ).then((results) => {
    const note = document.getElementById("asylum-note");
    if (note && results.some((ok) => !ok)) note.hidden = false;
    preload(allButtons.filter((b) => b.sound.localOnly && !b.missing).map((b) => b.sound.id));
  });

  // ── Board switching: scroll-snap swiping + tabs kept in sync ──
  const boards = document.getElementById("boards");
  const tabs = [...document.querySelectorAll(".tab")];
  let activeBoard = 0;

  function setActiveTab(i) {
    activeBoard = i;
    tabs.forEach((t, j) => t.classList.toggle("active", j === i));
    document.body.classList.toggle("theme-sisi", i === 1);
    document.body.classList.toggle("theme-asylum", i === 2);
    document.body.classList.toggle("theme-ganon", i === 3);
  }

  tabs.forEach((tab) =>
    tab.addEventListener("click", () => {
      const i = Number(tab.dataset.board);
      boards.scrollTo({ left: i * boards.clientWidth, behavior: "smooth" });
      setActiveTab(i);
    })
  );

  let scrollTimer = null;
  boards.addEventListener("scroll", () => {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => {
      const i = Math.round(boards.scrollLeft / boards.clientWidth);
      if (i !== activeBoard) setActiveTab(Math.max(0, Math.min(NUM_BOARDS - 1, i)));
    }, 80);
  }, { passive: true });

  document.getElementById("random-btn").addEventListener("click", () => {
    const pool = allButtons.filter((b) => b.sound.board === activeBoard && !b.missing);
    if (!pool.length) return;
    const pick = pool[Math.floor(Math.random() * pool.length)];
    pick.btn.scrollIntoView({ block: "nearest", behavior: "smooth" });
    play(pick.sound.id, pick.btn);
  });

  // Decode every bundled clip up front (active board first) so the first
  // press plays instantly and in full.
  preload(
    allButtons
      .filter((b) => !b.sound.localOnly)
      .sort((a, b) => (a.sound.board === activeBoard ? 0 : 1) - (b.sound.board === activeBoard ? 0 : 1))
      .map((b) => b.sound.id)
  );
})();
