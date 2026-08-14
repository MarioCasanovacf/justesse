#!/usr/bin/env python3
"""Emit the object inventory of a PPTX as NDJSON, so manipulability is verified, not asserted.

    python3 tools/inspect_pptx.py deck.pptx > deck.inspect.ndjson

One line per record. `deck` and `slide` records carry counts; every other line is one object with
its name, geometry in px on the 1280x720 canvas, and, for text, the exact string the file holds.
A `picture` record marks a rasterized region: the presentation-safe contract expects zero of them,
so a non-zero count is the finding, not a footnote.

Reading the inventory back out of the file is the point. A converter can claim it emitted native
objects; only the file can show it.
"""

import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
EMU_PER_PX = 9525


def px(value):
    return round(int(value) / EMU_PER_PX) if value is not None else None


def bbox_of(node):
    xfrm = node.find(f"{P}spPr/{A}xfrm")
    if xfrm is None:
        xfrm = node.find(f"{P}grpSpPr/{A}xfrm")
    if xfrm is None:
        return None
    off = xfrm.find(f"{A}off")
    ext = xfrm.find(f"{A}ext")
    if off is None or ext is None:
        return None
    return [px(off.get("x")), px(off.get("y")), px(ext.get("cx")), px(ext.get("cy"))]


def text_of(node):
    """Join runs within a paragraph, and paragraphs with a newline, as the file stores them."""
    return "\n".join(
        "".join(run.text or "" for run in paragraph.iter(f"{A}t"))
        for paragraph in node.iter(f"{A}p")
    )


def type_of(node):
    """Size in px and family of the first styled run, or (None, None)."""
    for props in node.iter(f"{A}rPr"):
        size = props.get("sz")
        latin = props.find(f"{A}latin")
        family = latin.get("typeface") if latin is not None else None
        if size is not None:
            # sz is hundredths of a point; px = pt * 96/72.
            return round(int(size) / 100 * 96 / 72, 1), family
        if family:
            return None, family
    return None, None


def fill_of(node):
    solid = node.find(f"{P}spPr/{A}solidFill/{A}srgbClr")
    if solid is not None:
        return "#" + solid.get("val")
    stroke = node.find(f"{P}spPr/{A}ln/{A}solidFill/{A}srgbClr")
    if stroke is not None:
        return "#" + stroke.get("val")
    return None


def slide_numbers(archive):
    numbers = []
    for name in archive.namelist():
        if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
            numbers.append(int(name[len("ppt/slides/slide"):-len(".xml")]))
    return sorted(numbers)


def inspect(path):
    """Yield one record dict per deck, slide, and object."""
    records = []
    with zipfile.ZipFile(path) as archive:
        numbers = slide_numbers(archive)
        records.append({"kind": "deck", "name": Path(path).name, "slides": len(numbers)})
        for number in numbers:
            root = ElementTree.fromstring(archive.read(f"ppt/slides/slide{number}.xml"))
            tree = root.find(f"{P}cSld/{P}spTree")
            shapes = [] if tree is None else [
                child for child in tree
                if child.tag in (f"{P}sp", f"{P}pic", f"{P}graphicFrame", f"{P}grpSp")
            ]
            slide_record = {"kind": "slide", "slide": number, "objects": len(shapes)}
            background = root.find(f"{P}cSld/{P}bg/{P}bgPr/{A}solidFill/{A}srgbClr")
            if background is not None:
                slide_record["background"] = "#" + background.get("val")
            records.append(slide_record)
            for shape in shapes:
                if shape.tag == f"{P}pic":
                    name_node = shape.find(f"{P}nvPicPr/{P}cNvPr")
                    records.append({
                        "kind": "picture",
                        "slide": number,
                        "name": None if name_node is None else name_node.get("name"),
                        "bbox": bbox_of(shape),
                        "rasterized": True,
                    })
                    continue
                if shape.tag == f"{P}graphicFrame":
                    name_node = shape.find(f"{P}nvGraphicFramePr/{P}cNvPr")
                    records.append({
                        "kind": "graphicFrame",
                        "slide": number,
                        "name": None if name_node is None else name_node.get("name"),
                    })
                    continue
                if shape.tag == f"{P}grpSp":
                    records.append({"kind": "group", "slide": number})
                    continue
                name_node = shape.find(f"{P}nvSpPr/{P}cNvPr")
                shape_props = shape.find(f"{P}nvSpPr/{P}cNvSpPr")
                geometry = shape.find(f"{P}spPr/{A}prstGeom")
                preset = None if geometry is None else geometry.get("prst")
                is_textbox = shape_props is not None and shape_props.get("txBox") == "1"
                record = {
                    "kind": "textbox" if is_textbox else ("line" if preset == "line" else "shape"),
                    "slide": number,
                    "name": None if name_node is None else name_node.get("name"),
                    "geometry": preset,
                    "bbox": bbox_of(shape),
                }
                color = fill_of(shape)
                if color:
                    record["color"] = color
                if is_textbox:
                    text = text_of(shape)
                    record["text"] = text
                    record["textChars"] = len(text)
                    size, family = type_of(shape)
                    if size is not None:
                        record["fontSizePx"] = size
                    if family:
                        record["fontFamily"] = family
                records.append(record)
    return records


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"FAIL: no presentation at {path}", file=sys.stderr)
        return 1
    records = inspect(path)
    for record in records:
        print(json.dumps(record, ensure_ascii=False))
    rasterized = sum(1 for record in records if record.get("rasterized"))
    editable = sum(1 for record in records if record["kind"] in ("textbox", "shape", "line"))
    print(
        f"{editable} native objects, {rasterized} rasterized regions",
        file=sys.stderr,
    )
    return 1 if rasterized else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
