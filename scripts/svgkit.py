"""Shared bits for the profile SVGs: themes, fonts, icons and a few drawing helpers.

Every asset is drawn twice, once per theme, so README can switch them with <picture>.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ICONS = json.loads((Path(__file__).parent / "icons.json").read_text())

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg="#0d1117", panel="#161b22", panel2="#1c2128", border="#30363d", grid="#161b22",
        text="#e6edf3", muted="#7d8590", faint="#484f58",
        purple="#a855f7", cyan="#00ADD8", green="#3fb950", yellow="#eab308", red="#f85149",
        glow=0.55, chip="#21262d",
    ),
    "light": dict(
        bg="#ffffff", panel="#f6f8fa", panel2="#eef1f4", border="#d0d7de", grid="#f0f2f5",
        text="#1f2328", muted="#656d76", faint="#afb8c1",
        purple="#7c3aed", cyan="#0089ad", green="#1a7f37", yellow="#9a6700", red="#cf222e",
        glow=0.22, chip="#eaeef2",
    ),
}

# Brand colors for the icons. A few are too dark for the dark theme, so they get a lighter twin.
BRAND = {
    "go": ("#00ADD8", "#00ADD8"), "gin": ("#00ADD8", "#008ecf"), "postgresql": ("#6b9bd8", "#336791"),
    "docker": ("#2496ED", "#1d7fd0"), "git": ("#F05032", "#e0401f"), "gnubash": ("#a6e3a1", "#2f7a2b"),
    "zsh": ("#f5a97f", "#c25e1d"), "githubactions": ("#2088FF", "#1a6fd6"), "telegram": ("#26A5E4", "#1c8bc4"),
    "kubernetes": ("#4f8ef7", "#326CE5"), "helm": ("#7ea7ff", "#0F1689"), "opentofu": ("#FFDA18", "#b59700"),
    "yandexcloud": ("#5282FF", "#3d6be0"), "openrouter": ("#a3aab4", "#4b5563"), "prometheus": ("#E6522C", "#c9411d"),
    "grafana": ("#F46800", "#d35a00"), "swift": ("#F05138", "#d63f27"), "apple": ("#e6edf3", "#1f2328"),
    "zedindustries": ("#7aa2f7", "#084ccf"), "ghostty": ("#c4b5fd", "#6d28d9"), "goland": ("#c084fc", "#7c3aed"),
    "github": ("#e6edf3", "#1f2328"), "gmail": ("#EA4335", "#d93025"),
}


def brand(name, theme):
    dark, light = BRAND[name]
    return dark if theme == "dark" else light


def esc(s):
    return escape(str(s))


def text_w(s, size, mono=False, bold=False):
    """Rough text width; good enough to size chips without a font engine."""
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
    return w * size * (1.05 if bold else 1.0)


def icon(name, x, y, size, fill, opacity=1):
    s = size / 24
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" '
            f'd="{ICONS[name]}" fill="{fill}"{op}/>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n{body}\n</svg>\n')


def frame(w, h, t, rx=16, grid=True, glows=((0.88, 0.9, 0.6, "purple"), (0.05, 0.0, 0.45, "cyan")), uid="f"):
    """Card background: fill, faint grid, two soft color glows, hairline border."""
    out = ["<defs>"]
    for i, (cx, cy, r, c) in enumerate(glows):
        out.append(f'<radialGradient id="{uid}g{i}" cx="{cx}" cy="{cy}" r="{r}">'
                   f'<stop offset="0" stop-color="{t[c]}" stop-opacity="{t["glow"]}"/>'
                   f'<stop offset="1" stop-color="{t[c]}" stop-opacity="0"/></radialGradient>')
    out.append(f'<pattern id="{uid}grid" width="32" height="32" patternUnits="userSpaceOnUse">'
               f'<path d="M32 0H0V32" fill="none" stroke="{t["grid"]}" stroke-width="1"/></pattern>')
    out.append(f'<clipPath id="{uid}clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    out.append("</defs>")
    out.append(f'<rect width="{w}" height="{h}" rx="{rx}" fill="{t["bg"]}"/>')
    if grid:
        out.append(f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#{uid}grid)"/>')
    for i in range(len(glows)):
        out.append(f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#{uid}g{i})"/>')
    out.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx-0.5}" fill="none" stroke="{t["border"]}"/>')
    return "\n".join(out)


def chip(x, y, label, t, size=13, mono=True, color=None, dashed=False, h=26):
    """Rounded pill with text; returns (svg, width)."""
    w = text_w(label, size, mono=mono) + 22
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    stroke = color or t["border"]
    fam = MONO if mono else SANS
    s = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{t["chip"]}" '
         f'stroke="{stroke}" stroke-opacity="0.9"{dash}/>'
         f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" font-family="{fam}" '
         f'font-size="{size}" fill="{t["text"] if not dashed else t["muted"]}">{esc(label)}</text>')
    return s, w


def write(name, theme, content):
    suffix = "" if theme == "dark" else "-light"
    path = ROOT / "assets" / f"{name}{suffix}.svg"
    path.write_text(content)
    return path
