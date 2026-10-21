"""Общее для картинок профиля: две темы, шрифт-контуры, иконки.

Стиль — минимализм со стеклом: под каждой карточкой медленно плывут размытые цветные пятна,
сверху — полупрозрачное «матовое стекло» с бликом по краю и мягкой тенью.
Цвета — фирменная палитра Go с go.dev: Gopher Blue #00ADD8, Light Blue, Aqua, Fuchsia и Yellow.
Каждая картинка рисуется дважды, под тёмную и светлую тему GitHub; README выбирает через <picture>.
"""
import base64, json, random
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
ROOT = HERE.parent
GLYPHS = json.loads((HERE / "glyphs.json").read_text())
ICONS = json.loads((HERE / "icons.json").read_text())

MONO = "ui-monospace, 'Geist Mono', SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0a0a0a", panel="#0d1014", line="#1f262e", line2="#2b343e", dot="#1f2a33",
                 text="#eef3f6", soft="#c3ccd3", muted="#8a96a0", faint="#4f5b66",
                 accent="#00ADD8", green="#3fb950", str="#7ee0c8", kw="#ff7aa8",
                 go=["#00ADD8", "#5DC9E2", "#00A29C", "#CE3262", "#FDDD00"],
                 aurora=["#00ADD8", "#00A29C", "#CE3262", "#5DC9E2"], blob=0.5, glass="#ffffff", glass_op=0.035,
                 rim="#ffffff", rim_op=0.24, shadow=0.55),
    "light": dict(bg="#ffffff", panel="#f7fbfc", line="#dfe8ec", line2="#cbd8de", dot="#d9e6eb",
                  text="#0b1a22", soft="#2f414b", muted="#5e707b", faint="#a3b1b9",
                  accent="#007d9c", green="#1a7f37", str="#00796b", kw="#b0285a",
                  go=["#007d9c", "#00ADD8", "#00A29C", "#CE3262", "#c9a800"],
                  aurora=["#5DC9E2", "#6fd6cc", "#f3a1bd", "#fde56b"], blob=0.5, glass="#ffffff", glass_op=0.6,
                  rim="#ffffff", rim_op=0.9, shadow=0.12),
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


def glow(fid, std=6, alpha=0.9):
    """Мягкое свечение вокруг фигуры: размытая копия под оригиналом."""
    return (f'<filter id="{fid}" x="-30%" y="-60%" width="160%" height="220%">'
            f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feComponentTransfer in="b" result="b2"><feFuncA type="linear" slope="{alpha}"/></feComponentTransfer>'
            '<feMerge><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def blobs(w, h, t, seed=1, n=3, op=None, uid="b"):
    """Размытые цветные пятна, которые медленно плывут, — «северное сияние» под стеклом."""
    rnd = random.Random(seed)
    op = t["blob"] if op is None else op
    out = [f'<defs><filter id="{uid}f" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{max(w, h) * 0.07:.0f}"/></filter></defs>',
           f'<g filter="url(#{uid}f)" opacity="{op}">']
    for i in range(n):
        cx, cy = rnd.uniform(0.1, 0.9) * w, rnd.uniform(0.15, 0.85) * h
        rx, ry = rnd.uniform(0.18, 0.32) * w, rnd.uniform(0.35, 0.6) * h
        dx, dy = rnd.uniform(-0.12, 0.12) * w, rnd.uniform(-0.2, 0.2) * h
        d = rnd.uniform(16, 26)
        out.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{t["aurora"][(seed + i) % 4]}">'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx:.0f} {dy:.0f};0 0" dur="{d:.1f}s" repeatCount="indefinite" '
                   'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></ellipse>')
    out.append("</g>")
    return "".join(out)


def frame(w, h, t, rx=16, fill=None, seed=None, n=3, glow=True, uid="g"):
    """Стеклянная карточка: фон, пятна, полупрозрачное стекло, блик по верхнему краю."""
    seed = (w * 7 + h * 13) % 97 if seed is None else seed
    out = [f'<defs><clipPath id="{uid}c"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
           f'<linearGradient id="{uid}r" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="{t["rim"]}" stop-opacity="{t["rim_op"]}"/>'
           f'<stop offset="0.5" stop-color="{t["rim"]}" stop-opacity="0.04"/><stop offset="1" stop-color="{t["rim"]}" stop-opacity="{t["rim_op"] * 0.35:.2f}"/></linearGradient>'
           f'<linearGradient id="{uid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["glass"]}" stop-opacity="{t["glass_op"] * 1.6:.3f}"/>'
           f'<stop offset="1" stop-color="{t["glass"]}" stop-opacity="{t["glass_op"]}"/></linearGradient></defs>',
           f'<g clip-path="url(#{uid}c)"><rect width="{w}" height="{h}" fill="{fill or t["panel"]}"/>']
    if glow:
        out.append(blobs(w, h, t, seed=seed, n=n, uid=uid + "b"))
    out.append(f'<rect width="{w}" height="{h}" fill="url(#{uid}s)"/></g>')
    out.append(f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{rx - 0.75}" fill="none" stroke="{t["line"]}"/>')
    out.append(f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{rx - 0.75}" fill="none" stroke="url(#{uid}r)" stroke-width="1.2"/>')
    return "".join(out)


def gopher(name, x, y, h, extra=""):
    """Гофер Эгона Элбре (CC0) из assets/gophers, встроенный прямо в SVG."""
    path = ROOT / "assets" / "gophers" / f"{name}.png"
    raw = path.read_bytes()
    iw, ih = int.from_bytes(raw[16:20], "big"), int.from_bytes(raw[20:24], "big")   # ширина и высота из заголовка PNG
    w = h * iw / ih
    data = base64.b64encode(raw).decode()
    return f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="data:image/png;base64,{data}"{extra}/>', w


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n{body}\n</svg>\n')


def write(name, theme, content, folder=None):
    out = Path(folder) if folder else ROOT / "assets"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}{'' if theme == 'dark' else '-light'}.svg").write_text(content)
