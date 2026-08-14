#!/usr/bin/env python3
"""Convert presentation-safe HTML into a PPTX whose every element is a native, editable object.

This is the reference implementation of the authoring subset defined in
`skill/justesse/references/pptx-safe-html.md`. It uses only the Python standard library, so a deck
rebuild costs nothing but a process start: author the HTML once, then iterate by re-running this.

    python3 tools/html2deck.py deck.html deck.pptx

Input is one `.slide` element per slide on a fixed 1280x720 px canvas, holding elements classed
`text`, `rect`, `ellipse`, or `line`, each with absolute `left`, `top`, `width`, and `height` in an
inline style. Output is a presentation whose text is live text and whose marks are shapes. Nothing
is rasterized, because nothing in the subset needs to be.

Constructs outside the subset are not silently approximated. They raise `UnsupportedConstruct`,
which names the element and the offending declaration, so the failure lands at authoring time
instead of in front of the recipient.
"""

import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

CANVAS_WIDTH_PX = 1280
CANVAS_HEIGHT_PX = 720
EMU_PER_PX = 9525
SLIDE_WIDTH_EMU = CANVAS_WIDTH_PX * EMU_PER_PX
SLIDE_HEIGHT_EMU = CANVAS_HEIGHT_PX * EMU_PER_PX

KINDS = ("text", "rect", "ellipse", "line")
HEX6 = re.compile(r"\A#([0-9A-Fa-f]{6})\Z")
HEX3 = re.compile(r"\A#([0-9A-Fa-f]{3})\Z")
PX = re.compile(r"\A(-?\d+(?:\.\d+)?)px\Z")
BORDER = re.compile(r"\A(\d+(?:\.\d+)?)px\s+solid\s+(#[0-9A-Fa-f]{3,6})\Z")

# Declarations that have no native-object equivalent. Authoring them means the region can only be
# carried across as a picture, so the converter refuses instead of flattening.
BANNED_PROPERTIES = {
    "box-shadow": "no shape equivalent; a shadowed region can only be rasterized",
    "text-shadow": "no shape equivalent; a shadowed region can only be rasterized",
    "filter": "no shape equivalent",
    "backdrop-filter": "no shape equivalent",
    "transform": "no shape equivalent; position the box absolutely instead",
    "mix-blend-mode": "no shape equivalent",
    "clip-path": "no shape equivalent",
    "opacity": "container opacity has no shape equivalent; use a solid value instead",
    "display": "runtime layout; every box is absolutely positioned",
    "position": "runtime layout; every box is absolutely positioned",
    "float": "runtime layout; every box is absolutely positioned",
    "margin": "runtime layout; use absolute left and top",
    "padding": "runtime layout; size the box to its content",
    "content": "generated content has no object equivalent",
}
BANNED_VALUE_TOKENS = (
    ("gradient", "gradients have no shape equivalent"),
    ("url(", "external and background images are outside the subset"),
    ("calc(", "runtime layout; resolve the value at authoring time"),
    ("%", "percentage dimensions are runtime layout; use px"),
    ("auto", "auto dimensions are runtime layout; use px"),
    ("var(", "resolve custom properties at authoring time"),
)


class UnsupportedConstruct(Exception):
    """An authored construct that cannot become a native object."""


class Element:
    def __init__(self, kind, name, box, style, text=""):
        self.kind = kind
        self.name = name
        self.box = box  # (left, top, width, height) in px
        self.style = style
        self.text = text
        self.fill = None  # RRGGBB, resolved at parse time
        self.border = None  # (weight_px, RRGGBB), resolved at parse time

    @property
    def paragraphs(self):
        return self.text.split("\n")


class Slide:
    def __init__(self, name, background=None):
        self.name = name
        self.background = background  # canvas fill as RRGGBB, or None for the app default
        self.elements = []


def _fail(where, message):
    raise UnsupportedConstruct(f"{where}: {message}")


def parse_style(raw, where):
    """Parse an inline style into a dict, rejecting anything outside the subset."""
    style = {}
    for declaration in (raw or "").split(";"):
        if not declaration.strip():
            continue
        prop, separator, value = declaration.partition(":")
        if not separator:
            _fail(where, f"malformed style declaration {declaration.strip()!r}")
        prop = prop.strip().casefold()
        value = value.strip()
        if prop in BANNED_PROPERTIES:
            _fail(where, f"`{prop}` is outside the subset: {BANNED_PROPERTIES[prop]}")
        for token, reason in BANNED_VALUE_TOKENS:
            if token in value.casefold():
                _fail(where, f"`{prop}: {value}` is outside the subset: {reason}")
        style[prop] = value
    return style


def px_value(style, prop, where):
    if prop not in style:
        _fail(where, f"missing required `{prop}`; every box needs absolute left, top, width, height")
    match = PX.match(style[prop].strip())
    if not match:
        _fail(where, f"`{prop}: {style[prop]}` must be an absolute px value")
    return round(float(match.group(1)))


def color(value, where, prop):
    value = value.strip()
    match = HEX6.match(value)
    if match:
        return match.group(1).upper()
    match = HEX3.match(value)
    if match:
        return "".join(channel * 2 for channel in match.group(1)).upper()
    _fail(where, f"`{prop}: {value}` must be a #RGB or #RRGGBB hex value")


def fill_color(style, where):
    for prop in ("background-color", "background"):
        if prop in style:
            return color(style[prop], where, prop)
    return None


def border_of(style, where):
    if "border" not in style:
        return None
    match = BORDER.match(style["border"].strip())
    if not match:
        _fail(where, f"`border: {style['border']}` must be `Npx solid #hex`")
    return round(float(match.group(1))), color(match.group(2), where, "border")


class DeckParser(HTMLParser):
    """Collect slides and their elements from presentation-safe HTML."""

    VOID = {"br", "hr", "img", "input", "meta", "link", "source", "col", "area", "base", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides = []
        self._slide = None
        self._slide_depth = 0
        self._element = None
        self._depth = 0
        self._chunks = []

    @staticmethod
    def _classes(attrs):
        return set((dict(attrs).get("class") or "").split())

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = self._classes(attrs)
        if self._element is not None:
            if tag == "br":
                self._chunks.append("\n")
                return
            if tag not in self.VOID:
                self._depth += 1
            return
        if "slide" in classes:
            if self._slide is not None:
                _fail(f"slide {len(self.slides) + 1}", "slides cannot nest")
            name = attributes.get("data-name") or f"slide-{len(self.slides) + 1}"
            style = parse_style(attributes.get("style"), name)
            self._slide = Slide(name, background=fill_color(style, name))
            self._slide_depth = 0
            return
        kinds = classes & set(KINDS)
        if not kinds:
            if self._slide is not None and tag not in self.VOID:
                self._slide_depth += 1
            return
        if len(kinds) > 1:
            _fail(attributes.get("data-name", tag), f"element declares more than one kind: {sorted(kinds)}")
        if self._slide is None:
            _fail(attributes.get("data-name", tag), "element sits outside any `.slide`")
        kind = kinds.pop()
        name = attributes.get("data-name") or f"{kind}-{len(self._slide.elements) + 1}"
        where = f"{self._slide.name} / {name}"
        style = parse_style(attributes.get("style"), where)
        box = (
            px_value(style, "left", where),
            px_value(style, "top", where),
            px_value(style, "width", where),
            px_value(style, "height", where),
        )
        self._element = Element(kind, name, box, style)
        self._depth = 0
        self._chunks = []

    def handle_startendtag(self, tag, attrs):
        if self._element is not None and tag == "br":
            self._chunks.append("\n")
            return
        started_inside_element = self._element is not None
        self.handle_starttag(tag, attrs)
        if self._element is not None and not started_inside_element:
            # A self-closed element declaration, e.g. `<div class="rect" style="..."/>`.
            self._close_element()

    def handle_data(self, data):
        if self._element is not None:
            self._chunks.append(data)

    def _close_element(self):
        element = self._element
        where = f"{self._slide.name} / {element.name}"
        text = "".join(self._chunks)
        element.text = "\n".join(" ".join(line.split()) for line in text.split("\n")).strip("\n")
        if element.kind == "text" and not element.text:
            _fail(where, "a `text` object carries no text")
        if element.kind != "text" and element.text.strip():
            _fail(where, f"a `{element.kind}` object cannot carry text; use a separate `text` object")
        # Resolve every declared value now, so an unconvertible one fails at authoring time
        # rather than at emission, when a deck is already half written.
        element.fill = fill_color(element.style, where)
        element.border = border_of(element.style, where)
        if element.kind == "line" and element.fill is None:
            _fail(where, "a `line` object needs a `background` hex value as its stroke color")
        if element.kind in ("rect", "ellipse") and element.fill is None and element.border is None:
            _fail(where, f"a `{element.kind}` object needs a `background` hex value, a `border`, or both")
        if element.kind == "text":
            run_properties(element.style, where)
            paragraph_properties(element.style, where)
        self._slide.elements.append(element)
        self._element = None
        self._chunks = []

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self._element is not None:
            if self._depth > 0:
                self._depth -= 1
                return
            self._close_element()
            return
        if self._slide is None:
            return
        if self._slide_depth > 0:
            self._slide_depth -= 1
            return
        # The slide's own container closed.
        self.slides.append(self._slide)
        self._slide = None


def parse_html(html):
    parser = DeckParser()
    parser.feed(html)
    parser.close()
    if parser._slide is not None:
        parser.slides.append(parser._slide)
    if not parser.slides:
        raise UnsupportedConstruct("no `.slide` element found")
    for slide in parser.slides:
        if not slide.elements:
            _fail(slide.name, "slide holds no objects")
    return parser.slides


# --- OOXML emission -------------------------------------------------------------------------

NS = (
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
)
DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'


def emu(px):
    return int(round(px * EMU_PER_PX))


def xfrm(box):
    left, top, width, height = box
    return (
        f'<a:xfrm><a:off x="{emu(left)}" y="{emu(top)}"/>'
        f'<a:ext cx="{emu(max(width, 0))}" cy="{emu(max(height, 0))}"/></a:xfrm>'
    )


def run_properties(style, where):
    size = style.get("font-size")
    if size is None:
        _fail(where, "a `text` object needs an explicit `font-size` in px")
    match = PX.match(size.strip())
    if not match:
        _fail(where, f"`font-size: {size}` must be an absolute px value")
    hundredths = int(round(float(match.group(1)) * 0.75 * 100))
    weight = style.get("font-weight", "").strip().casefold()
    bold = "1" if weight in ("bold", "bolder") or (weight.isdigit() and int(weight) >= 600) else "0"
    italic = "1" if style.get("font-style", "").strip().casefold() == "italic" else "0"
    parts = [f'<a:rPr lang="en-US" sz="{hundredths}" b="{bold}" i="{italic}" dirty="0">']
    if "color" in style:
        parts.append(f'<a:solidFill><a:srgbClr val="{color(style["color"], where, "color")}"/></a:solidFill>')
    if "font-family" in style:
        family = style["font-family"].split(",")[0].strip().strip("'\"")
        if family:
            parts.append(f"<a:latin typeface={quoteattr(family)}/><a:cs typeface={quoteattr(family)}/>")
    parts.append("</a:rPr>")
    return "".join(parts)


def paragraph_properties(style, where):
    align = {"left": "l", "center": "ctr", "right": "r", "justify": "just"}
    parts = []
    if "text-align" in style:
        key = style["text-align"].strip().casefold()
        if key not in align:
            _fail(where, f"`text-align: {style['text-align']}` is outside the subset")
        parts.append(f'algn="{align[key]}"')
    attributes = (" " + " ".join(parts)) if parts else ""
    spacing = ""
    if "line-height" in style:
        raw = style["line-height"].strip()
        match = PX.match(raw)
        if match:
            spacing = f'<a:lnSpc><a:spcPts val="{int(round(float(match.group(1)) * 0.75 * 100))}"/></a:lnSpc>'
        else:
            try:
                spacing = f'<a:lnSpc><a:spcPct val="{int(round(float(raw) * 100000))}"/></a:lnSpc>'
            except ValueError:
                _fail(where, f"`line-height: {raw}` must be a px value or a unitless multiplier")
    if not spacing and not attributes:
        return ""
    return f"<a:pPr{attributes}>{spacing}</a:pPr>" if spacing else f"<a:pPr{attributes}/>"


def text_body(element, where):
    run_props = run_properties(element.style, where)
    para_props = paragraph_properties(element.style, where)
    paragraphs = []
    for line in element.paragraphs:
        if line:
            paragraphs.append(f"<a:p>{para_props}<a:r>{run_props}<a:t>{escape(line)}</a:t></a:r></a:p>")
        else:
            paragraphs.append(f"<a:p>{para_props}<a:endParaRPr lang=\"en-US\"/></a:p>")
    return (
        '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"/>'
        "<a:lstStyle/>" + "".join(paragraphs) + "</p:txBody>"
    )


def shape_xml(element, shape_id, where):
    name = quoteattr(element.name)
    if element.kind == "text":
        return (
            f"<p:sp><p:nvSpPr><p:cNvPr id=\"{shape_id}\" name={name}/>"
            '<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f"<p:spPr>{xfrm(element.box)}<a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom>"
            "<a:noFill/></p:spPr>" + text_body(element, where) + "</p:sp>"
        )
    if element.kind == "line":
        stroke = element.fill
        left, top, width, height = element.box
        weight = emu(max(height, 1))
        return (
            f"<p:sp><p:nvSpPr><p:cNvPr id=\"{shape_id}\" name={name}/>"
            "<p:cNvSpPr/><p:nvPr/></p:nvSpPr>"
            f"<p:spPr>{xfrm((left, top, width, 0))}"
            '<a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:noFill/>'
            f'<a:ln w="{weight}" cap="flat"><a:solidFill><a:srgbClr val="{stroke}"/></a:solidFill></a:ln>'
            "</p:spPr>"
            "<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang=\"en-US\"/></a:p></p:txBody></p:sp>"
        )
    geometry = "ellipse" if element.kind == "ellipse" else "rect"
    fill, border = element.fill, element.border
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    if border:
        weight, stroke = border
        line_xml = f'<a:ln w="{emu(weight)}"><a:solidFill><a:srgbClr val="{stroke}"/></a:solidFill></a:ln>'
    else:
        line_xml = "<a:ln><a:noFill/></a:ln>"
    return (
        f"<p:sp><p:nvSpPr><p:cNvPr id=\"{shape_id}\" name={name}/>"
        "<p:cNvSpPr/><p:nvPr/></p:nvSpPr>"
        f"<p:spPr>{xfrm(element.box)}<a:prstGeom prst=\"{geometry}\"><a:avLst/></a:prstGeom>"
        f"{fill_xml}{line_xml}</p:spPr>"
        "<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang=\"en-US\"/></a:p></p:txBody></p:sp>"
    )


def slide_xml(slide):
    shapes = []
    for index, element in enumerate(slide.elements, start=2):
        shapes.append(shape_xml(element, index, f"{slide.name} / {element.name}"))
    background = (
        f'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{slide.background}"/></a:solidFill>'
        "<a:effectLst/></p:bgPr></p:bg>"
        if slide.background
        else ""
    )
    return (
        DECL + f"<p:sld {NS}><p:cSld>{background}<p:spTree>"
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        + "".join(shapes)
        + "</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"
    )


def _relationships(entries):
    body = "".join(
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/{kind}" Target="{target}"/>'
        for rid, kind, target in entries
    )
    return (
        DECL
        + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + body
        + "</Relationships>"
    )


def _theme():
    scheme = "".join(
        f'<a:{tag}><a:srgbClr val="{value}"/></a:{tag}>'
        for tag, value in (
            ("dk1", "000000"), ("lt1", "FFFFFF"), ("dk2", "000000"), ("lt2", "FFFFFF"),
            ("accent1", "000000"), ("accent2", "000000"), ("accent3", "000000"),
            ("accent4", "000000"), ("accent5", "000000"), ("accent6", "000000"),
            ("hlink", "000000"), ("folHlink", "000000"),
        )
    )
    fill = '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    line = '<a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    return (
        DECL
        + '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Justesse">'
        f"<a:themeElements><a:clrScheme name=\"Justesse\">{scheme}</a:clrScheme>"
        '<a:fontScheme name="Justesse">'
        '<a:majorFont><a:latin typeface=""/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
        '<a:minorFont><a:latin typeface=""/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
        "</a:fontScheme>"
        '<a:fmtScheme name="Justesse">'
        f"<a:fillStyleLst>{fill * 3}</a:fillStyleLst>"
        f"<a:lnStyleLst>{line * 3}</a:lnStyleLst>"
        "<a:effectStyleLst>"
        + '<a:effectStyle><a:effectLst/></a:effectStyle>' * 3
        + "</a:effectStyleLst>"
        f"<a:bgFillStyleLst>{fill * 3}</a:bgFillStyleLst>"
        "</a:fmtScheme></a:themeElements></a:theme>"
    )


def _empty_sp_tree(extra=""):
    return (
        "<p:cSld><p:spTree>"
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f"</p:spTree></p:cSld>{extra}"
    )


CLR_MAP = (
    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
    'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" '
    'folHlink="folHlink"/>'
)


def build_pptx(slides, destination):
    """Write `slides` to a PPTX at `destination`."""
    destination = Path(destination)
    count = len(slides)
    slide_ids = "".join(
        f'<p:sldId id="{256 + index}" r:id="rId{index + 2}"/>' for index in range(count)
    )
    presentation = (
        DECL + f"<p:presentation {NS}>"
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f"<p:sldIdLst>{slide_ids}</p:sldIdLst>"
        f'<p:sldSz cx="{SLIDE_WIDTH_EMU}" cy="{SLIDE_HEIGHT_EMU}"/>'
        '<p:notesSz cx="6858000" cy="9144000"/>'
        "</p:presentation>"
    )
    presentation_rels = _relationships(
        [("rId1", "officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml")]
        + [
            (f"rId{index + 2}", "officeDocument/2006/relationships/slide", f"slides/slide{index + 1}.xml")
            for index in range(count)
        ]
        + [(f"rId{count + 2}", "officeDocument/2006/relationships/theme", "theme/theme1.xml")]
    )
    master = (
        DECL + f"<p:sldMaster {NS}>" + _empty_sp_tree(CLR_MAP)
        + '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
        + "</p:sldMaster>"
    )
    layout = (
        DECL + f'<p:sldLayout {NS} type="blank" preserve="1">' + _empty_sp_tree()
        + "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>"
    )
    overrides = "".join(
        f'<Override PartName="/ppt/slides/slide{index + 1}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for index in range(count)
    )
    content_types = (
        DECL + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
        + overrides
        + "</Types>"
    )
    parts = {
        "[Content_Types].xml": content_types,
        "_rels/.rels": _relationships([
            ("rId1", "officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
        ]),
        "ppt/presentation.xml": presentation,
        "ppt/_rels/presentation.xml.rels": presentation_rels,
        "ppt/slideMasters/slideMaster1.xml": master,
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": _relationships([
            ("rId1", "officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        ]),
        "ppt/slideLayouts/slideLayout1.xml": layout,
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": _relationships([
            ("rId1", "officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml"),
        ]),
        "ppt/theme/theme1.xml": _theme(),
    }
    for index, slide in enumerate(slides, start=1):
        parts[f"ppt/slides/slide{index}.xml"] = slide_xml(slide)
        parts[f"ppt/slides/_rels/slide{index}.xml.rels"] = _relationships([
            ("rId1", "officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
        ])
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, payload in parts.items():
            archive.writestr(name, payload)
    return destination


def convert(html_path, pptx_path):
    slides = parse_html(Path(html_path).read_text(encoding="utf-8"))
    build_pptx(slides, pptx_path)
    return slides


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip())
        return 2
    try:
        slides = convert(argv[1], argv[2])
    except UnsupportedConstruct as error:
        print(f"FAIL: {error}")
        print("\nThis construct cannot become a native object. Fix it in the HTML; do not export a picture.")
        return 1
    objects = sum(len(slide.elements) for slide in slides)
    print(f"PASS: {len(slides)} slide(s), {objects} native objects, 0 rasterized regions -> {argv[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
