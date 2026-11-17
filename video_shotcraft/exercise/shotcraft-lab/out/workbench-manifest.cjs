"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/workbench.ts
var workbench_exports = {};
__export(workbench_exports, {
  WORKBENCH: () => WORKBENCH
});
module.exports = __toCommonJS(workbench_exports);

// src/Main.tsx
var import_remotion = require("remotion");

// src/timeline.ts
var SHOTS = {
  hero: { from: 0, duration: 90 },
  features: { from: 90, duration: 90 }
};
var TOTAL = SHOTS.hero.duration + SHOTS.features.duration;
var FLASH_CUTS = [SHOTS.features.from];
var CAPTIONS = [
  { from: SHOTS.features.from + 18, duration: 48, text: "ONE TIMELINE \xB7 EVERY BEAT EDITABLE" }
];
var PEAK_F = {
  "whoosh-fast.mp3": 21.75,
  "impact-cine.mp3": 16.65,
  "transition-soft.mp3": 13.65
};
var OUTPUT_AUDIO_OFFSET_F = 0;
var sfxFrom = (targetPeakF, src) => Math.max(0, Math.round(targetPeakF - (PEAK_F[src] ?? 0) - OUTPUT_AUDIO_OFFSET_F));
var SFX = [
  { target: SHOTS.hero.from + 36, src: "whoosh-fast.mp3", volume: 0.45, action: "hero card lift" },
  { target: SHOTS.hero.from + 70, src: "impact-cine.mp3", volume: 0.5, action: "hero card reseat" },
  { target: SHOTS.features.from + 24, src: "transition-soft.mp3", volume: 0.4, action: "feature rows land" }
].map((s) => ({ ...s, from: sfxFrom(s.target, s.src), duration: 90 }));

// src/Main.tsx
var import_jsx_runtime = require("react/jsx-runtime");
var clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };
var HERO_DEFAULTS = {
  product: "NOVA Focus",
  kicker: "A CALMER WORKSPACE",
  accent: "#ffb703",
  fontSize: 42
};
var FEATURE_DEFAULTS = {
  title: "Everything lands\nright on beat.",
  items: "Capture the real product\nPin motion to frames\nEdit every layer",
  accent: "#ff4d8d",
  fontSize: 46,
  duration: 90
};
var CAPTION_DEFAULTS = {
  text: "",
  color: "#ffffff",
  accent: "#ffb703",
  fontSize: 18,
  duration: 48
};
var ProductCard = ({
  product,
  kicker,
  accent,
  fontSize
}) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { style: {
  width: 560,
  borderRadius: 28,
  padding: 34,
  color: "#17213b",
  background: "linear-gradient(145deg, #ffffff, #e8f2ff)",
  border: "2px solid rgba(255,255,255,0.8)",
  boxShadow: "0 35px 100px rgba(0,0,0,0.45)",
  fontFamily: "Arial, sans-serif"
}, children: [
  /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between" }, children: [
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { fontSize: 15, fontWeight: 800, letterSpacing: 3, color: "#53627d" }, children: kicker }),
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { width: 18, height: 18, borderRadius: 18, background: accent, boxShadow: `0 0 30px ${accent}` } })
  ] }),
  /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { marginTop: 28, fontSize, lineHeight: 1.05, fontWeight: 900 }, children: product }),
  /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { style: { marginTop: 28, display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 16 }, children: [
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { height: 122, borderRadius: 18, background: "#17213b", padding: 18, boxSizing: "border-box" }, children: [0.82, 0.56, 0.7].map((w, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { width: `${w * 100}%`, height: 10, marginBottom: 15, borderRadius: 8, background: i === 0 ? accent : "#7e8daa" } }, i)) }),
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { height: 122, borderRadius: 18, background: accent, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 42, fontWeight: 900 }, children: "03" })
  ] })
] });
var HeroShot = (props) => {
  const p = { ...HERO_DEFAULTS, ...props };
  const frame = (0, import_remotion.useCurrentFrame)();
  const enter = (0, import_remotion.interpolate)(frame, [0, 24], [0, 1], { ...clamp, easing: import_remotion.Easing.bezier(0.16, 1, 0.3, 1) });
  const lift = (0, import_remotion.interpolate)(frame, [30, 44, 58, 70], [0, 1, 1, 0], { ...clamp, easing: import_remotion.Easing.inOut(import_remotion.Easing.ease) });
  const spotX = (0, import_remotion.interpolate)(frame, [0, 20, 34], [22, 72, 50], { ...clamp, easing: import_remotion.Easing.inOut(import_remotion.Easing.ease) });
  const scale = (0.78 + enter * 0.22) * (1 + lift * 0.055);
  return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_remotion.AbsoluteFill, { style: { background: "#090d1c", overflow: "hidden", fontFamily: "Arial, sans-serif" }, children: [
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.AbsoluteFill, { style: {
      background: `radial-gradient(circle at ${spotX}% 44%, ${p.accent}55 0%, #354aa766 22%, transparent 58%)`,
      opacity: 0.45 + enter * 0.55
    } }),
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: {
      position: "absolute",
      left: 200,
      top: 105,
      transform: `translateY(${70 * (1 - enter) - 26 * lift}px) scale(${scale}) rotateY(${-10 * lift}deg)`,
      transformOrigin: "center center"
    }, children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ProductCard, { ...p }) }),
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { position: "absolute", left: 62, bottom: 45, color: "#fff", fontSize: 16, letterSpacing: 4, fontWeight: 700, opacity: enter }, children: "SPOTLIGHT \u2192 LIFT \u2192 RESEAT" })
  ] });
};
var FeatureShot = (props) => {
  const p = { ...FEATURE_DEFAULTS, ...props };
  const frame = (0, import_remotion.useCurrentFrame)();
  const exit = (0, import_remotion.interpolate)(frame, [p.duration - 8, p.duration], [1, 0], clamp);
  return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_remotion.AbsoluteFill, { style: { background: "linear-gradient(135deg, #27104f, #071a38)", color: "#fff", fontFamily: "Arial, sans-serif", opacity: exit }, children: [
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { position: "absolute", width: 520, height: 520, right: -170, top: -190, borderRadius: 520, background: p.accent, opacity: 0.28, filter: "blur(20px)" } }),
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { position: "absolute", left: 66, top: 60, whiteSpace: "pre-line", fontSize: p.fontSize, lineHeight: 1.08, fontWeight: 900 }, children: p.title }),
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { style: { position: "absolute", left: 68, top: 230, width: 825 }, children: p.items.split("\n").map((item, i) => {
      const on = (0, import_remotion.interpolate)(frame, [12 + i * 12, 28 + i * 12], [0, 1], { ...clamp, easing: import_remotion.Easing.bezier(0.16, 1, 0.3, 1) });
      return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { style: {
        display: "flex",
        alignItems: "center",
        gap: 20,
        marginBottom: 15,
        padding: "16px 22px",
        borderRadius: 16,
        background: "rgba(255,255,255,0.1)",
        border: "1px solid rgba(255,255,255,0.18)",
        fontSize: 23,
        fontWeight: 700,
        opacity: on,
        transform: `translateX(${90 * (1 - on)}px)`
      }, children: [
        /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { style: { color: p.accent, fontSize: 28 }, children: [
          "0",
          i + 1
        ] }),
        item
      ] }, item);
    }) })
  ] });
};
var FlashCut = ({ duration = 10 }) => {
  const frame = (0, import_remotion.useCurrentFrame)();
  const opacity = (0, import_remotion.interpolate)(frame, [0, duration * 0.4, duration], [0, 0.85, 0], clamp);
  return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.AbsoluteFill, { style: { pointerEvents: "none", opacity, background: "radial-gradient(ellipse at 50% 45%, rgba(255,248,235,0.98), rgba(255,244,224,0.55) 55%, transparent 80%)" } });
};
var Caption = (props) => {
  const p = { ...CAPTION_DEFAULTS, ...props };
  const frame = (0, import_remotion.useCurrentFrame)();
  const opacity = (0, import_remotion.interpolate)(frame, [0, 7, p.duration - 7, p.duration], [0, 1, 1, 0], clamp);
  return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.AbsoluteFill, { style: { pointerEvents: "none", opacity }, children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { style: { position: "absolute", bottom: 28, left: 70, right: 70, color: p.color, fontFamily: "Arial, sans-serif", fontSize: p.fontSize, fontWeight: 800, letterSpacing: 2, textAlign: "center" }, children: [
    /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { style: { color: p.accent }, children: "\u25A0" }),
    " ",
    p.text
  ] }) });
};
var Main = () => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_remotion.AbsoluteFill, { style: { backgroundColor: "#090d1c" }, children: [
  SFX.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.Sequence, { from: s.from, durationInFrames: s.duration, children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.Audio, { src: (0, import_remotion.staticFile)(`audio/${s.src}`), volume: s.volume }) }, s.src)),
  /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.Sequence, { from: SHOTS.hero.from, durationInFrames: SHOTS.hero.duration, children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(HeroShot, {}) }),
  /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.Sequence, { from: SHOTS.features.from, durationInFrames: SHOTS.features.duration, children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(FeatureShot, {}) }),
  CAPTIONS.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.Sequence, { from: c.from, durationInFrames: c.duration, children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Caption, { ...c }) }, c.from)),
  FLASH_CUTS.map((cut) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_remotion.Sequence, { from: cut - 5, durationInFrames: 10, children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(FlashCut, { duration: 10 }) }, cut))
] });

// src/workbench.ts
var text = (key, label, def) => ({ type: "text", key, label, default: def });
var textarea = (key, label, def) => ({ type: "textarea", key, label, default: def });
var color = (key, label, def) => ({ type: "color", key, label, default: def });
var size = (key, label, def) => ({ type: "slider", key, label, default: def, min: 14, max: 80, step: 1, unit: "px" });
var WORKBENCH = {
  name: "Shotcraft learning lab",
  fps: 30,
  width: 960,
  height: 540,
  total: TOTAL,
  background: "#090d1c",
  shots: [
    {
      id: "hero",
      label: "S1 \u5355\u4E3B\u89D2\u4EA7\u54C1\u955C\u5934",
      from: SHOTS.hero.from,
      duration: SHOTS.hero.duration,
      component: HeroShot,
      props: { ...HERO_DEFAULTS },
      schema: [text("product", "\u4EA7\u54C1\u540D", HERO_DEFAULTS.product), text("kicker", "\u7709\u9898", HERO_DEFAULTS.kicker), color("accent", "\u5F3A\u8C03\u8272", HERO_DEFAULTS.accent), size("fontSize", "\u4EA7\u54C1\u540D\u5B57\u53F7", HERO_DEFAULTS.fontSize)]
    },
    {
      id: "features",
      label: "S2 \u529F\u80FD\u843D\u70B9",
      from: SHOTS.features.from,
      duration: SHOTS.features.duration,
      component: FeatureShot,
      props: { ...FEATURE_DEFAULTS },
      durationProp: "duration",
      schema: [textarea("title", "\u6807\u9898", FEATURE_DEFAULTS.title), textarea("items", "\u529F\u80FD\uFF08\u6BCF\u884C\u4E00\u6761\uFF09", FEATURE_DEFAULTS.items), color("accent", "\u5F3A\u8C03\u8272", FEATURE_DEFAULTS.accent), size("fontSize", "\u6807\u9898\u5B57\u53F7", FEATURE_DEFAULTS.fontSize)]
    }
  ],
  transitions: FLASH_CUTS.map((cut, i) => ({
    id: `flash-${i}`,
    label: "\u8DE8\u5207\u70B9\u6696\u767D\u95EA",
    from: cut - 5,
    duration: 10,
    component: FlashCut,
    durationProp: "duration",
    cardId: "flash-cut",
    cardName: "\u6696\u767D\u95EA\u8F6C\u573A"
  })),
  captions: CAPTIONS.map((c, i) => ({
    id: `caption-${i}`,
    label: c.text,
    from: c.from,
    duration: c.duration,
    component: Caption,
    props: { ...CAPTION_DEFAULTS, ...c },
    durationProp: "duration",
    schema: [text("text", "\u5B57\u5E55", c.text), color("color", "\u6587\u5B57\u8272", CAPTION_DEFAULTS.color), color("accent", "\u65B9\u70B9\u8272", CAPTION_DEFAULTS.accent), size("fontSize", "\u5B57\u53F7", CAPTION_DEFAULTS.fontSize)],
    cardId: "caption",
    cardName: "\u89E3\u8BF4\u5B57\u5E55\u6761"
  })),
  sfx: SFX.map((s) => ({ from: s.from, duration: s.duration, src: `audio/${s.src}`, volume: s.volume })),
  order: ["transitions", "captions", "overlays"],
  original: Main
};
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  WORKBENCH
});
