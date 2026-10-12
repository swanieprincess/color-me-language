#!/usr/bin/env python3
"""Build a TrueType font from one SVG file per glyph.

The drawing tool is Inkscape (or anything that writes plain SVG). Each glyph
lives in its own SVG file, drawn on the glyph template:

    glyphs/A.svg  glyphs/a.svg  glyphs/zero.svg  glyphs/period.svg ...

Conventions (see fonts/README.md for the Inkscape walk-through):

* File name = glyph name. Letters and digits use their AGL names
  (``A``, ``a``, ``zero`` ... ``nine``); punctuation uses AGL names too
  (``period``, ``comma``, ``question``, ``exclam``, ``hyphen``,
  ``quotesingle``, ``ampersand`` ...). Unknown names are skipped with a
  warning.
* The SVG ``viewBox`` is the glyph box. Its WIDTH is the advance width (so
  the gaps between the drawing and the left/right page edges are the side
  bearings). The baseline sits at ``baseline_svg`` user units from the top
  (800 on the standard template, whose viewBox is 1000 tall).
* Everything inside a layer or group labelled ``GUIDES`` is ignored.
* Every drawn object (path, rect, circle, ellipse, polygon ...) is a filled
  shape and all objects are UNIONED, whatever direction they were drawn in.
  Holes (the counter of an O) must belong to the same object as the outer
  shape: Path > Difference or Path > Exclusion in Inkscape. An object with
  ``fill-rule: evenodd`` is read with that rule. Stroke-only objects
  (``fill: none``) are skipped with a warning: run Path > Stroke to Path.

Usage:

    build_font.py init  <project-dir> [--charset basic|caps|full]
        Create glyphs/<name>.svg from the template for every character
        in the charset that does not exist yet.

    build_font.py build <project-dir> [--out <dir>]
        Read <project-dir>/font.json and glyphs/*.svg, write
        <out>/<Family>-<Style>.ttf (+ .woff2 when brotli is installed) and
        a specimen PNG + HTML.

    build_font.py check <project-dir>
        List which glyphs of the charset exist and which are missing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from fontTools.agl import AGL2UV
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.transform import Identity, Transform
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path.parser import parse_path
from fontTools.svgLib.path.shapes import PathBuilder

try:  # optional but strongly recommended: union of the drawn objects
    import pathops  # type: ignore
except ImportError:  # pragma: no cover
    pathops = None

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "glyph_template.svg"
INKSCAPE_NS = "http://www.inkscape.org/namespaces/inkscape"
SVG_NS = "http://www.w3.org/2000/svg"

CHARSETS = {
    "caps": [chr(c) for c in range(65, 91)] + list("0123456789") + list(".,!?-'&"),
    "basic": [chr(c) for c in range(65, 91)]
    + [chr(c) for c in range(97, 123)]
    + list("0123456789")
    + list(".,!?-'\":;()&"),
    "full": [chr(c) for c in range(33, 127)],
}

UV2AGL = {v: k for k, v in AGL2UV.items()}


def glyph_name_for(char: str) -> str:
    return UV2AGL.get(ord(char), "uni%04X" % ord(char))


def codepoint_for(name: str) -> int | None:
    if name in AGL2UV:
        return AGL2UV[name]
    m = re.fullmatch(r"uni([0-9A-Fa-f]{4,6})", name)
    if m:
        return int(m.group(1), 16)
    if len(name) == 1:
        return ord(name)
    return None


# ----------------------------------------------------------------------------
# SVG reading
# ----------------------------------------------------------------------------

def _is_guide(el: ET.Element) -> bool:
    label = el.get(f"{{{INKSCAPE_NS}}}label", "") or ""
    ident = el.get("id", "") or ""
    return label.upper().startswith("GUIDE") or ident.upper().startswith("GUIDE")


def _style(el: ET.Element) -> dict[str, str]:
    """Presentation attributes + the style attribute, as a dict."""
    out: dict[str, str] = {}
    for key in ("fill", "fill-rule", "stroke"):
        if el.get(key) is not None:
            out[key] = el.get(key).strip()  # type: ignore[union-attr]
    for part in (el.get("style") or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def _parse_transform(text: str | None) -> Transform | None:
    """SVG transform attribute -> fontTools Transform (translate, scale,
    rotate, skewX, skewY, matrix; composed left to right as SVG does)."""
    if not text or not text.strip():
        return None
    import math

    t = Identity
    for fn, args in re.findall(r"(\w+)\s*\(([^)]*)\)", text):
        nums = [float(v) for v in re.split(r"[\s,]+", args.strip()) if v]
        if fn == "translate":
            t = t.translate(nums[0], nums[1] if len(nums) > 1 else 0)
        elif fn == "scale":
            t = t.scale(nums[0], nums[1] if len(nums) > 1 else nums[0])
        elif fn == "rotate":
            a = math.radians(nums[0])
            if len(nums) == 3:
                t = t.translate(nums[1], nums[2]).rotate(a).translate(-nums[1], -nums[2])
            else:
                t = t.rotate(a)
        elif fn == "skewX":
            t = t.skew(math.radians(nums[0]), 0)
        elif fn == "skewY":
            t = t.skew(0, math.radians(nums[0]))
        elif fn == "matrix" and len(nums) == 6:
            t = t.transform(Transform(*nums))
    return None if t == Identity else t


def _viewbox(root: ET.Element) -> tuple[float, float, float, float]:
    vb = root.get("viewBox")
    if vb:
        x, y, w, h = (float(v) for v in re.split(r"[ ,]+", vb.strip()))
        return x, y, w, h
    num = lambda s: float(re.sub(r"[a-z%]+$", "", s))  # noqa: E731
    return 0.0, 0.0, num(root.get("width")), num(root.get("height"))


def _shapes(root: ET.Element, name: str):
    """Yield (element, path_d) for every drawn object outside GUIDES."""
    def walk(el: ET.Element, inherited: dict[str, str]):
        if _is_guide(el):
            return
        style = dict(inherited)
        style.update(_style(el))
        tag = el.tag.split("}")[-1]
        if tag == "g":
            if el.get("transform"):
                print(
                    f"  warning: {name}: a group carries a transform; ungroup "
                    "(Shift+Ctrl+G) and re-save, or the glyph may be misplaced",
                    file=sys.stderr,
                )
            for child in el:
                yield from walk(child, style)
            return
        if tag in ("path", "rect", "circle", "ellipse", "line", "polyline", "polygon"):
            if style.get("fill", "").lower() == "none":
                print(f"  warning: {name}: skipped a stroke-only <{tag}>; run Path > Stroke to Path", file=sys.stderr)
                return
            el_transform = _parse_transform(el.get("transform"))
            if "transform" in el.attrib:  # parsed above; PathBuilder only knows matrix()
                el = ET.Element(el.tag, {k: v for k, v in el.attrib.items() if k != "transform"})
            pb = PathBuilder()
            pb.add_path_from_element(el)
            for d in pb.paths:
                yield el, d, el_transform, style
        elif tag in ("text", "image"):
            print(f"  warning: {name}: <{tag}> ignored; convert text with Path > Object to Path", file=sys.stderr)
        else:
            for child in el:
                yield from walk(child, style)

    yield from walk(root, {})


def read_glyph(svg_path: Path, meta: dict) -> tuple[RecordingPen, int]:
    """Return (outline in font units with overlaps removed, advance width)."""
    root = ET.parse(svg_path).getroot()
    vx, vy, vw, vh = _viewbox(root)
    upm = meta["unitsPerEm"]
    scale = upm / vh
    baseline = meta["baseline_svg"]
    # x' = (x - vx) * s ; y' = (baseline - (y - vy)) * s
    transform = (scale, 0, 0, -scale, -vx * scale, (baseline + vy) * scale)
    advance = int(round(vw * scale))

    pieces = []
    for el, d, el_transform, style in _shapes(root, svg_path.name):
        rec = RecordingPen()
        pen = TransformPen(rec, transform)
        if el_transform:
            pen = TransformPen(pen, el_transform)
        parse_path(d, pen)
        if not rec.value:
            continue
        if pathops is None:
            pieces.append(rec)
            continue
        path = pathops.Path()
        rec.replay(path.getPen())
        if style.get("fill-rule", "").lower() == "evenodd":
            path.fillType = pathops.FillType.EVEN_ODD
        path.simplify(fix_winding=True, keep_starting_points=False)
        pieces.append(path)

    out = RecordingPen()
    if not pieces:
        return out, advance
    if pathops is None:
        for rec in pieces:
            rec.replay(out)
        return out, advance
    if meta.get("removeOverlaps", True):
        pathops.union(pieces, out, fix_winding=True, keep_starting_points=False)
    else:
        for path in pieces:
            path.draw(out)
    return out, advance


def outline_to_ttglyph(rec: RecordingPen):
    ttpen = TTGlyphPen(None)
    rec.replay(Cu2QuPen(ttpen, max_err=1.0, reverse_direction=False))
    return ttpen.glyph()


# ----------------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------------

def cmd_init(project: Path, charset: str) -> None:
    glyph_dir = project / "glyphs"
    glyph_dir.mkdir(parents=True, exist_ok=True)
    made = 0
    for ch in CHARSETS[charset]:
        name = glyph_name_for(ch)
        target = glyph_dir / f"{name}.svg"
        if target.exists():
            continue
        text = TEMPLATE.read_text(encoding="utf-8")
        text = text.replace("GLYPH_LABEL", xml_escape(f"{name}  ({ch})"))
        target.write_text(text, encoding="utf-8")
        made += 1
    print(f"created {made} glyph files in {glyph_dir}")


def cmd_check(project: Path) -> None:
    meta = json.loads((project / "font.json").read_text())
    charset = CHARSETS[meta.get("charset", "basic")]
    glyph_dir = project / "glyphs"
    have, missing = [], []
    for ch in charset:
        name = glyph_name_for(ch)
        (have if (glyph_dir / f"{name}.svg").exists() else missing).append(f"{name}({ch})")
    print(f"{len(have)} glyph files present, {len(missing)} missing")
    if missing:
        print("missing: " + " ".join(missing))


def cmd_build(project: Path, out: Path | None) -> Path:
    meta = json.loads((project / "font.json").read_text())
    family = meta["family"]
    style = meta.get("style", "Regular")
    upm = meta["unitsPerEm"]
    out = out or project / "build"
    out.mkdir(parents=True, exist_ok=True)

    glyph_dir = project / "glyphs"
    glyphs: dict[str, object] = {}
    metrics: dict[str, tuple[int, int]] = {}
    cmap: dict[int, str] = {}

    # Required glyphs.
    glyphs[".notdef"] = TTGlyphPen(None).glyph()
    metrics[".notdef"] = (int(upm * 0.5), 0)
    glyphs["space"] = TTGlyphPen(None).glyph()
    metrics["space"] = (int(meta.get("spaceAdvance", upm * 0.25)), 0)
    cmap[0x20] = "space"
    cmap[0xA0] = "space"

    loaded = 0
    for svg in sorted(glyph_dir.glob("*.svg")):
        name = svg.stem
        if name in ("space", ".notdef"):
            continue
        cp = codepoint_for(name)
        if cp is None:
            print(f"  skip {svg.name}: not an AGL or uniXXXX glyph name", file=sys.stderr)
            continue
        rec, advance = read_glyph(svg, meta)
        if not rec.value:
            continue  # template still empty
        glyph = outline_to_ttglyph(rec)
        glyphs[name] = glyph
        glyph.recalcBounds(None)
        metrics[name] = (advance, getattr(glyph, "xMin", 0))
        cmap[cp] = name
        loaded += 1

    if loaded == 0:
        sys.exit("no glyphs with outlines found; draw some letters first")

    order = [".notdef", "space"] + [n for n in glyphs if n not in (".notdef", "space")]
    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    asc, desc = meta["ascender"], meta["descender"]
    fb.setupHorizontalHeader(ascent=asc, descent=desc)
    fb.setupOS2(
        sTypoAscender=asc,
        sTypoDescender=desc,
        sTypoLineGap=0,
        usWinAscent=asc,
        usWinDescent=-desc,
        sCapHeight=meta.get("capHeight", int(upm * 0.7)),
        sxHeight=meta.get("xHeight", int(upm * 0.5)),
        usWeightClass=meta.get("weightClass", 400),
        fsType=0,
    )
    full = f"{family} {style}".strip()
    ps = re.sub(r"[^A-Za-z0-9]", "", family) + "-" + re.sub(r"[^A-Za-z0-9]", "", style)
    fb.setupNameTable(
        {
            "familyName": family,
            "styleName": style,
            "fullName": full,
            "psName": ps,
            "version": "Version " + meta.get("version", "0.1"),
            "copyright": meta.get("copyright", ""),
            "designer": meta.get("designer", ""),
            "uniqueFontIdentifier": f"{ps};{meta.get('version', '0.1')}",
        }
    )
    fb.setupPost()
    fb.font["head"].unitsPerEm = upm

    ttf = out / f"{ps}.ttf"
    fb.save(str(ttf))
    print(f"wrote {ttf}  ({loaded} drawn glyphs)")

    try:
        import brotli  # noqa: F401

        fb.font.flavor = "woff2"
        woff2 = out / f"{ps}.woff2"
        fb.font.save(str(woff2))
        print(f"wrote {woff2}")
    except ImportError:
        pass

    write_specimen(ttf, out, meta, [chr(c) for c in sorted(cmap) if c > 0x20])
    return ttf


def write_specimen(ttf: Path, out: Path, meta: dict, chars: list[str]) -> None:
    sample = meta.get("sample", "The Learning Dojo")
    html = out / "specimen.html"
    html.write_text(
        f"""<!doctype html><meta charset="utf-8"><title>{meta['family']} specimen</title>
<style>
@font-face{{font-family:"{meta['family']}";src:url("{ttf.name}")}}
body{{font-family:"{meta['family']}",sans-serif;background:#fff;color:#111;padding:40px}}
h1{{font-size:96px;margin:0 0 24px;font-weight:normal}}
.outline{{color:#fff;-webkit-text-stroke:3px #111;paint-order:stroke fill}}
p{{font-size:40px;line-height:1.3;margin:0 0 16px;word-break:break-all}}
</style>
<h1>{sample}</h1><h1 class="outline">{sample}</h1>
<p>{''.join(chars)}</p>
""",
        encoding="utf-8",
    )
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    font_big = ImageFont.truetype(str(ttf), 120)
    font_small = ImageFont.truetype(str(ttf), 56)
    img = Image.new("RGB", (1600, 520), "white")
    d = ImageDraw.Draw(img)
    d.text((40, 40), sample, font=font_big, fill="black")
    d.text((40, 220), sample, font=font_big, fill="white", stroke_width=4, stroke_fill="black")
    d.text((40, 400), "".join(chars)[:40], font=font_small, fill="black")
    png = out / "specimen.png"
    img.save(png)
    print(f"wrote {png} and {html}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("project", type=Path)
    p.add_argument("--charset", choices=sorted(CHARSETS), default="basic")
    p = sub.add_parser("check")
    p.add_argument("project", type=Path)
    p = sub.add_parser("build")
    p.add_argument("project", type=Path)
    p.add_argument("--out", type=Path)
    a = ap.parse_args()
    if a.cmd == "init":
        cmd_init(a.project, a.charset)
    elif a.cmd == "check":
        cmd_check(a.project)
    else:
        cmd_build(a.project, a.out)


if __name__ == "__main__":
    main()
