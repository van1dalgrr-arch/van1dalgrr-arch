"""Shared bits for the profile SVGs: themes, type, icons, sakura and a few drawing helpers.

Look: black and white ink with sakura pink as the only color.
Every asset is drawn twice, once per theme, so README can switch them with <picture>.
"""

import json
import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ICONS = json.loads((Path(__file__).parent / "icons.json").read_text())
GLYPHS = json.loads((Path(__file__).parent / "glyphs.json").read_text())

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg="#0a0a0b", panel="#111113", panel2="#18181b", border="#27272a",
        ink="#f5f3ef", text="#f5f3ef", muted="#8e8e96", faint="#3f3f46", ghost="#1c1c20",
        sakura="#ffb3c7", deep="#ff7aa2", pale="#ffe3ec", stamp="#0a0a0b",
        moon="#f2efe9", wood="#3a3a41", branch="#d4d4d8", glow=0.16,
    ),
    "light": dict(
        bg="#f8f6f1", panel="#ffffff", panel2="#f1eee8", border="#e4e0d8",
        ink="#0a0a0b", text="#0a0a0b", muted="#6b6b72", faint="#c9c5bd", ghost="#ece8e1",
        sakura="#f39bb5", deep="#e2557f", pale="#fde7ee", stamp="#ffffff",
        moon="#fbd5e0", wood="#1c1917", branch="#1c1917", glow=0.35,
    ),
}


def esc(s):
    return escape(str(s))


def text_w(s, size, mono=False):
    """Rough width of system-font text, for sizing chips without a font engine."""
    if mono:
        return len(s) * size * 0.602
    w = 0.0
    for ch in s:
        if ch in "il.,:;|!'·":
            w += 0.28
        elif ch in "mwMW":
            w += 0.86
        elif ch.isupper():
            w += 0.66
        elif ch == " ":
            w += 0.28
        else:
            w += 0.55
    return w * size


# ───────────────────────── display type (Noto Serif JP as paths) ─────────────────────────

def gwidth(s, size, weight=700, tracking=0):
    g = GLYPHS["weights"][str(weight)]
    k = size / GLYPHS["upm"]
    return sum((g[c][0] if c in g else 500) * k + tracking for c in s) - (tracking if s else 0)


def gtext(s, x, y, size, fill, weight=700, anchor="start", tracking=0, extra=""):
    """Headline text drawn from baked glyph outlines. y is the baseline."""
    g = GLYPHS["weights"][str(weight)]
    k = size / GLYPHS["upm"]
    w = gwidth(s, size, weight, tracking)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    out, cx = [], x
    for c in s:
        adv, d = g.get(c, (500, ""))
        if d:
            out.append(f'<path transform="translate({cx:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})" d="{d}"/>')
        cx += adv * k + tracking
    return f'<g fill="{fill}"{extra}>{"".join(out)}</g>'


def vtext(s, x, y, size, fill, weight=700, gap=0.12, extra=""):
    """Vertical Japanese text, top to bottom; x is the column's center, y its top."""
    out = []
    for i, c in enumerate(s):
        out.append(gtext(c, x, y + size * 0.88 + i * size * (1 + gap), size, fill, weight, anchor="middle"))
    return f'<g{extra}>{"".join(out)}</g>'


# ─────────────────────────────────── icons ───────────────────────────────────

def icon(name, x, y, size, fill, opacity=1):
    s = size / 24
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" '
            f'd="{ICONS[name]}" fill="{fill}"{op}/>')


# ─────────────────────────────────── sakura ───────────────────────────────────

# One petal with the notch at its tip, pointing up from the origin.
PETAL = "M0 0C-5 -3 -7 -9 -5 -14C-4 -17 -2 -18 -1 -18L0 -15.5L1 -18C2 -18 4 -17 5 -14C7 -9 5 -3 0 0Z"


def blossom(cx, cy, r, t, rot=0, open_=1.0, extra=""):
    """Five-petal flower. r is the petal length; open_ < 1 draws a half-open bud."""
    k = r / 18
    petals = []
    for i in range(5):
        a = rot + i * 72
        petals.append(f'<path d="{PETAL}" transform="rotate({a:.1f}) scale({k * open_:.3f} {k:.3f})" '
                      f'fill="{t["sakura"]}" stroke="{t["deep"]}" stroke-width="{0.6 / k:.2f}" stroke-opacity="0.5"/>')
    center = (f'<circle r="{r*0.2:.1f}" fill="{t["deep"]}"/>'
              + "".join(f'<circle cx="{math.cos(math.radians(rot + 36 + i*72)) * r*0.38:.1f}" '
                        f'cy="{math.sin(math.radians(rot + 36 + i*72)) * r*0.38:.1f}" r="{r*0.06:.1f}" fill="{t["deep"]}"/>'
                        for i in range(5)))
    return f'<g transform="translate({cx:.1f} {cy:.1f})"{extra}>{"".join(petals)}{center}</g>'


def bud(cx, cy, r, t, rot=0):
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot})">'
            f'<ellipse cx="0" cy="{-r*0.6:.1f}" rx="{r*0.45:.1f}" ry="{r*0.75:.1f}" fill="{t["sakura"]}" stroke="{t["deep"]}" stroke-width="0.8"/>'
            f'<path d="M0 0L{-r*0.35:.1f} {-r*0.35:.1f}M0 0L{r*0.35:.1f} {-r*0.35:.1f}" stroke="{t["wood"]}" stroke-width="1.4"/></g>')


def petals(n, w, h, t, seed=1, x_range=None, y0=-30, dur=(9, 16), size=(0.45, 0.8), drift=160):
    """Petals falling with a sway and a spin; negative begin times spread them out from frame one."""
    rnd = random.Random(seed)
    x_lo, x_hi = x_range or (0, w)
    out = []
    for _ in range(n):
        x = rnd.uniform(x_lo, x_hi)
        d = rnd.uniform(*dur)
        s = rnd.uniform(*size)
        sway = rnd.uniform(30, 70)
        dx = -rnd.uniform(drift * 0.4, drift)
        path = (f"M{x:.0f} {y0}C{x + sway:.0f} {h*0.3:.0f} {x - sway + dx*0.5:.0f} {h*0.6:.0f} {x + dx:.0f} {h + 30:.0f}")
        spin = rnd.choice((360, -360))
        op = rnd.uniform(0.55, 0.95)
        out.append(
            f'<g opacity="{op:.2f}"><animateMotion path="{path}" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
            f'<path d="{PETAL}" fill="{t["sakura"]}" transform="scale({s:.2f})">'
            f'<animateTransform attributeName="transform" type="rotate" from="0" to="{spin}" dur="{rnd.uniform(3, 6):.1f}s" '
            f'repeatCount="indefinite" additive="sum"/></path></g>')
    return "\n".join(out)


def brush(x, y, w, h, color, seed=3, draw=True, uid="b"):
    """A dry-brush stroke: a ragged ribbon, optionally painted on from left to right."""
    rnd = random.Random(seed)
    top, bot = [], []
    n = 18
    for i in range(n + 1):
        px = x + w * i / n
        taper = math.sin(math.pi * min(1, (i + 1.5) / (n + 1))) ** 0.5
        top.append(f"{px:.1f} {y - h/2 * taper + rnd.uniform(-1.2, 1.2):.1f}")
        bot.append(f"{px:.1f} {y + h/2 * taper + rnd.uniform(-1.2, 1.2):.1f}")
    d = "M" + " L".join(top) + " L" + " L".join(reversed(bot)) + "Z"
    if not draw:
        return f'<path d="{d}" fill="{color}"/>'
    return (f'<clipPath id="{uid}"><rect x="{x}" y="{y-h}" width="0" height="{h*2}">'
            f'<animate attributeName="width" from="0" to="{w}" dur="0.9s" begin="0.2s" fill="freeze" calcMode="spline" '
            f'keyTimes="0;1" keySplines="0.3 0 0.2 1"/></rect></clipPath>'
            f'<path d="{d}" fill="{color}" clip-path="url(#{uid})"/>')


def hanko(cx, cy, size, chars, t, rot=-4):
    """Red-seal style stamp, pink here, with the characters in a vertical column."""
    fs = size * (0.36 if len(chars) > 1 else 0.6)
    col = vtext(chars, 0, -size/2 + size*0.08 if len(chars) > 1 else -fs*0.55, fs, t["stamp"], weight=900, gap=0.02)
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot})">'
            f'<rect x="{-size/2}" y="{-size/2}" width="{size}" height="{size}" rx="{size*0.12:.1f}" fill="{t["deep"]}"/>'
            f'<rect x="{-size/2 + 3}" y="{-size/2 + 3}" width="{size - 6}" height="{size - 6}" rx="{size*0.09:.1f}" fill="none" stroke="{t["stamp"]}" stroke-width="1.2" opacity="0.7"/>'
            f'{col}</g>')


# ─────────────────────────────────── frame ───────────────────────────────────

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n{body}\n</svg>\n')


def paper(w, h, t, rx=18, border=True, fill=None):
    out = f'<rect width="{w}" height="{h}" rx="{rx}" fill="{fill or t["bg"]}"/>'
    if border:
        out += f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx-0.5}" fill="none" stroke="{t["border"]}"/>'
    return out


def chip(x, y, label, t, size=12, dashed=False, h=26, pink=False):
    """Outlined pill with mono text; returns (svg, width)."""
    w = text_w(label, size, mono=True) + 22
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    stroke = t["deep"] if pink else t["faint"]
    color = t["deep"] if pink else t["text"]
    s = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="none" stroke="{stroke}"{dash}/>'
         f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" font-family="{MONO}" '
         f'font-size="{size}" fill="{color}">{esc(label)}</text>')
    return s, w


def write(name, theme, content):
    suffix = "" if theme == "dark" else "-light"
    path = ROOT / "assets" / f"{name}{suffix}.svg"
    path.write_text(content)
    return path
