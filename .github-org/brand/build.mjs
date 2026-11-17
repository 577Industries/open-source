/**
 * 577 Industries brand-asset pipeline.
 *
 * Renders the org avatar, profile banners (dark/light), standalone wordmark
 * SVGs, and per-repo social-preview cards from the Steel design system
 * (palette chosen 2026-04-19; type: Instrument Serif / Inter Tight /
 * JetBrains Mono — all SIL OFL, vendored in ./fonts).
 *
 * Deterministic: same inputs → byte-identical outputs.
 *
 *   node build.mjs            # everything
 *   node build.mjs avatar     # one target: avatar | banner | wordmark | social
 *
 * Signature element: the calibration tick-scale — a hairline rule with
 * graduated ticks and one highlighted tolerance band. It encodes the
 * company's actual discipline (calibrated uncertainty, tolerance bounds)
 * and must appear on every asset.
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import satori from "satori";
import { Resvg } from "@resvg/resvg-js";

const ROOT = dirname(fileURLToPath(import.meta.url));
const OUT = join(ROOT, "out");

/* ── Steel palette ─────────────────────────────────────────────── */
const STEEL = {
  dark: {
    bg: "#06101c",
    bg2: "#0c1c30",
    surface: "#12233a",
    rule: "#24405f",
    ink: "#e8eef6",
    ink2: "#9fb3cb",
    signal: "#5eb5ff",
    amber: "#cd9265",
  },
  light: {
    bg: "#f2ede1",
    bg2: "#ece5d4",
    surface: "#e6decb",
    rule: "#c9bfa6",
    ink: "#1a2433",
    ink2: "#4a5a70",
    signal: "#1e3a8a",
    amber: "#8a5a2e",
  },
};

/* ── Fonts ─────────────────────────────────────────────────────── */
const font = (file) => readFileSync(join(ROOT, "fonts", file));
const FONTS = [
  { name: "Instrument Serif", data: font("InstrumentSerif-Regular.ttf"), weight: 400, style: "normal" },
  { name: "Instrument Serif", data: font("InstrumentSerif-Italic.ttf"), weight: 400, style: "italic" },
  { name: "Inter Tight", data: font("InterTight-Regular.ttf"), weight: 400, style: "normal" },
  { name: "Inter Tight", data: font("InterTight-Medium.ttf"), weight: 500, style: "normal" },
  { name: "Inter Tight", data: font("InterTight-SemiBold.ttf"), weight: 600, style: "normal" },
  { name: "JetBrains Mono", data: font("JetBrainsMono-Regular.ttf"), weight: 400, style: "normal" },
  { name: "JetBrains Mono", data: font("JetBrainsMono-Medium.ttf"), weight: 500, style: "normal" },
  { name: "JetBrainsMono Bold", data: font("JetBrainsMono-Bold.ttf"), weight: 700, style: "normal" },
];

/* ── Element helpers (satori takes React-shaped plain objects) ─── */
const el = (type, style, children = undefined, rest = {}) => ({
  type,
  props: { style, children, ...rest },
});
const div = (style, children) => el("div", { display: "flex", ...style }, children);
const text = (content, style) => el("div", { display: "flex", ...style }, content);

/* ── Signature: calibration tick-scale ─────────────────────────────
 * A hairline rule with graduated ticks; one interval is highlighted
 * as the "tolerance band". Heights alternate like a real scale.
 * width: total px · color: tick/rule color · band: [startTick, endTick]
 */
function tickScale({ width, ticks = 21, color, bandColor, band = [12, 15], ruleOpacity = 0.55, tickH = 12, majorEvery = 5 }) {
  const children = [];
  const step = width / (ticks - 1);
  // baseline rule
  children.push(div({ position: "absolute", left: 0, top: tickH, width, height: 1.5, backgroundColor: color, opacity: ruleOpacity }));
  // tolerance band segment (sits on the rule)
  children.push(
    div({
      position: "absolute",
      left: band[0] * step,
      top: tickH - 1.5,
      width: (band[1] - band[0]) * step,
      height: 4.5,
      backgroundColor: bandColor,
      borderRadius: 1,
    })
  );
  for (let i = 0; i < ticks; i++) {
    const major = i % majorEvery === 0;
    children.push(
      div({
        position: "absolute",
        left: i * step - 0.75,
        top: major ? 0 : tickH * 0.45,
        width: 1.5,
        height: major ? tickH : tickH * 0.55,
        backgroundColor: color,
        opacity: major ? 0.9 : 0.5,
      })
    );
  }
  return div({ position: "relative", width, height: tickH + 4 }, children);
}

/* ── Render plumbing ───────────────────────────────────────────── */
async function renderSvg(node, width, height) {
  return satori(node, { width, height, fonts: FONTS });
}
async function renderPng(node, width, height, scale = 1) {
  const svg = await renderSvg(node, width, height);
  const resvg = new Resvg(svg, { fitTo: { mode: "width", value: width * scale } });
  return resvg.render().asPng();
}
const save = (rel, buf) => {
  const p = join(OUT, rel);
  mkdirSync(dirname(p), { recursive: true });
  writeFileSync(p, buf);
  console.log("wrote", rel, `(${(buf.length / 1024).toFixed(1)} KB)`);
};

/* ── Avatar 512×512 — navy field, serif 577, tick-scale beneath ── */
function avatarNode() {
  const c = STEEL.dark;
  return div(
    {
      width: 512,
      height: 512,
      backgroundColor: c.bg,
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
    },
    [
      text("577", {
        fontFamily: "Instrument Serif",
        fontSize: 252,
        color: STEEL.light.bg, // cream digits — ties dark and light worlds
        lineHeight: 1,
        marginTop: -20,
      }),
      div({ marginTop: 34 }, [
        tickScale({ width: 300, ticks: 11, majorEvery: 5, color: c.ink2, bandColor: c.signal, band: [6, 8], tickH: 22 }),
      ]),
    ]
  );
}

/* ── Wordmark — 577 ‖ INDUSTRIES with tick-scale under the digits ─ */
function wordmarkNode(theme, { w = 1040, h = 220 } = {}) {
  const c = STEEL[theme];
  return div(
    { width: w, height: h, alignItems: "flex-start", justifyContent: "flex-start", backgroundColor: "transparent" },
    [
      div({ flexDirection: "column", marginLeft: 8 }, [
        text("577", { fontFamily: "Instrument Serif", fontSize: 148, color: c.ink, lineHeight: 1, letterSpacing: -2 }),
        div({ marginTop: 12 }, [
          tickScale({ width: 252, ticks: 11, majorEvery: 5, color: c.ink2, bandColor: c.signal, band: [6, 8], tickH: 14 }),
        ]),
      ]),
      div({ width: 2, height: 150, backgroundColor: c.rule, marginLeft: 44, marginTop: 10 }),
      div({ flexDirection: "column", marginLeft: 44, marginTop: 22 }, [
        text("INDUSTRIES", { fontFamily: "JetBrains Mono", fontWeight: 500, fontSize: 58, letterSpacing: 22, color: c.ink }),
        text("CALIBRATED SYSTEMS · DUAL-USE R&D", {
          fontFamily: "JetBrains Mono",
          fontSize: 21,
          letterSpacing: 6.5,
          color: c.ink2,
          marginTop: 26,
        }),
      ]),
    ]
  );
}

/* ── Banner 1600×400 ───────────────────────────────────────────── */
function bannerNode(theme) {
  const c = STEEL[theme];
  const gradient =
    theme === "dark"
      ? { backgroundImage: `linear-gradient(105deg, ${c.bg} 0%, ${c.bg} 55%, ${c.bg2} 100%)` }
      : { backgroundColor: c.bg };
  return div(
    { width: 1600, height: 400, flexDirection: "column", position: "relative", ...gradient },
    [
      // hairline frame rules
      div({ position: "absolute", left: 0, top: 0, width: 1600, height: 2, backgroundColor: c.rule }),
      div({ position: "absolute", left: 0, top: 398, width: 1600, height: 2, backgroundColor: c.rule }),
      // right-side extended calibration scale, quiet
      div({ position: "absolute", right: 72, top: 182 }, [
        tickScale({ width: 420, ticks: 21, majorEvery: 5, color: c.ink2, bandColor: c.signal, band: [13, 16], tickH: 16 }),
      ]),
      text("§ 577INDUSTRIES.COM", {
        position: "absolute",
        right: 72,
        top: 220,
        fontFamily: "JetBrains Mono",
        fontSize: 17,
        letterSpacing: 5,
        color: c.ink2,
      }),
      // main block
      div({ flexDirection: "column", marginLeft: 72, marginTop: 64 }, [
        text("AI SYSTEMS INTEGRATOR · COLUMBUS, OHIO", {
          fontFamily: "JetBrains Mono",
          fontSize: 19,
          letterSpacing: 6,
          color: c.signal,
        }),
        div({ alignItems: "baseline", marginTop: 18 }, [
          text("577", { fontFamily: "Instrument Serif", fontSize: 128, color: c.ink, lineHeight: 1, letterSpacing: -2 }),
          text("Industries", {
            fontFamily: "Instrument Serif",
            fontStyle: "italic",
            fontSize: 104,
            color: c.ink,
            lineHeight: 1,
            marginLeft: 30,
          }),
        ]),
        text("Engineering for missions where failure is not an option.", {
          fontFamily: "Inter Tight",
          fontWeight: 500,
          fontSize: 34,
          color: c.ink2,
          marginTop: 22,
        }),
      ]),
    ]
  );
}

/* ── Social preview 1280×640 (per repo) ────────────────────────── */
function socialNode({ repo, program, blurb }) {
  const c = STEEL.dark;
  return div(
    { width: 1280, height: 640, flexDirection: "column", position: "relative", backgroundColor: c.bg },
    [
      div({ position: "absolute", left: 0, top: 0, width: 1280, height: 3, backgroundColor: c.signal, opacity: 0.9 }),
      div({ flexDirection: "column", marginLeft: 84, marginTop: 84, width: 1100 }, [
        text(`577i · ${program.toUpperCase()}`, {
          fontFamily: "JetBrains Mono",
          fontSize: 24,
          letterSpacing: 7,
          color: c.signal,
        }),
        text(repo, {
          fontFamily: "JetBrains Mono",
          fontWeight: 500,
          fontSize: repo.length > 26 ? 62 : 76,
          color: c.ink,
          marginTop: 30,
          letterSpacing: -1,
        }),
        text(blurb, {
          fontFamily: "Inter Tight",
          fontSize: 33,
          color: c.ink2,
          marginTop: 26,
          lineHeight: 1.35,
          maxWidth: 1080,
        }),
      ]),
      // footer: tick-scale + wordmark line
      div({ position: "absolute", left: 84, top: 528 }, [
        tickScale({ width: 300, ticks: 11, majorEvery: 5, color: c.ink2, bandColor: c.signal, band: [6, 8], tickH: 14 }),
      ]),
      div({ position: "absolute", right: 84, top: 520, alignItems: "baseline" }, [
        text("577", { fontFamily: "Instrument Serif", fontSize: 46, color: c.ink }),
        text("INDUSTRIES", { fontFamily: "JetBrains Mono", fontSize: 22, letterSpacing: 7, color: c.ink, marginLeft: 14 }),
        text("· 577industries.com", { fontFamily: "Inter Tight", fontSize: 22, color: c.ink2, marginLeft: 14 }),
      ]),
    ]
  );
}

/* ── Repo manifest for social cards ────────────────────────────── */
const REPOS = JSON.parse(readFileSync(join(ROOT, "repos.json"), "utf8"));

/* ── Targets ───────────────────────────────────────────────────── */
const targets = {
  async avatar() {
    save("avatar.png", await renderPng(avatarNode(), 512, 512));
    save("preview/avatar-32.png", await renderPng(avatarNode(), 512, 512, 32 / 512));
    save("preview/avatar-20.png", await renderPng(avatarNode(), 512, 512, 20 / 512));
  },
  async banner() {
    save("banner-dark.png", await renderPng(bannerNode("dark"), 1600, 400));
    save("banner-light.png", await renderPng(bannerNode("light"), 1600, 400));
  },
  async wordmark() {
    save("wordmark-dark.svg", Buffer.from(await renderSvg(wordmarkNode("dark"), 1040, 220)));
    save("wordmark-light.svg", Buffer.from(await renderSvg(wordmarkNode("light"), 1040, 220)));
    save("preview/wordmark-dark.png", await renderPng(wordmarkNode("dark"), 1040, 220));
    save("preview/wordmark-light.png", await renderPng(wordmarkNode("light"), 1040, 220));
  },
  async social() {
    for (const r of REPOS) save(`social/${r.repo}.png`, await renderPng(socialNode(r), 1280, 640));
  },
};

const pick = process.argv[2];
const run = pick ? { [pick]: targets[pick] } : targets;
if (pick && !targets[pick]) {
  console.error(`unknown target "${pick}" — use: ${Object.keys(targets).join(" | ")}`);
  process.exit(1);
}
for (const [name, fn] of Object.entries(run)) {
  console.log(`── ${name}`);
  await fn();
}
