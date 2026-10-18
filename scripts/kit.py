"""Общее для всех картинок профиля: палитра, шрифты-контуры, иконки, пиксель-арт, звёзды.

Стиль: белая ночь в Петербурге — сине-чёрный фон, приглушённые лаванда, пудрово-розовый и персик, без неона.
"""
import json, random
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
ROOT = HERE.parent
GLYPHS = json.loads((HERE / "glyphs.json").read_text())
ICONS = json.loads((HERE / "icons.json").read_text())

MONO = "ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

C = dict(
    night="#090b11", bg="#0d1017", panel="#12161f", panel2="#181d28", line="#262c3a",
    text="#e8e4dc", soft="#bdb7ad", muted="#8b8a94", faint="#4b4f5e",
    violet="#7d77a8", lilac="#a59fc9", pink="#b9849a", rose="#d0a3b3", orange="#c9956b",
    amber="#dcb48c", sun="#ecd5a4", cyan="#8fb3bf", green="#9cbf9f",
)
GRAD = [C["violet"], C["pink"], C["orange"]]   # главный градиент профиля

PIX = {"p": C["violet"], "l": C["lilac"], "m": C["pink"], "r": C["rose"], "o": C["orange"],
       "a": C["amber"], "y": C["sun"], "w": C["text"], "k": C["night"], "g": C["faint"], "c": C["cyan"]}


def esc(s):
    return escape(str(s))


def tw(s, size, mono=True):
    """Ширина текста системным шрифтом — на глаз, для отступов."""
    return len(s) * size * (0.602 if mono else 0.56)


# ── надписи контурами ──

def gw(s, size, font="display", tracking=0):
    f = GLYPHS[font]
    k = size / f["upm"]
    return sum(f["g"].get(c, [f["upm"] * 0.5])[0] * k + tracking for c in s) - (tracking if s else 0)


def gt(s, x, y, size, fill, font="display", anchor="start", tracking=0, extra=""):
    """Текст из запечённых контуров; y — базовая линия."""
    f = GLYPHS[font]
    k = size / f["upm"]
    w = gw(s, size, font, tracking)
    x -= {"start": 0, "middle": w / 2, "end": w}[anchor]
    out = []
    for c in s:
        adv, d = f["g"].get(c, [f["upm"] * 0.5, ""])
        if d:
            out.append(f'<path transform="translate({x:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})" d="{d}"/>')
        x += adv * k + tracking
    return f'<g fill="{fill}"{extra}>{"".join(out)}</g>'


# ── прочее ──

def icon(name, x, y, size, fill, extra=""):
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({size / 24:.4f})" d="{ICONS[name]}" fill="{fill}"{extra}/>'


def lgrad(gid, colors, x1=0, y1=0, x2=1, y2=0, anim=None):
    stops = "".join(f'<stop offset="{i / (len(colors) - 1):.3f}" stop-color="{c}"/>' for i, c in enumerate(colors))
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{stops}{anim or ""}</linearGradient>'


def glow(fid, std=6, alpha=0.9):
    return (f'<filter id="{fid}" x="-30%" y="-60%" width="160%" height="220%">'
            f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feComponentTransfer in="b" result="b2"><feFuncA type="linear" slope="{alpha}"/></feComponentTransfer>'
            '<feMerge><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def pixels(art, x, y, s, extra=""):
    """Пиксель-арт из строк: каждый символ — цвет из PIX, точка — пусто."""
    out = []
    for r, row in enumerate(art):
        for c, ch in enumerate(row):
            if ch in PIX:
                out.append(f'<rect x="{x + c * s:.1f}" y="{y + r * s:.1f}" width="{s + 0.3:.1f}" height="{s + 0.3:.1f}" fill="{PIX[ch]}"/>')
    return f'<g{extra} shape-rendering="crispEdges">{"".join(out)}</g>'


def stars(n, w, h, seed=1, y0=0):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(y0, h)
        r = rnd.choice((0.7, 0.9, 1.1, 1.4, 1.8))
        d = rnd.uniform(2.5, 6)
        lo = rnd.uniform(0.15, 0.5)
        col = rnd.choice((C["text"], C["text"], C["lilac"], C["rose"]))
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}">'
                   f'<animate attributeName="opacity" values="1;{lo:.2f};1" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')
    return "\n".join(out)


def scanlines(w, h, pid="scan", op=0.035):
    return (f'<defs><pattern id="{pid}" width="4" height="4" patternUnits="userSpaceOnUse">'
            f'<rect width="4" height="1" fill="#000"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#{pid})" opacity="{op}" pointer-events="none"/>')


def card(w, h, rx=20, fill=None, stroke=True, gid="cardstroke"):
    """Фон карточки с тонкой градиентной рамкой."""
    out = [f'<defs>{lgrad(gid, [C["violet"], C["pink"], C["orange"]], 0, 0, 1, 1)}</defs>',
           f'<rect width="{w}" height="{h}" rx="{rx}" fill="{fill or C["bg"]}"/>']
    if stroke:
        out.append(f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx - 1}" fill="none" stroke="url(#{gid})" stroke-opacity="0.35" stroke-width="1.2"/>')
    return "\n".join(out)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n{body}\n</svg>\n')


def write(name, content):
    (ROOT / "assets" / f"{name}.svg").write_text(content)
