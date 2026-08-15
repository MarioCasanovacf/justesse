#!/usr/bin/env node
// Emit the object inventory of a rendered HTML surface as NDJSON, one record per visual atom,
// in the same record shape tools/inspect_pptx.py emits for decks — so tools/diff_specimens.py
// consumes either without knowing which medium produced it.
//
//     node tools/inspect_html.mjs page.html > page.inspect.ndjson
//     node tools/inspect_html.mjs page.html --viewports 1440x1000,390x844
//
// Each requested viewport becomes one "slide" (slide 1 is the first viewport), because a
// responsive surface at two widths is two compositions of one design, exactly as a deck's slides
// are. Records carry kind (textbox for text-bearing atoms, shape for painted boxes, picture for
// raster images), bbox in CSS px, color (text color for textboxes, paint for shapes), type size
// and family, and the text content.
//
// Requires the `playwright` package plus an installed Chrome or Chromium; this repository does
// not vendor either. Like the render and QA commands, browser capture is runner-provided
// evidence: any runner that produces the same record shape satisfies the contract.

import { pathToFileURL } from "node:url";
import path from "node:path";
import { createRequire } from "node:module";

// Resolve playwright from the invoking project first (its node_modules), then from
// wherever this tool itself lives; the repository vendors neither.
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
    } catch (error) {
      continue;
    }
  }
  fail("no Chrome or Chromium available to playwright");
}

// Runs inside the page: walk the DOM in document order and emit visual atoms.
function collectAtoms() {
  const atoms = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  const skip = new Set(["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE", "META", "LINK"]);
  for (let el = walker.currentNode; el; el = walker.nextNode()) {
    if (skip.has(el.tagName)) continue;
    const style = getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") continue;
    const rect = el.getBoundingClientRect();
    if (rect.width < 1 || rect.height < 1) continue;
    const directText = Array.from(el.childNodes)
      .filter((node) => node.nodeType === Node.TEXT_NODE)
      .map((node) => node.textContent)
      .join("")
      .replace(/\s+/g, " ")
      .trim();
    const bg = style.backgroundColor;
    const paintedBg = bg && !bg.startsWith("rgba(0, 0, 0, 0)") && bg !== "transparent";
    const borderW = parseFloat(style.borderTopWidth) || 0;
    const painted = paintedBg || (borderW > 0 && style.borderTopStyle !== "none");
    const isImage = el.tagName === "IMG" || el.tagName === "CANVAS";
    const isSvg = el.tagName === "svg";
    if (!directText && !painted && !isImage && !isSvg) continue;
    const bbox = [
      Math.round(rect.left + window.scrollX),
      Math.round(rect.top + window.scrollY),
      Math.round(rect.width),
      Math.round(rect.height),
    ];
    const name =
      el.getAttribute("data-name") ||
      (el.id ? `#${el.id}` : `${el.tagName.toLowerCase()}${el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/)[0] : ""}`);
    if (isImage) {
      atoms.push({ kind: "picture", name, bbox, rasterized: true });
      continue;
    }
    const record = { kind: directText ? "textbox" : "shape", name, bbox };
    if (isSvg) record.kind = "shape", (record.geometry = "svg");
    const toHex = (rgb) => {
      const match = rgb.match(/\d+(\.\d+)?/g);
      if (!match) return null;
      const [r, g, b] = match.map((v) => Math.round(parseFloat(v)));
      return (
        "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("").toUpperCase()
      );
    };
    if (directText) {
      record.text = directText;
      record.textChars = directText.length;
      record.color = toHex(style.color);
      record.fontSizePx = Math.round(parseFloat(style.fontSize) * 10) / 10;
      record.fontFamily = style.fontFamily.split(",")[0].trim().replace(/["']/g, "");
    } else if (paintedBg) {
      record.color = toHex(bg);
    } else {
      record.color = toHex(style.borderTopColor);
    }
    atoms.push(record);
  }
  const bodyBg = getComputedStyle(document.body).backgroundColor;
  const rootBg = getComputedStyle(document.documentElement).backgroundColor;
  const pick = bodyBg && !bodyBg.startsWith("rgba(0, 0, 0, 0)") ? bodyBg : rootBg;
  const match = pick && pick.match(/\d+(\.\d+)?/g);
  const background = match
    ? "#" +
      match.slice(0, 3).map((v) => Math.round(parseFloat(v)).toString(16).padStart(2, "0")).join("").toUpperCase()
    : null;
  return { atoms, background };
}

const args = process.argv.slice(2);
// A flag's value does not start with `--`, so it has to be consumed by index rather than filtered
// out by shape; otherwise `--viewports 1440x1000` reads as a second input file.
const viewportIndex = args.findIndex((a) => a === "--viewports" || a.startsWith("--viewports="));
const consumed = new Set();
let viewportSpec = "1440x1000,390x844";
if (viewportIndex !== -1) {
  const inline = args[viewportIndex].includes("=");
  viewportSpec = inline ? args[viewportIndex].split("=")[1] : args[viewportIndex + 1];
  consumed.add(viewportIndex);
  if (!inline) consumed.add(viewportIndex + 1);
}
const files = args.filter((a, index) => !a.startsWith("--") && !consumed.has(index));
if (files.length !== 1 || !viewportSpec) {
  console.error("usage: node tools/inspect_html.mjs page.html [--viewports WxH,WxH]");
  process.exit(2);
}
const viewports = viewportSpec.split(",").map((pair) => {
  const [width, height] = pair.trim().split("x").map(Number);
  if (!width || !height) fail(`bad viewport ${pair}`);
  return { width, height };
});

const playwright = resolvePlaywright();
if (!playwright) {
  fail("the playwright package is not resolvable from the current directory; npm install playwright");
}

const browser = await launch(playwright);
const records = [{ kind: "deck", name: path.basename(files[0]), slides: viewports.length }];
for (const [index, viewport] of viewports.entries()) {
  const page = await browser.newPage({ viewport });
  await page.goto(pathToFileURL(path.resolve(files[0])).href, { waitUntil: "networkidle" });
  const { atoms, background } = await page.evaluate(collectAtoms);
  const slide = { kind: "slide", slide: index + 1, objects: atoms.length };
  if (background) slide.background = background;
  slide.viewport = `${viewport.width}x${viewport.height}`;
  records.push(slide);
  for (const atom of atoms) records.push({ slide: index + 1, ...atom });
  await page.close();
}
await browser.close();

for (const record of records) console.log(JSON.stringify(record));
const rasterized = records.filter((r) => r.rasterized).length;
const editable = records.filter((r) => ["textbox", "shape"].includes(r.kind)).length;
console.error(`${editable} visual atoms, ${rasterized} raster image(s), ${viewports.length} viewport(s)`);
