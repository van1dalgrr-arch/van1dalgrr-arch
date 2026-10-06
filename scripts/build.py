"""Draws every static SVG of the profile README into assets/, dark and light.

    python3 scripts/build.py

Content lives here as plain data (PROFILE, PROJECTS, STACK, ROADMAP, SECTIONS...), so updating
the profile means editing a list and re-running the script. Live numbers come from stats.py.
New characters in a headline need scripts/glyphs.py first.
"""

import math
import random

from svgkit import (MONO, SANS, THEMES, blossom, brush, bud, chip, esc, gtext, gwidth, hanko, icon,
                    paper, petals, svg, text_w, vtext, write)

W = 1200


def wrap(s, size, width):
    lines, cur = [], ""
    for word in s.split():
        nxt = f"{cur} {word}".strip()
        if text_w(nxt, size) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = nxt
    return lines + [cur]


def stroke_path(d, width, color, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{extra}/>'


def flowers(items, t):
    """(x, y, r, rot) list; a negative r draws a closed bud instead of a blossom."""
    return "".join(bud(x, y, -r, t, rot) if r < 0 else blossom(x, y, r, t, rot) for x, y, r, rot in items)


# ─────────────────────────────────── hero ───────────────────────────────────

# A cherry branch reaching in from the top right: (path, width).
HERO_BRANCH = [
    ("M1230 58C1150 70 1080 96 1010 132", 15),
    ("M1010 132C950 162 890 178 830 172", 10),
    ("M830 172C780 166 735 172 690 196", 6),
    ("M690 196C665 210 645 228 630 250", 3),
    ("M1010 132C1000 185 980 230 945 268", 7),
    ("M945 268C930 284 912 298 892 306", 3.5),
    ("M1100 92C1092 55 1075 30 1048 8", 6),
    ("M870 176C850 140 840 112 818 90", 4.5),
    ("M760 168C745 200 735 222 712 240", 3),
    ("M1160 70C1170 130 1160 180 1140 222", 6),
    ("M1140 222C1132 240 1120 252 1104 262", 3),
    ("M940 160C925 128 920 100 930 70", 3.5),
]
HERO_FLOWERS = [
    (1048, 10, 15, 10), (1062, 34, 11, 40), (1020, 118, 13, 20), (990, 150, 16, 5), (958, 200, 14, 30),
    (945, 262, 17, 12), (905, 300, 12, 50), (880, 312, -9, 20), (870, 180, 15, 0), (842, 170, 12, 22),
    (818, 92, 16, 15), (836, 118, -8, -20), (930, 70, 14, 33), (925, 100, -8, 10), (760, 172, 13, 18),
    (712, 240, 15, 8), (735, 222, -8, 30), (690, 196, 14, 40), (650, 228, 11, 15), (630, 252, 13, 0),
    (1140, 220, 15, 25), (1104, 262, 13, 8), (1165, 140, 12, 50), (1180, 100, -9, -15), (1100, 92, 14, 30),
    (800, 160, -7, 40), (1080, 110, -8, 60), (965, 240, -7, -25),
]


def hero(theme):
    t = THEMES[theme]
    H = 540
    o = ["<defs>",
         f'<radialGradient id="mg" cx="0.5" cy="0.5" r="0.5"><stop offset="0.55" stop-color="{t["moon"]}" stop-opacity="{t["glow"]}"/>'
         f'<stop offset="1" stop-color="{t["moon"]}" stop-opacity="0"/></radialGradient>',
         f'<clipPath id="hc"><rect width="{W}" height="{H}" rx="18"/></clipPath>',
         "</defs>",
         paper(W, H, t),
         '<g clip-path="url(#hc)">']
    # faint vertical rules, like a page of vertical writing
    for x in range(60, W, 120):
        o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{t["ghost"]}"/>')
    o.append(f'<circle cx="900" cy="230" r="270" fill="url(#mg)"/>')
    o.append(f'<circle cx="900" cy="230" r="178" fill="{t["moon"]}"/>')
    # the branch sways a little around its root
    o.append('<g><animateTransform attributeName="transform" type="rotate" values="0 1230 58;-0.8 1230 58;0 1230 58" '
             'dur="7s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>')
    for d, w in HERO_BRANCH:
        o.append(stroke_path(d, w, t["wood"]))
    o.append(flowers(HERO_FLOWERS, t))
    o.append("</g>")
    o.append(petals(26, W, H, t, seed=4, x_range=(420, 1250)))
    o.append("</g>")

    # "backend developer" written down the left margin
    o.append(vtext("バックエンド開発者", 58, 70, 19, t["muted"], weight=400, gap=0.18))
    o.append(f'<line x1="58" y1="300" x2="58" y2="470" stroke="{t["faint"]}"/>')

    o.append(gtext("ヴァンダル", 118, 150, 28, t["deep"], weight=700, tracking=10))
    o.append(gtext("van1dal", 110, 290, 138, t["ink"], weight=900, tracking=-4))
    nw = gwidth("van1dal", 138, 900, -4)
    o.append(hanko(110 + nw + 52, 212, 62, "夜桜", t, rot=-6))
    o.append(brush(116, 322, 330, 12, t["sakura"], seed=11, draw=False))
    o.append(gtext("Go backend developer,", 116, 380, 34, t["ink"], weight=400))
    o.append(gtext("on the way to DevOps.", 116, 424, 34, t["ink"], weight=400))
    o.append(f'<text x="118" y="466" font-family="{MONO}" font-size="15" fill="{t["muted"]}">'
             f'gin · postgresql · docker · ci  <tspan fill="{t["deep"]}">→</tspan>  kubernetes</text>')

    # magazine-style index along the bottom
    o.append(f'<line x1="110" y1="{H-44}" x2="{W-40}" y2="{H-44}" stroke="{t["border"]}"/>')
    idx = ["01 about", "02 now", "03 projects", "04 stack", "05 ci", "06 desk", "07 stats", "08 contact"]
    for i, s in enumerate(idx):
        o.append(f'<text x="{110 + i * 132}" y="{H-20}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">'
                 f'<tspan fill="{t["deep"]}">{s[:2]}</tspan>{esc(s[2:])}</text>')
    return svg(W, H, "\n".join(o), "van1dal — Go backend developer on the way to DevOps")


# ─────────────────────────────── section headers ───────────────────────────────

SECTIONS = {
    "about": ("01", "About", "人物"),
    "now": ("02", "Right now", "今"),
    "projects": ("03", "Projects", "作品"),
    "stack": ("04", "Stack", "技"),
    "ci": ("05", "How code ships", "流"),
    "desk": ("06", "Where I work", "環境"),
    "stats": ("07", "Stats", "統計"),
    "contact": ("08", "Contact", "連絡"),
}


def header(key, theme):
    t = THEMES[theme]
    num, title, kanji = SECTIONS[key]
    H = 120
    o = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}" rx="18"/>']
    o.append(gtext(kanji, W - 30, 112, 118, t["ghost"], weight=900, anchor="end"))
    o.append(f'<text x="24" y="44" font-family="{MONO}" font-size="15" fill="{t["deep"]}" letter-spacing="2">{num}</text>')
    o.append(f'<line x1="56" y1="39" x2="120" y2="39" stroke="{t["faint"]}"/>')
    tw = gwidth(title, 46, 700)
    o.append(brush(18, 104, tw + 40, 10, t["sakura"], seed=len(title) * 7, draw=False))
    o.append(gtext(title, 24, 96, 46, t["ink"], weight=700))
    o.append(gtext(kanji, 24 + tw + 22, 94, 30, t["deep"], weight=700, tracking=4))
    o.append(blossom(24 + tw + 22 + gwidth(kanji, 30, 700, 4) + 26, 82, 11, t, rot=15))
    return svg(W, H, "\n".join(o), f"{num} {title}")


# ─────────────────────────────── about: character sheet ───────────────────────────────

PROFILE = [
    ("class", "Backend developer, Go"),
    ("path", "Backend → DevOps"),
    ("main quest", "Kubernetes on a local cluster"),
    ("side quest", "logsence: tests + image built by CI"),
    ("base", "MacBook Air, 8 GB RAM"),
    ("speaks", "English, Russian"),
]
INVENTORY = [("go", "Go"), ("gin", "Gin"), ("postgresql", "Postgres"), ("docker", "Docker"),
             ("git", "Git"), ("githubactions", "Actions"), ("kubernetes", "k8s"), ("helm", "Helm")]
TRAINING = {"kubernetes", "helm"}


def cat(t, dark, cx, base):
    """Black cat on the sill, seen against the moon. The tail swishes, the eyes blink."""
    ink = "#0a0a0b" if dark else t["ink"]
    o = [f'<g fill="{ink}">',
         f'<path d="M{cx+38} {base-6}C{cx+88} {base-4} {cx+100} {base-46} {cx+80} {base-78}" fill="none" stroke="{ink}" stroke-width="11" stroke-linecap="round">'
         f'<animateTransform attributeName="transform" type="rotate" values="0 {cx+38} {base-6};-9 {cx+38} {base-6};0 {cx+38} {base-6}" dur="3.2s" repeatCount="indefinite" '
         'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/></path>',
         f'<path d="M{cx-46} {base}C{cx-58} {base-60} {cx-40} {base-108} {cx} {base-112}C{cx+40} {base-108} {cx+58} {base-60} {cx+46} {base}Z"/>',
         f'<circle cx="{cx}" cy="{base-128}" r="36"/>',
         f'<path d="M{cx-33} {base-140}L{cx-30} {base-182}L{cx-6} {base-160}Z"/>',
         f'<path d="M{cx+33} {base-140}L{cx+30} {base-182}L{cx+6} {base-160}Z"/>',
         "</g>"]
    for ex in (cx - 13, cx + 13):
        o.append(f'<ellipse cx="{ex}" cy="{base-130}" rx="5" ry="6.5" fill="{t["sakura"]}">'
                 '<animate attributeName="ry" values="6.5;6.5;0.6;6.5;6.5" keyTimes="0;0.9;0.93;0.96;1" dur="4.5s" repeatCount="indefinite"/></ellipse>')
    o.append(f'<path d="M{cx-24} {base-100}Q{cx} {base-88} {cx+24} {base-100}" fill="none" stroke="{t["deep"]}" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<circle cx="{cx}" cy="{base-89}" r="5" fill="{t["sakura"]}"/>')
    return "\n".join(o)


def about(theme):
    t = THEMES[theme]
    H = 480
    o = [paper(W, H, t)]
    px, py, pw, ph = 30, 30, 360, 420
    o.append(f'<clipPath id="win"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14"/></clipPath>')
    o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>')
    o.append('<g clip-path="url(#win)">')
    o.append(f'<circle cx="{px+pw/2}" cy="{py+190}" r="122" fill="{t["moon"]}"/>')
    o.append(stroke_path(f"M{px+pw+10} {py+40}C{px+290} {py+60} {px+250} {py+70} {px+210} {py+52}", 6, t["wood"]))
    o.append(stroke_path(f"M{px+290} {py+52}C{px+300} {py+90} {px+296} {py+110} {px+280} {py+130}", 3, t["wood"]))
    o.append(flowers([(px+210, py+52, 13, 10), (px+250, py+68, 11, 40), (px+282, py+128, 12, 5), (px+320, py+44, 14, 22), (px+296, py+96, -7, 30)], t))
    o.append(cat(t, theme == "dark", px + pw/2 - 20, py + 350))
    o.append(f'<rect x="{px}" y="{py+350}" width="{pw}" height="70" fill="{t["panel2"]}"/>')
    o.append(f'<line x1="{px}" y1="{py+350}" x2="{px+pw}" y2="{py+350}" stroke="{t["faint"]}" stroke-width="2"/>')
    o.append(petals(8, pw, ph, t, seed=9, x_range=(px + 60, px + pw + 60), dur=(8, 13), size=(0.4, 0.6), drift=120))
    o.append("</g>")
    o.append(gtext("猫", px + 18, py + ph - 16, 16, t["deep"], weight=700))
    o.append(f'<text x="{px+40}" y="{py+ph-18}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">night shift</text>')

    sx = 440
    o.append(f'<text x="{sx}" y="66" font-family="{MONO}" font-size="13" fill="{t["deep"]}" letter-spacing="2">CHARACTER</text>')
    o.append(gtext("van1dal", sx, 120, 52, t["ink"], weight=900))
    o.append(gtext("ヴァンダル", sx + gwidth("van1dal", 52, 900) + 18, 116, 20, t["deep"], weight=700, tracking=4))
    y = 176
    for k, v in PROFILE:
        o.append(f'<text x="{sx}" y="{y}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{esc(k)}</text>')
        o.append(f'<line x1="{sx + 96}" y1="{y-4}" x2="{sx + 120}" y2="{y-4}" stroke="{t["faint"]}" stroke-dasharray="2 3"/>')
        o.append(f'<text x="{sx + 130}" y="{y}" font-family="{SANS}" font-size="16" fill="{t["text"]}">{esc(v)}</text>')
        y += 32
    o.append(f'<text x="{sx}" y="{y + 18}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">inventory</text>')
    for i, (ic, label) in enumerate(INVENTORY):
        x = sx + i * 88
        sy = y + 32
        tr = ic in TRAINING
        dash = ' stroke-dasharray="4 3"' if tr else ""
        o.append(f'<rect x="{x}" y="{sy}" width="76" height="76" rx="12" fill="{t["panel"]}" stroke="{t["deep"] if tr else t["border"]}"{dash}/>')
        o.append(icon(ic, x + 24, sy + 14, 28, t["deep"] if tr else t["ink"]))
        o.append(f'<text x="{x + 38}" y="{sy + 63}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["muted"]}">{esc(label)}</text>')
    o.append(f'<text x="{sx + 7*88 + 76}" y="{y + 18}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["deep"]}">┄ in training</text>')
    return svg(W, H, "\n".join(o), "About: backend developer in Go, moving to DevOps; main quest Kubernetes")


# ─────────────────────────────── roadmap as a branch ───────────────────────────────

ROADMAP = [
    ("Go + SQL", "Gin, pgx, migrations", "done"),
    ("Docker", "multi-stage, Compose", "done"),
    ("CI", "Actions, linters, vuln", "done"),
    ("Kubernetes", "kind, kubectl, k9s", "now"),
    ("Helm", "charts for my APIs", "next"),
    ("OpenTofu", "infra as code", "next"),
    ("Cloud", "Yandex Cloud deploys", "next"),
    ("Observability", "Prometheus, Grafana", "next"),
]


def roadmap(theme):
    t = THEMES[theme]
    H = 300
    o = [paper(W, H, t)]
    n = len(ROADMAP)
    xs = [110 + i * (980 / (n - 1)) for i in range(n)]

    def by(x):  # the branch waves gently
        return 140 + 14 * math.sin(x / 150)

    pts = " ".join(f"L{x:.0f} {by(x):.1f}" for x in range(30, 1171, 10))
    o.append(stroke_path("M" + pts[1:], 9, t["branch"], ' stroke-linejoin="round"'))
    rnd = random.Random(5)
    for x in range(70, 1150, 70):
        up = rnd.choice((-1, 1))
        o.append(stroke_path(f"M{x} {by(x):.1f}q12 {up*-6} 22 {up*-26}", 2.5, t["branch"]))
    o.append(gtext("道", 30, 46, 20, t["deep"], weight=900))
    o.append(f'<text x="58" y="42" font-family="{MONO}" font-size="13" fill="{t["muted"]}">the road: backend → DevOps   '
             f'<tspan fill="{t["faint"]}">bloomed · blooming · buds</tspan></text>')
    now = next(i for i, r in enumerate(ROADMAP) if r[2] == "now")
    for i, (name, sub, state) in enumerate(ROADMAP):
        x, y = xs[i], by(xs[i])
        if state == "done":
            o.append(blossom(x, y, 22, t, rot=i * 17))
        elif state == "now":
            o.append(f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{t["deep"]}" stroke-width="1.5">'
                     '<animate attributeName="r" values="24;42" dur="2s" repeatCount="indefinite"/>'
                     '<animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/></circle>')
            o.append(blossom(x, y, 20, t, rot=8, open_=0.6))
            o.append(hanko(x, y - 64, 36, "今", t, rot=-5))
        else:
            o.append(bud(x, y, 13, t, rot=(-1) ** i * 12))
        col = t["text"] if state != "next" else t["muted"]
        o.append(f'<text x="{x}" y="{y + 58}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{col}">{esc(name)}</text>')
        o.append(f'<text x="{x}" y="{y + 79}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{t["muted"]}">{esc(sub)}</text>')
    o.append(petals(10, W, H, t, seed=21, x_range=(80, xs[now] + 60), dur=(7, 12), size=(0.4, 0.65), drift=90))
    return svg(W, H, "\n".join(o), "Roadmap: Go + SQL, Docker and CI done; Kubernetes now; next Helm, OpenTofu, Yandex Cloud, observability")


# ─────────────────────────────────── projects ───────────────────────────────────

PROJECTS = [
    dict(slug="logsence", repo="logsence", kanji="記録", status="進行中 · building now",
         desc="Log collection service: ingest logs over HTTP, keep them in PostgreSQL, query them by service.",
         chips=["Gin", "pgx + sqlx", "migrations", "Docker", "CI"]),
    dict(slug="ordergo", repo="OrderGo", kanji="注文",
         desc="REST API for orders, grown step by step toward a production layout: cmd/ + internal/, config, health.",
         chips=["Gin", "PostgreSQL", "Compose", "Makefile"]),
    dict(slug="watchdog", repo="watchdog", kanji="番犬",
         desc="Uptime monitor: polls a service's /health every 5 seconds and tells you the moment it stops answering.",
         chips=["net/http", "no framework", "Docker"]),
    dict(slug="pulse", repo="Pulse", kanji="鼓動",
         desc="A small HTTP framework for Go: its own Context, routing for every verb and a middleware chain on top of Gin.",
         chips=["Context", "routing", "middleware"]),
    dict(slug="mini-deploy", repo="MINI-deploy", kanji="配備",
         desc="Deployment API for DevOps practice: takes deploy requests, tracks them, exposes a health check.",
         chips=["Gin", "health check"], todo=["CI/CD", "Yandex Cloud"]),
    dict(slug="nexa", repo="NEXA-AI-BOT", title="NEXA AI", kanji="対話", icon2="telegram",
         desc="Telegram bot that talks to an LLM through the OpenRouter API: /start, /help, /about and free chat.",
         chips=["Telegram Bot API", "OpenRouter"]),
]


def card(i, p, theme):
    t = THEMES[theme]
    w, h = 590, 270
    title = p.get("title", p["repo"])
    o = [paper(w, h, t, fill=t["panel"])]
    o.append(f'<clipPath id="cc"><rect width="{w}" height="{h}" rx="18"/></clipPath>')
    o.append(f'<g clip-path="url(#cc)">{gtext(p["kanji"], w + 10, h + 26, 150, t["ghost"], weight=900, anchor="end")}</g>')
    o.append(f'<text x="30" y="46" font-family="{MONO}" font-size="13" fill="{t["deep"]}" letter-spacing="2">{i+1:02d}</text>')
    o.append(f'<line x1="58" y1="41" x2="96" y2="41" stroke="{t["faint"]}"/>')
    o.append(f'<text x="106" y="46" font-family="{MONO}" font-size="13" fill="{t["muted"]}">van1dalgrr-arch</text>')
    o.append(gtext(title, 28, 98, 38, t["ink"], weight=700))
    o.append(hanko(w - 54, 58, 52, p["kanji"], t, rot=5 if i % 2 else -5))
    if p.get("status"):
        sx = 30 + gwidth(title, 38, 700) + 20
        o.append(f'<circle cx="{sx + 5}" cy="86" r="4.5" fill="{t["deep"]}"><animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/></circle>')
        o.append(f'<text x="{sx + 16}" y="91" font-family="{MONO}" font-size="12" fill="{t["deep"]}">{esc(p["status"])}</text>')
    y = 134
    for line in wrap(p["desc"], 15.5, w - 70)[:3]:
        o.append(f'<text x="30" y="{y}" font-family="{SANS}" font-size="15.5" fill="{t["muted"]}">{esc(line)}</text>')
        y += 24
    x = 30
    for c in p["chips"]:
        s, cw = chip(x, h - 74, c, t)
        o.append(s)
        x += cw + 8
    for c in p.get("todo", []):
        s, cw = chip(x, h - 74, "next: " + c, t, dashed=True, pink=True)
        o.append(s)
        x += cw + 8
    o.append(f'<line x1="30" y1="{h-34}" x2="{w-30}" y2="{h-34}" stroke="{t["border"]}"/>')
    o.append(icon("go", 30, h - 27, 18, t["ink"]))
    if p.get("icon2"):
        o.append(icon(p["icon2"], 56, h - 27, 18, t["ink"]))
    o.append(f'<text x="{w-30}" y="{h-13}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">open repo <tspan fill="{t["deep"]}">→</tspan></text>')
    return svg(w, h, "\n".join(o), f"{title}: {p['desc']}")


# ─────────────────────────────────── stack ───────────────────────────────────

STACK = [
    ("毎日", "every day", [("go", "Go"), ("gin", "Gin"), ("postgresql", "PostgreSQL"), ("docker", "Docker"), ("git", "Git"), ("zsh", "zsh · bash")],
     ["REST APIs", "SQL", "Compose", "Makefiles"]),
    ("実戦", "in my projects", [("githubactions", "Actions"), ("go", "golangci-lint"), ("telegram", "Telegram API"), ("openrouter", "LLM APIs")],
     ["migrations", "govulncheck", "hadolint", "gitleaks"]),
    ("修行", "in training", [("kubernetes", "Kubernetes"), ("helm", "Helm"), ("opentofu", "OpenTofu"), ("yandexcloud", "Yandex Cloud")],
     ["kind", "OrbStack", "k9s", "observability"]),
]


def stack(theme):
    t = THEMES[theme]
    H = 460
    o = [paper(W, H, t)]
    for r, (kanji, label, items, extra) in enumerate(STACK):
        y = 30 + r * 145
        tr = r == 2
        if r:
            o.append(f'<line x1="30" y1="{y - 10}" x2="{W-30}" y2="{y - 10}" stroke="{t["border"]}" stroke-dasharray="2 6"/>')
        o.append(vtext(kanji, 60, y + 4, 38, t["deep"] if tr else t["ink"], weight=900, gap=0.04))
        o.append(f'<text x="104" y="{y + 26}" font-family="{MONO}" font-size="13" fill="{t["deep"] if tr else t["text"]}" letter-spacing="1">{esc(label)}</text>')
        for j, e in enumerate(extra):
            o.append(f'<text x="104" y="{y + 50 + j*18}" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">· {esc(e)}</text>')
        for j, (ic, name) in enumerate(items):
            cx, cy = 330 + j * 140, y + 50
            if tr:
                o.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="none" stroke="{t["deep"]}" stroke-width="1.5" stroke-dasharray="5 6">'
                         f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{18 + j*3}s" repeatCount="indefinite"/></circle>')
                o.append(f'<circle cx="{cx}" cy="{cy}" r="31" fill="{t["pale"] if theme == "light" else t["panel"]}"/>')
            else:
                o.append(f'<circle cx="{cx}" cy="{cy}" r="36" fill="{t["panel"]}" stroke="{t["border"]}"/>')
            o.append(icon(ic, cx - 16, cy - 16, 32, t["deep"] if tr else t["ink"]))
            o.append(f'<text x="{cx}" y="{cy + 64}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["text"]}">{esc(name)}</text>')
    o.append(stroke_path(f"M{W} {H-130}C{W-60} {H-110} {W-90} {H-80} {W-110} {H-36}", 5, t["branch"]))
    o.append(flowers([(W - 110, H - 36, 14, 10), (W - 80, H - 86, 12, 40), (W - 40, H - 118, 13, 0), (W - 95, H - 60, -7, 30)], t))
    return svg(W, H, "\n".join(o), "Stack — every day: Go, Gin, PostgreSQL, Docker, Git, zsh; in projects: GitHub Actions, golangci-lint, Telegram API, LLM APIs; in training: Kubernetes, Helm, OpenTofu, Yandex Cloud")


# ─────────────────────────────── CI as a metro map ───────────────────────────────

JOBS = [("gofmt · go vet", 4.2), ("go test -race", 6.0), ("golangci-lint", 5.2), ("govulncheck", 4.6), ("hadolint · docker build", 6.8)]


def pipeline(theme):
    t = THEMES[theme]
    H = 420
    o = [paper(W, H, t)]
    o.append(gtext("流", 30, 46, 20, t["deep"], weight=900))
    o.append(f'<text x="58" y="42" font-family="{MONO}" font-size="13" fill="{t["muted"]}">CI line · every push · all trains run in parallel</text>')
    mid = 220
    x0, x_split, x_job, x_join, x_green, x_merge, x_next = 100, 170, 420, 800, 860, 990, 1115
    tracks = []
    for i, (label, dur) in enumerate(JOBS):
        y = 100 + i * 60
        dy = abs(y - mid)
        d = f"M{x0} {mid}H{x_split}L{x_split + dy} {y}H{x_join - dy}L{x_join} {mid}H{x_green}"
        tracks.append((d, y, label, dur))
    for d, *_ in tracks:
        o.append(f'<path d="{d}" fill="none" stroke="{t["ink"]}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<path d="M{x_green} {mid}H{x_merge}" stroke="{t["deep"]}" stroke-width="9" stroke-linecap="round"/>')
    o.append(f'<path d="M{x_merge} {mid}H{x_next - 30}" stroke="{t["deep"]}" stroke-width="9" stroke-linecap="round" stroke-dasharray="2 16" opacity="0.8"/>')
    for d, y, label, dur in tracks:
        o.append(f'<circle cx="{x_job}" cy="{y}" r="11" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="4"/>')
        o.append(f'<text x="{x_job + 24}" y="{y - 14}" font-family="{MONO}" font-size="14" fill="{t["text"]}">{esc(label)}</text>')
    # one train per job, each taking as long as its job
    for d, y, label, dur in tracks:
        o.append(f'<g><animateMotion path="{d}" dur="{dur}s" repeatCount="indefinite" rotate="auto" calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.55 1"/>'
                 f'<rect x="-16" y="-7" width="32" height="14" rx="7" fill="{t["sakura"]}" stroke="{t["deep"]}" stroke-width="1.5"/>'
                 f'<rect x="5" y="-3.5" width="6" height="7" rx="2" fill="{t["bg"]}"/></g>')

    def station(x, kanji, label, sub, pink=False, dashed=False):
        r = 21
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        col = t["deep"] if pink else t["ink"]
        return (f'<rect x="{x - r}" y="{mid - r - 6}" width="{2*r}" height="{2*r + 12}" rx="{r}" fill="{t["bg"]}" stroke="{col}" stroke-width="4"{dash}/>'
                + gtext(kanji, x, mid + 9, 23, col, weight=900, anchor="middle")
                + f'<text x="{x}" y="{mid + 64}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{t["text"]}">{esc(label)}</text>'
                + f'<text x="{x}" y="{mid + 84}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["muted"]}">{esc(sub)}</text>')

    o.append(station(x0, "発", "git push", "departure"))
    o.append(station(x_green, "緑", "all green", "every job passed", pink=True))
    o.append(station(x_merge, "着", "merge", "arrival", pink=True))
    o.append(station(x_next, "次", "→ k8s", "next line", pink=True, dashed=True))
    o.append(f'<text x="30" y="{H-26}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">'
             f'<tspan fill="{t["deep"]}">▬</tspan> train = one CI job    ○ station = check    '
             f'<tspan fill="{t["faint"]}">same line in every Go repo, starting from my gonew template</tspan></text>')
    return svg(W, H, "\n".join(o), "CI as a metro map: git push departs, gofmt and vet, tests, golangci-lint, govulncheck and a Docker build run in parallel, all green, merge; next line: Kubernetes")


# ─────────────────────────────────── dotfiles ───────────────────────────────────

def dotfiles(theme):
    t = THEMES[theme]
    H = 280
    o = [paper(W, H, t, fill=t["panel"])]
    o.append(f'<clipPath id="dc"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    o.append(f'<g clip-path="url(#dc)">{gtext("環境", 780, H + 72, 170, t["ghost"], weight=900, anchor="end")}</g>')
    o.append(f'<text x="34" y="48" font-family="{MONO}" font-size="13" fill="{t["deep"]}" letter-spacing="2">DOTFILES</text>')
    o.append(gtext("My whole Mac, as code.", 32, 102, 40, t["ink"], weight=700))
    o.append(f'<text x="34" y="138" font-family="{SANS}" font-size="16" fill="{t["muted"]}">One command turns a clean Mac into mine, dot doctor checks it, CI tests the setup itself.</text>')
    x = 34
    for ic, label in (("ghostty", "Ghostty"), ("apple", "AeroSpace"), ("zsh", "pure-zsh prompt"), ("zedindustries", "Zed"), ("goland", "GoLand"), ("swift", "Swift")):
        w = text_w(label, 12, mono=True) + 42
        o.append(f'<rect x="{x}" y="164" width="{w:.0f}" height="30" rx="15" fill="none" stroke="{t["faint"]}"/>')
        o.append(icon(ic, x + 11, 172, 14, t["ink"]))
        o.append(f'<text x="{x + 31}" y="183.5" font-family="{MONO}" font-size="12" fill="{t["text"]}">{esc(label)}</text>')
        x += w + 8
    o.append(f'<text x="34" y="{H-36}" font-family="{MONO}" font-size="13" fill="{t["muted"]}"><tspan fill="{t["deep"]}">❯</tspan> ./bootstrap.sh   '
             f'<tspan fill="{t["deep"]}">❯</tspan> dot doctor   <tspan fill="{t["faint"]}"># and the Mac is mine again</tspan></text>')
    tiles = [("8 GB", "of RAM, all of it light"), ("~0.15 s", "zsh start"), ("25", "live wallpapers, Swift"), ("1", "command to set up")]
    for i, (big, small) in enumerate(tiles):
        tx, ty = 800 + (i % 2) * 190, 36 + (i // 2) * 106
        o.append(f'<rect x="{tx}" y="{ty}" width="176" height="94" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>')
        o.append(gtext(big, tx + 18, ty + 50, 34, t["deep"] if i in (0, 3) else t["ink"], weight=900))
        o.append(f'<text x="{tx+18}" y="{ty+76}" font-family="{SANS}" font-size="12" fill="{t["muted"]}">{esc(small)}</text>')
    return svg(W, H, "\n".join(o), "dotfiles: macOS dev environment as code — Ghostty, AeroSpace, zsh, Zed, GoLand themes, live wallpapers in Swift")


# ─────────────────────────────────── footer ───────────────────────────────────

def footer(theme):
    t = THEMES[theme]
    H = 260
    o = [paper(W, H, t, border=False)]
    o.append(f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="18"/></clipPath><g clip-path="url(#fc)">')
    o.append('<g><animateTransform attributeName="transform" type="rotate" values="0 -20 10;0.9 -20 10;0 -20 10" dur="6s" repeatCount="indefinite"/>')
    for d, w in (("M-20 10C80 30 160 60 230 110", 10), ("M230 110C270 140 300 160 340 168", 5),
                 ("M120 42C140 80 150 110 140 150", 5), ("M180 76C220 60 250 40 270 14", 4)):
        o.append(stroke_path(d, w, t["branch"]))
    o.append(flowers([(230, 110, 16, 10), (270, 140, 13, 40), (340, 168, 15, 0), (140, 150, 15, 25), (270, 14, 14, 15),
                      (150, 110, 12, 50), (60, 26, 13, 20), (305, 158, -8, 20), (250, 40, -8, -20)], t))
    o.append("</g>")
    o.append(petals(16, W, H, t, seed=31, x_range=(100, 1250), dur=(7, 12)))
    o.append("</g>")
    o.append(gtext("またね", W / 2, 150, 72, t["ink"], weight=900, anchor="middle", tracking=8))
    o.append(f'<text x="{W/2}" y="196" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t["muted"]}">'
             f'mata ne · see you · <tspan fill="{t["deep"]}">thanks for stopping by</tspan></text>')
    o.append(hanko(W - 90, 120, 56, "夜桜", t, rot=7))
    return svg(W, H, "\n".join(o), "mata ne — see you, thanks for stopping by")


def main():
    for theme in THEMES:
        write("hero", theme, hero(theme))
        write("about", theme, about(theme))
        write("roadmap", theme, roadmap(theme))
        write("stack", theme, stack(theme))
        write("pipeline", theme, pipeline(theme))
        write("dotfiles", theme, dotfiles(theme))
        write("footer", theme, footer(theme))
        for key in SECTIONS:
            write("h-" + key, theme, header(key, theme))
        for i, p in enumerate(PROJECTS):
            write("card-" + p["slug"], theme, card(i, p, theme))
    print("assets written")


if __name__ == "__main__":
    main()
