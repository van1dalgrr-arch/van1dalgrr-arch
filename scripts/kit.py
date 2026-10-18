"""Общее для картинок профиля: две темы, шрифт-контуры, иконки.

Стиль — минимализм: почти чёрный (или белый) фон, текст, тонкие рамки и один сдержанный синий акцент.
Каждая картинка рисуется дважды, под тёмную и светлую тему GitHub; README выбирает через <picture>.
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
ROOT = HERE.parent
GLYPHS = json.loads((HERE / "glyphs.json").read_text())
ICONS = json.loads((HERE / "icons.json").read_text())

MONO = "ui-monospace, 'Geist Mono', SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0a0a0a", panel="#0f0f11", line="#222226", line2="#2e2e34", dot="#26262b",
                 text="#ededed", soft="#c4c4ca", muted="#8f8f97", faint="#55555d",
                 accent="#7aa2ff", green="#3fb950", str="#a5d6a7", kw="#c3a6ff"),
    "light": dict(bg="#ffffff", panel="#fafafa", line="#e6e6ea", line2="#d6d6dc", dot="#e3e3e8",
                  text="#111113", soft="#3a3a41", muted="#6c6c75", faint="#b0b0b8",
                  accent="#2f6bff", green="#1a7f37", str="#1f7a3a", kw="#7c3aed"),
}


def esc(s):
    return escape(str(s))


def tw(s, size, mono=False):
    """Ширина текста системным шрифтом — на глаз, для отступов."""
    return len(s) * size * (0.602 if mono else 0.54)


def gw(s, size, font="head", tracking=0):
    f = GLYPHS[font]
    k = size / f["upm"]
    return sum(f["g"].get(c, [f["upm"] * 0.5])[0] * k + tracking for c in s) - (tracking if s else 0)


def gt(s, x, y, size, fill, font="head", anchor="start", tracking=0, extra=""):
    """Текст из запечённых контуров Geist; y — базовая линия."""
    f = GLYPHS[font]
    k = size / f["upm"]
    x -= {"start": 0, "middle": gw(s, size, font, tracking) / 2, "end": gw(s, size, font, tracking)}[anchor]
    out = []
    for c in s:
        adv, d = f["g"].get(c, [f["upm"] * 0.5, ""])
        if d:
            out.append(f'<path transform="translate({x:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})" d="{d}"/>')
        x += adv * k + tracking
    return f'<g fill="{fill}"{extra}>{"".join(out)}</g>'


def icon(name, x, y, size, fill):
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({size / 24:.4f})" d="{ICONS[name]}" fill="{fill}"/>'


def arrow(x, y, size, color):
    """Стрелка ↗ — ссылка наружу."""
    s = size
    return (f'<path d="M{x} {y + s}L{x + s} {y}M{x + s * 0.3} {y}H{x + s}V{y + s * 0.7}" fill="none" stroke="{color}" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')


def frame(w, h, t, rx=16, fill=None):
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="{fill or t["bg"]}"/>'
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx - 0.5}" fill="none" stroke="{t["line"]}"/>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n{body}\n</svg>\n')


def write(name, theme, content, folder=None):
    out = Path(folder) if folder else ROOT / "assets"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}{'' if theme == 'dark' else '-light'}.svg").write_text(content)
