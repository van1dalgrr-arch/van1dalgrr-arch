"""Bakes the display font (Noto Serif JP, SIL OFL) into scripts/glyphs.json as SVG paths.

Headlines and kanji are drawn as paths, so they look the same on every machine,
including ones without Japanese fonts. Run it only when a headline gets a new character:

    npm pack @fontsource/noto-serif-jp && tar xzf fontsource-noto-serif-jp-*.tgz
    pip install fonttools brotli
    python3 scripts/glyphs.py package/files
"""

import glob
import json
import string
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

WEIGHTS = (400, 700, 900)
# Every non-ASCII character any headline uses. ASCII is always included.
JAPANESE = (
    "ヴァンダル バックエンド開発者 またね 作品 記録 注文 番犬 鼓動 配備 対話 毎日 実戦 修行 道 環境 "
    "統計 連絡 今 発 着 駅 桜 夜 印 技 流 人 物 猫 線 夢 見 進 中 済 次 書 全 部 緑 通 過 終 点 "
    "・ 「 」 ー 、 。 → ✿"
)
CHARS = sorted(set(string.printable.strip() + " " + JAPANESE.replace(" ", "")) | {" "})


def main(font_dir):
    out = {"upm": None, "weights": {}}
    for w in WEIGHTS:
        files = sorted(glob.glob(f"{font_dir}/noto-serif-jp-*-{w}-normal.woff2"))
        need, got = set(CHARS), {}
        for f in files:
            if not need:
                break
            font = TTFont(f)
            cmap = font.getBestCmap()
            gs = font.getGlyphSet()
            out["upm"] = font["head"].unitsPerEm
            for ch in list(need):
                name = cmap.get(ord(ch))
                if not name:
                    continue
                pen = SVGPathPen(gs)
                gs[name].draw(pen)
                got[ch] = [gs[name].width, pen.getCommands()]
                need.discard(ch)
        if need - {"✿", "→"}:
            print(f"weight {w}: missing {''.join(sorted(need))}")
        out["weights"][str(w)] = got
    Path(__file__).with_name("glyphs.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print("glyphs.json written")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "package/files")
