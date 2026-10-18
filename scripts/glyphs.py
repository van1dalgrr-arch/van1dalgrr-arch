#!/usr/bin/env python3
"""Запекает шрифты заголовков в scripts/glyphs.json — контурами SVG, чтобы надписи выглядели одинаково везде.

Нужно только когда в заголовке появляется новый символ (латиница и ASCII уже есть):

    npm pack @fontsource/geist-sans && for t in *.tgz; do tar xzf $t --one-top-level; done
    pip install fonttools brotli
    python3 scripts/glyphs.py <папка с распакованными пакетами>

Шрифт — Geist Sans (SIL OFL): 600 для заголовков, 400 для подзаголовков.
"""
import glob, json, string, sys
from pathlib import Path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONTS = {   # имя → (пакет, вес)
    "head": ("geist-sans", 600),
    "body": ("geist-sans", 400),
}
CHARS = set(string.printable.strip()) | {" "} | set("·→—…’")

def main(root):
    out = {}
    for name, (pkg, w) in FONTS.items():
        got, upm = {}, 1000
        for f in sorted(glob.glob(f"{root}/**/{pkg}-*-{w}-normal.woff2", recursive=True)):
            font = TTFont(f)
            upm, cmap, gs = font["head"].unitsPerEm, font.getBestCmap(), font.getGlyphSet()
            for ch in CHARS - got.keys():
                if ord(ch) in cmap:
                    pen = SVGPathPen(gs)
                    gs[cmap[ord(ch)]].draw(pen)
                    got[ch] = [gs[cmap[ord(ch)]].width, pen.getCommands()]
        out[name] = {"upm": upm, "g": got}
        print(name, len(got), "glyphs; нет:", "".join(sorted(CHARS - got.keys())))
    Path(__file__).with_name("glyphs.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
