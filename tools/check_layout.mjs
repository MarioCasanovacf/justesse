#!/usr/bin/env node
// Measure a presentation-safe HTML deck against the one thing its author cannot check by reading
// it: what the text actually does once a font measures it.
//
//     node tools/check_layout.mjs deck.html
//     node tools/check_layout.mjs deck.html --max-void 80
//
// The subset in skill/justesse/references/pptx-safe-html.md fixes every box at authoring time, but
// a box's declared height is a prediction. Type is measured by the font, so a title expected to fit
// on one line wraps to two, overflows its box, and lands on the paragraph below it. That collision
// is in the presentation file as much as in the browser, because a text box overflows rather than
// shrinks to fit, and it survives review easily: it is invisible in the source, and a reviewer who
// checks the first slide never sees it.
//
// Three failures are reported, all of them measured rather than judged:
//
//   overflow    text taller than the box its author declared
//   collision   two text objects overlapping once wrapped
//   escape      an object outside the 1280x720 canvas, which is off the slide
//
// Shapes may overlap anything, and text may sit on a shape: a label inside a bar and a bar crossing
// its axis are composition, not defects. Only text against text is a collision.
//
// `--max-void N` additionally reports the largest empty horizontal band in each slide's live area
// when it exceeds N px. That one is off by default and opt-in by threshold, because how much space
// a surface should carry is a judgment an identity declares, not a constant this tool knows.
//
// Requires the `playwright` package plus an installed Chrome or Chromium, like inspect_html.mjs.
// Browser measurement is runner-provided evidence: any runner reporting the same findings satisfies
// the contract.

import { pathToFileURL } from "node:url";
import path from "node:path";
import { createRequire } from "node:module";

const CANVAS_WIDTH = 1280;
const CANVAS_HEIGHT = 720;

function resolvePlaywright() {
  for (const base of [path.join(process.cwd(), "noop.js"), import.meta.url]) {
    try {
      return createRequire(base)("playwright");
    } catch {
      continue;
    }
  }
  return null;
}

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(2);
}

async function launch(playwright) {
  for (const options of [{ channel: "chrome" }, {}]) {
    try {
      return await playwright.chromium.launch({ headless: true, ...options });
    } catch {
      continue;
    }
  }
  fail("no Chrome or Chromium available to playwright");
}

// Runs inside the page. Declared geometry comes from the inline style, because that is what the
// converter reads; painted extent comes from layout, because that is what the reader sees.
function measure({ canvasWidth, canvasHeight }) {
  const findings = [];
  const voids = [];
  const slides = [...document.querySelectorAll(".slide")];
  if (!slides.length) return { findings: [{ kind: "structure", detail: "no .slide element found" }], voids };

  for (const [index, slide] of slides.entries()) {
    const name = slide.dataset.name || `slide-${index + 1}`;
    const objects = [...slide.querySelectorAll(".text, .rect, .ellipse, .line")].map((el) => {
      const isText = el.classList.contains("text");
      const left = parseFloat(el.style.left);
      const top = parseFloat(el.style.top);
      const width = parseFloat(el.style.width);
      const declared = parseFloat(el.style.height);
      // A text box is as tall as its wrapped content; a shape is as tall as it was declared.
      const painted = isText ? el.scrollHeight : declared;
      return {
        name: el.dataset.name || el.className,
        isText,
        left,
        top,
        width,
        declared,
        painted,
        right: left + width,
        bottom: top + painted,
      };
    });

    for (const object of objects) {
      if (object.isText && object.painted > object.declared + 1) {
        findings.push({
          kind: "overflow",
          slide: name,
          object: object.name,
          detail: `text is ${Math.round(object.painted)}px tall in a ${object.declared}px box (over by ${Math.round(object.painted - object.declared)}px)`,
        });
      }
      if (
        object.left < 0 ||
        object.top < 0 ||
        object.right > canvasWidth ||
        object.top + object.declared > canvasHeight
      ) {
        findings.push({
          kind: "escape",
          slide: name,
          object: object.name,
          detail: `box [${object.left}, ${object.top}, ${object.width}, ${object.declared}] leaves the ${canvasWidth}x${canvasHeight} canvas`,
        });
      }
    }

    const texts = objects.filter((object) => object.isText);
    for (let i = 0; i < texts.length; i += 1) {
      for (let j = i + 1; j < texts.length; j += 1) {
        const a = texts[i];
        const b = texts[j];
        if (a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom) {
          findings.push({
            kind: "collision",
            slide: name,
            object: `${a.name} x ${b.name}`,
            detail: "two text objects overlap once wrapped",
          });
        }
      }
    }

    // Largest empty horizontal band in the live area, ignoring the running header and footer,
    // which are furniture rather than composition.
    const furniture = /^(stage|deck|folio|source|rule-top|rule-foot)/;
    const spans = objects
      .filter((object) => !furniture.test(object.name))
      .map((object) => [object.top, object.bottom])
      .sort((a, b) => a[0] - b[0]);
    if (spans.length) {
      const first = Math.min(...objects.filter((o) => /^rule-top/.test(o.name)).map((o) => o.bottom), 74);
      const last = Math.max(...objects.filter((o) => /^rule-foot/.test(o.name)).map((o) => o.top), 0) || canvasHeight;
      let cursor = first;
      let largest = 0;
      for (const [top, bottom] of spans) {
        if (top - cursor > largest) largest = top - cursor;
        cursor = Math.max(cursor, bottom);
      }
      if (last - cursor > largest) largest = last - cursor;
      voids.push({ slide: name, largest: Math.round(largest) });
    }
  }
  return { findings, voids };
}

const args = process.argv.slice(2);
const voidFlag = args.findIndex((a) => a === "--max-void" || a.startsWith("--max-void="));
let maxVoid = null;
const consumed = new Set();
if (voidFlag !== -1) {
  const inline = args[voidFlag].includes("=");
  const raw = inline ? args[voidFlag].split("=")[1] : args[voidFlag + 1];
  maxVoid = Number(raw);
  if (!Number.isFinite(maxVoid)) fail(`--max-void needs a number, got ${raw}`);
  consumed.add(voidFlag);
  if (!inline) consumed.add(voidFlag + 1);
}
const files = args.filter((a, index) => !a.startsWith("--") && !consumed.has(index));
if (files.length !== 1) {
  console.error("usage: node tools/check_layout.mjs deck.html [--max-void N]");
  process.exit(2);
}

const playwright = resolvePlaywright();
if (!playwright) {
  fail("the playwright package is not resolvable from the current directory; npm install playwright");
}

const browser = await launch(playwright);
const page = await browser.newPage({ viewport: { width: CANVAS_WIDTH + 48, height: 900 } });
await page.goto(pathToFileURL(path.resolve(files[0])).href, { waitUntil: "networkidle" });
const { findings, voids } = await page.evaluate(measure, { canvasWidth: CANVAS_WIDTH, canvasHeight: CANVAS_HEIGHT });
await browser.close();

const over = maxVoid === null ? [] : voids.filter((entry) => entry.largest > maxVoid);
for (const finding of findings) {
  console.log(`[${finding.kind}] ${finding.slide ?? ""} ${finding.object ?? ""}: ${finding.detail}`);
}
for (const entry of over) {
  console.log(`[void] ${entry.slide}: largest empty band is ${entry.largest}px, over the declared ${maxVoid}px`);
}

if (maxVoid !== null && !over.length) {
  const worst = voids.reduce((a, b) => (b.largest > a.largest ? b : a), { largest: 0, slide: "-" });
  console.error(`largest empty band ${worst.largest}px on ${worst.slide}, within the declared ${maxVoid}px`);
}
if (!findings.length && !over.length) {
  console.log(`PASS: every text box contains its text, no two collide, nothing leaves the canvas`);
  process.exit(0);
}
console.log(`\nFAIL: ${findings.length + over.length} finding(s). These are in the presentation file too, not only the preview.`);
process.exit(1);
