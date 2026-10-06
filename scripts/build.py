"""Draws every static SVG of the profile README into assets/, dark and light.

    python3 scripts/build.py

Content lives here as plain data (PROJECTS, STACK, ROADMAP...), so updating the profile
means editing a list and re-running the script. Live numbers come from stats.py instead.
"""

import math

from svgkit import (MONO, SANS, THEMES, brand, chip, esc, frame, icon, svg, text_w, write)

W = 1200


def wrap(s, size, width, mono=False):
    lines, cur = [], ""
    for word in s.split():
        nxt = f"{cur} {word}".strip()
        if text_w(nxt, size, mono=mono) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = nxt
    return lines + [cur]


# ───────────────────────────────── hero ─────────────────────────────────

TERMINAL = [
    # (kind, text, color-key)   kind: "cmd" is typed, "out" pops in
    ("cmd", "go test -race ./...", None),
    ("out", "ok    logsence/internal/...   PASS", "green"),
    ("cmd", "docker compose up -d --build", None),
    ("out", "✔ postgres healthy   ✔ app started", "green"),
    ("cmd", "git push origin main", None),
    ("out", "→ CI  fmt · vet · test · lint · vuln · image", "muted"),
    ("out", "✓ all checks passed", "green"),
    ("cmd", "kubectl get pods   # learning now", None),
]


def hero(theme):
    t = THEMES[theme]
    H = 420
    o = ["<defs>",
         f'<radialGradient id="h1" cx="0.86" cy="0.95" r="0.6"><stop offset="0" stop-color="{t["purple"]}" stop-opacity="{t["glow"]}"/>'
         f'<stop offset="1" stop-color="{t["purple"]}" stop-opacity="0"/>'
         '<animate attributeName="cx" values="0.86;0.70;0.86" dur="14s" repeatCount="indefinite"/>'
         '<animate attributeName="cy" values="0.95;0.80;0.95" dur="11s" repeatCount="indefinite"/></radialGradient>',
         f'<radialGradient id="h2" cx="0.04" cy="0.02" r="0.48"><stop offset="0" stop-color="{t["cyan"]}" stop-opacity="{t["glow"]}"/>'
         f'<stop offset="1" stop-color="{t["cyan"]}" stop-opacity="0"/>'
         '<animate attributeName="cx" values="0.04;0.18;0.04" dur="13s" repeatCount="indefinite"/></radialGradient>',
         f'<linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="{t["purple"]}"/><stop offset="1" stop-color="{t["cyan"]}"/></linearGradient>',
         f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["grid"]}"/></pattern>',
         f'<linearGradient id="fade" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{t["bg"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["bg"]}" stop-opacity="0.6"/></linearGradient>',
         f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000" flood-opacity="{0.45 if theme == "dark" else 0.12}"/></filter>',
         "</defs>",
         f'<rect width="{W}" height="{H}" rx="16" fill="{t["bg"]}"/>',
         f'<rect width="{W}" height="{H}" rx="16" fill="url(#grid)"/>',
         f'<rect width="{W}" height="{H}" rx="16" fill="url(#h1)"/>',
         f'<rect width="{W}" height="{H}" rx="16" fill="url(#h2)"/>',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="15.5" fill="none" stroke="{t["border"]}"/>']

    # left: prompt, name, tagline
    m = t["muted"]
    o.append(f'<text x="64" y="84" font-family="{MONO}" font-size="16">'
             f'<tspan fill="{m}">╭─[</tspan><tspan fill="{t["purple"]}" font-weight="700">van1dal</tspan><tspan fill="{m}">@</tspan>'
             f'<tspan fill="{t["cyan"]}" font-weight="700">github</tspan><tspan fill="{m}">]─[</tspan><tspan fill="{t["cyan"]}">~/backend</tspan>'
             f'<tspan fill="{m}">]─[</tspan><tspan fill="{t["yellow"]}">main</tspan><tspan fill="{m}">]</tspan></text>')
    o.append(f'<text x="58" y="194" font-family="{SANS}" font-size="104" font-weight="800" letter-spacing="-4" fill="url(#name)">van1dal</text>')
    o.append(f'<text x="64" y="242" font-family="{SANS}" font-size="27" font-weight="600" fill="{t["text"]}">'
             f'Go backend developer <tspan fill="{t["purple"]}">→</tspan> DevOps</text>')
    o.append(f'<text x="64" y="280" font-family="{SANS}" font-size="17" fill="{m}">REST APIs on Gin + PostgreSQL, shipped in Docker,</text>')
    o.append(f'<text x="64" y="304" font-family="{SANS}" font-size="17" fill="{m}">checked by CI on every push. Next stop: Kubernetes.</text>')

    x = 64
    for name, label in (("go", "Go"), ("postgresql", "PostgreSQL"), ("docker", "Docker"), ("githubactions", "CI/CD"), ("kubernetes", "k8s · learning")):
        w = text_w(label, 13, mono=True) + 46
        dashed = ' stroke-dasharray="4 3"' if "learning" in label else ""
        o.append(f'<rect x="{x}" y="334" width="{w:.0f}" height="32" rx="16" fill="{t["panel"]}" stroke="{t["border"]}"{dashed}/>')
        o.append(icon(name, x + 12, 342, 16, brand(name, theme)))
        o.append(f'<text x="{x + 34}" y="355" font-family="{MONO}" font-size="13" fill="{t["text"]}">{esc(label)}</text>')
        x += w + 10

    # right: terminal window with a typed session that loops
    tx, ty, tw, th = 700, 52, 452, 316
    o.append(f'<g filter="url(#shadow)"><rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/></g>')
    o.append(f'<path d="M{tx} {ty+12}a12 12 0 0 1 12-12h{tw-24}a12 12 0 0 1 12 12v24h-{tw}z" fill="{t["panel2"]}"/>')
    o.append(f'<line x1="{tx}" y1="{ty+36}" x2="{tx+tw}" y2="{ty+36}" stroke="{t["border"]}"/>')
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        o.append(f'<circle cx="{tx + 20 + i*20}" cy="{ty+18}" r="6" fill="{c}"/>')
    o.append(f'<text x="{tx + tw/2}" y="{ty+23}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{m}">~/logsence — zsh</text>')

    T = 16.0             # loop length, seconds
    cw = 13 * 0.602      # monospace advance at 13px
    clock = 0.6
    lx, ly, lh = tx + 20, ty + 66, 27
    clips, lines = [], []
    for i, (kind, txt, ck) in enumerate(TERMINAL):
        y = ly + i * lh
        if kind == "cmd":
            full = "❯ " + txt
            start, dur = clock + 0.35, 0.045 * len(txt)
            clock = start + dur
            body = (f'<tspan fill="{t["purple"]}">❯</tspan> <tspan fill="{t["text"]}">{esc(txt.split("#")[0])}</tspan>'
                    + (f'<tspan fill="{m}">#{esc(txt.split("#")[1])}</tspan>' if "#" in txt else ""))
        else:
            full = txt
            start, dur = clock + 0.25, 0.01
            clock = start + dur
            body = f'<tspan fill="{t[ck]}">{esc(txt)}</tspan>'
        wpx = len(full) * cw + 12
        s, e = start / T, (start + dur) / T
        clips.append(f'<clipPath id="l{i}"><rect x="{lx-2}" y="{y-16}" height="{lh}" width="0">'
                     f'<animate attributeName="width" values="0;0;{wpx:.0f};{wpx:.0f};0" keyTimes="0;{s:.4f};{e:.4f};0.97;1" '
                     f'dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        lines.append(f'<text x="{lx}" y="{y}" xml:space="preserve" font-family="{MONO}" font-size="13" clip-path="url(#l{i})">{body}</text>')
    # blinking cursor on the last prompt, shown once the session has finished
    cy = ly + len(TERMINAL) * lh
    s = (clock + 0.3) / T
    o.append("<defs>" + "".join(clips) + "</defs>")
    o.extend(lines)
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{s:.4f};{s+0.001:.4f};0.97;1" dur="{T}s" repeatCount="indefinite"/>'
             f'<text x="{lx}" y="{cy}" font-family="{MONO}" font-size="13" fill="{t["purple"]}">❯</text>'
             f'<rect x="{lx + 16}" y="{cy - 12}" width="8" height="15" fill="{t["purple"]}">'
             '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
    return svg(W, H, "\n".join(o), "van1dal — Go backend developer moving into DevOps")


# ──────────────────────────────── projects ────────────────────────────────

PROJECTS = [
    dict(slug="logsence", repo="logsence", status="building now",
         desc="Log collection service: ingest logs over HTTP, store them in PostgreSQL, query them by service.",
         chips=["Gin", "pgx + sqlx", "migrations", "Docker", "CI"]),
    dict(slug="ordergo", repo="OrderGo",
         desc="REST API for orders, built step by step toward a production layout: cmd/ + internal/, config, health.",
         chips=["Gin", "PostgreSQL", "Compose", "Makefile"]),
    dict(slug="watchdog", repo="watchdog",
         desc="Uptime monitor: polls a service's /health every 5 seconds and reports when it stops answering.",
         chips=["net/http", "no framework", "Docker"]),
    dict(slug="pulse", repo="Pulse",
         desc="A small HTTP framework for Go: own Context, routing for every verb and a middleware chain, Gin as the engine.",
         chips=["Context", "routing", "middleware"]),
    dict(slug="mini-deploy", repo="MINI-deploy",
         desc="Deployment API for DevOps practice: accepts deploy requests, tracks them, exposes a health check.",
         chips=["Gin", "health check"], todo=["CI/CD", "Yandex Cloud"]),
    dict(slug="nexa", repo="NEXA-AI-BOT", title="NEXA AI", icon2="telegram",
         desc="Telegram bot that talks to an LLM through the OpenRouter API: /start, /help, /about and free chat.",
         chips=["Telegram Bot API", "OpenRouter"]),
]


def card(p, theme):
    t = THEMES[theme]
    w, h = 590, 214
    title = p.get("title", p["repo"])
    o = [frame(w, h, t, glows=((1.0, 0.0, 0.55, "purple"), (0.0, 1.0, 0.5, "cyan")), uid="c"),
         f'<defs><linearGradient id="bar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{t["purple"]}"/>'
         f'<stop offset="1" stop-color="{t["cyan"]}"/></linearGradient></defs>',
         f'<rect x="0" y="28" width="4" height="{h-56}" rx="2" fill="url(#bar)"/>']
    o.append(f'<text x="30" y="42" font-family="{MONO}" font-size="13" fill="{t["muted"]}">van1dalgrr-arch /</text>')
    o.append(f'<text x="30" y="74" font-family="{SANS}" font-size="27" font-weight="700" fill="{t["text"]}">{esc(title)}</text>')

    # top-right: status pill or language
    if p.get("status"):
        label = p["status"]
        pw = text_w(label, 12, mono=True) + 34
        px = w - 26 - pw
        o.append(f'<rect x="{px:.0f}" y="24" width="{pw:.0f}" height="26" rx="13" fill="{t["green"]}" fill-opacity="0.12" stroke="{t["green"]}" stroke-opacity="0.6"/>')
        o.append(f'<circle cx="{px+14:.0f}" cy="37" r="4" fill="{t["green"]}"><animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>')
        o.append(f'<text x="{px+24:.0f}" y="41.5" font-family="{MONO}" font-size="12" fill="{t["green"]}">{esc(label)}</text>')
    else:
        ic = p.get("icon2", "go")
        o.append(icon(ic, w - 50, 26, 24, brand(ic, theme)))
        if ic != "go":
            o.append(icon("go", w - 86, 26, 24, brand("go", theme)))

    y = 108
    for line in wrap(p["desc"], 15.5, w - 60)[:3]:
        o.append(f'<text x="30" y="{y}" font-family="{SANS}" font-size="15.5" fill="{t["muted"]}">{esc(line)}</text>')
        y += 23

    x = 30
    for c in p["chips"]:
        s, cw = chip(x, h - 46, c, t, size=12)
        o.append(s)
        x += cw + 8
    for c in p.get("todo", []):
        s, cw = chip(x, h - 46, "next: " + c, t, size=12, dashed=True)
        o.append(s)
        x += cw + 8
    return svg(w, h, "\n".join(o), f"{title}: {p['desc']}")


# ────────────────────────────────── stack ──────────────────────────────────

STACK = [
    dict(title="every day", color="cyan",
         items=[("go", "Go"), ("gin", "Gin"), ("postgresql", "PostgreSQL"), ("docker", "Docker"), ("git", "Git"), ("zsh", "zsh · bash")],
         extra=["REST APIs", "SQL", "Compose", "Makefiles"]),
    dict(title="in my projects", color="purple",
         items=[("githubactions", "Actions CI"), ("go", "golangci-lint"), ("telegram", "Telegram API"), ("openrouter", "LLM APIs")],
         extra=["migrations", "govulncheck", "hadolint", "gitleaks"]),
    dict(title="learning now", color="yellow", learning=True,
         items=[("kubernetes", "Kubernetes"), ("helm", "Helm"), ("opentofu", "OpenTofu"), ("yandexcloud", "Yandex Cloud")],
         extra=["kind", "OrbStack", "k9s", "observability"]),
]


def stack(theme):
    t = THEMES[theme]
    H = 350
    o = [frame(W, H, t, glows=((0.5, 1.2, 0.6, "purple"), (0.0, 0.0, 0.35, "cyan")), uid="s")]
    pw, gap, x0 = 368, 24, 30
    for i, col in enumerate(STACK):
        x = x0 + i * (pw + gap)
        c = t[col["color"]]
        dash = ' stroke-dasharray="6 5"' if col.get("learning") else ""
        o.append(f'<rect x="{x}" y="28" width="{pw}" height="{H-56}" rx="12" fill="{t["panel"]}" fill-opacity="0.85" stroke="{t["border"]}"{dash}/>')
        o.append(f'<circle cx="{x+24}" cy="56" r="5" fill="{c}">'
                 + ('<animate attributeName="r" values="5;7;5" dur="1.6s" repeatCount="indefinite"/>' if col.get("learning") else "")
                 + "</circle>")
        o.append(f'<text x="{x+38}" y="61" font-family="{MONO}" font-size="14" font-weight="700" fill="{c}" letter-spacing="1">{esc(col["title"].upper())}</text>')
        o.append(f'<line x1="{x+20}" y1="80" x2="{x+pw-20}" y2="80" stroke="{t["border"]}"/>')
        for j, (ic, label) in enumerate(col["items"]):
            ix = x + 20 + (j % 2) * (pw - 40) / 2
            iy = 96 + (j // 2) * 50
            o.append(f'<rect x="{ix}" y="{iy}" width="36" height="36" rx="9" fill="{t["panel2"]}" stroke="{t["border"]}"/>')
            o.append(icon(ic, ix + 8, iy + 8, 20, brand(ic, theme)))
            o.append(f'<text x="{ix+48}" y="{iy+23}" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["text"]}">{esc(label)}</text>')
        cx, cy = x + 20, 262
        for e in col["extra"]:
            s, cw = chip(cx, cy, e, t, size=12, h=24, dashed=bool(col.get("learning")))
            if cx + cw > x + pw - 16:
                cx, cy = x + 20, cy + 30
                s, cw = chip(cx, cy, e, t, size=12, h=24, dashed=bool(col.get("learning")))
            o.append(s)
            cx += cw + 6
    return svg(W, H, "\n".join(o), "Skills: every day Go, Gin, PostgreSQL, Docker, Git, zsh; in projects GitHub Actions, golangci-lint, Telegram Bot API, LLM APIs; learning Kubernetes, Helm, OpenTofu, Yandex Cloud")


# ───────────────────────────────── pipeline ─────────────────────────────────

JOBS = [("gofmt · go vet", 0.26), ("go test -race", 0.44), ("golangci-lint", 0.36), ("govulncheck", 0.31), ("hadolint · docker build", 0.52)]


def pipeline(theme):
    t = THEMES[theme]
    H, T = 360, 9.0
    o = [frame(W, H, t, glows=((0.55, 0.5, 0.45, "green"), (0.0, 0.0, 0.35, "purple")), uid="p"),
         f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0L10 5L0 10z" fill="{t["faint"]}"/></marker></defs>']

    def anim(attr, vals, times):
        return (f'<animate attributeName="{attr}" values="{";".join(map(str, vals))}" '
                f'keyTimes="{";".join(f"{k:.4f}" for k in times)}" dur="{T}s" repeatCount="indefinite"/>')

    def packet(d, s, e, color):
        return (f'<circle r="4.5" fill="{color}" opacity="0">'
                f'<animateMotion path="{d}" keyPoints="0;0;1;1" keyTimes="0;{s:.4f};{e:.4f};1" calcMode="linear" dur="{T}s" repeatCount="indefinite"/>'
                + anim("opacity", [0, 0, 1, 1, 0, 0], [0, s, s + 0.005, e - 0.005, e, 1]) + "</circle>")

    def box(x, y, w, h, label, stroke, bold=False, dashed=False, color=None):
        d = ' stroke-dasharray="6 5"' if dashed else ""
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["panel"]}" stroke="{stroke}" stroke-width="1.5"{d}/>'
                f'<text x="{x + w/2}" y="{y + h/2 + 5.5}" text-anchor="middle" font-family="{MONO}" font-size="{16 if bold else 15}" '
                f'font-weight="{700 if bold else 500}" fill="{color or t["text"]}">{esc(label)}</text>')

    def status(cx, cy, done_at):
        """Yellow spinner until done_at, then a green check; resets with the loop."""
        return (f'<g opacity="1">{anim("opacity", [1, 1, 0, 0, 1], [0, done_at, done_at + 0.002, 0.97, 1])}'
                f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{t["yellow"]}" stroke-width="2" stroke-dasharray="30 14">'
                f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="0.9s" repeatCount="indefinite"/></circle></g>'
                f'<g opacity="0">{anim("opacity", [0, 0, 1, 1, 0], [0, done_at, done_at + 0.002, 0.97, 1])}'
                f'<circle cx="{cx}" cy="{cy}" r="8" fill="{t["green"]}"/>'
                f'<path d="M{cx-3.5} {cy}l2.5 2.6 4.8-5" fill="none" stroke="{t["bg"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')

    o.append(f'<text x="40" y="46" font-family="{SANS}" font-size="15" fill="{t["muted"]}">every push · jobs run in parallel</text>')
    o.append(box(40, 145, 150, 50, "git push", t["purple"], bold=True))
    go_out = 0.10
    for i, (label, done) in enumerate(JOBS):
        y = 30 + i * 60
        mid = y + 20
        d_in = f"M190 170 C245 170 245 {mid} 300 {mid}"
        d_out = f"M560 {mid} C610 {mid} 610 170 660 170"
        o.append(f'<path d="{d_in}" fill="none" stroke="{t["faint"]}" stroke-width="1.5" marker-end="url(#a)"/>')
        o.append(f'<path d="{d_out}" fill="none" stroke="{t["faint"]}" stroke-width="1.5" marker-end="url(#a)"/>')
        o.append(f'<rect x="300" y="{y}" width="260" height="40" rx="10" fill="{t["panel"]}" stroke="{t["cyan"]}" stroke-width="1.5"/>')
        o.append(f'<text x="446" y="{y+26}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="500" fill="{t["text"]}">{esc(label)}</text>')
        o.append(status(322, mid, done))
        o.append(packet(d_in, 0.02, go_out, t["purple"]))
        o.append(packet(d_out, done, done + 0.08, t["green"]))

    green_at = max(d for _, d in JOBS) + 0.09
    merge_at = green_at + 0.10
    # "all green": grey while waiting, lights up when every job has reported
    o.append(f'<rect x="660" y="140" width="150" height="60" rx="10" fill="{t["panel"]}" stroke="{t["faint"]}" stroke-width="1.5"/>')
    o.append(f'<rect x="660" y="140" width="150" height="60" rx="10" fill="{t["green"]}" fill-opacity="0.10" stroke="{t["green"]}" stroke-width="1.5" opacity="0">'
             + anim("opacity", [0, 0, 1, 1, 0], [0, green_at, green_at + 0.02, 0.97, 1]) + "</rect>")
    o.append(f'<text x="735" y="176" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="{t["text"]}">all green ✓</text>')
    d_m = "M810 170 C845 170 845 170 880 170"
    o.append(f'<path d="{d_m}" fill="none" stroke="{t["faint"]}" stroke-width="1.5" marker-end="url(#a)"/>')
    o.append(packet(d_m, green_at, merge_at - 0.02, t["green"]))
    o.append(f'<rect x="880" y="145" width="120" height="50" rx="10" fill="{t["panel"]}" stroke="{t["purple"]}" stroke-width="1.5"/>')
    o.append(f'<rect x="880" y="145" width="120" height="50" rx="10" fill="{t["purple"]}" fill-opacity="0.16" opacity="0">'
             + anim("opacity", [0, 0, 1, 1, 0], [0, merge_at, merge_at + 0.02, 0.97, 1]) + "</rect>")
    o.append(f'<text x="940" y="176" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="{t["text"]}">merge</text>')
    o.append(f'<path d="M1000 170 C1020 170 1020 170 1040 170" fill="none" stroke="{t["faint"]}" stroke-width="1.5" stroke-dasharray="6 5" marker-end="url(#a)"/>')
    o.append(f'<rect x="1040" y="125" width="130" height="90" rx="10" fill="none" stroke="{t["faint"]}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    o.append(icon("kubernetes", 1093, 136, 24, brand("kubernetes", theme), opacity=0.8))
    o.append(f'<text x="1105" y="182" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["muted"]}">image →</text>')
    o.append(f'<text x="1105" y="200" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["muted"]}">Kubernetes</text>')
    o.append(f'<text x="1105" y="238" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t["muted"]}">next</text>')
    o.append(f'<text x="40" y="{H-26}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">'
             f'<tspan fill="{t["yellow"]}">◌</tspan> running   <tspan fill="{t["green"]}">●</tspan> passed   '
             f'<tspan fill="{t["purple"]}">●</tspan> commit on its way</text>')
    return svg(W, H, "\n".join(o), "git push runs gofmt, tests, golangci-lint, govulncheck and a Docker build in parallel; all green, then merge; next: image to Kubernetes")


# ───────────────────────────────── roadmap ─────────────────────────────────

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
    H = 230
    o = [frame(W, H, t, glows=((0.4, 0.45, 0.22, "yellow"), (1.0, 1.0, 0.4, "purple")), uid="r"),
         f'<defs><linearGradient id="track" x1="0" x2="1"><stop offset="0" stop-color="{t["purple"]}"/>'
         f'<stop offset="1" stop-color="{t["cyan"]}"/></linearGradient></defs>']
    n = len(ROADMAP)
    x0, x1, ty = 100, 1100, 108
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    now = next(i for i, r in enumerate(ROADMAP) if r[2] == "now")
    o.append(f'<text x="36" y="44" font-family="{MONO}" font-size="14" fill="{t["muted"]}">'
             f'<tspan fill="{t["purple"]}">$</tspan> cat roadmap.md   <tspan fill="{t["faint"]}"># backend → DevOps</tspan></text>')
    o.append(f'<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" stroke="{t["border"]}" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 10"/>')
    o.append(f'<line x1="{x0}" y1="{ty}" x2="{xs[now]}" y2="{ty}" stroke="url(#track)" stroke-width="4" stroke-linecap="round">'
             f'<animate attributeName="x2" values="{x0};{xs[now]};{xs[now]}" keyTimes="0;0.35;1" dur="6s" repeatCount="indefinite"/></line>')
    for i, (name, sub, state) in enumerate(ROADMAP):
        x = xs[i]
        if state == "done":
            o.append(f'<circle cx="{x}" cy="{ty}" r="13" fill="url(#track)"/>')
            o.append(f'<path d="M{x-5} {ty}l3.5 3.6 6.5-7" fill="none" stroke="{t["bg"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        elif state == "now":
            o.append(f'<circle cx="{x}" cy="{ty}" r="16" fill="none" stroke="{t["yellow"]}" stroke-width="2">'
                     '<animate attributeName="r" values="16;30" dur="1.8s" repeatCount="indefinite"/>'
                     '<animate attributeName="opacity" values="0.9;0" dur="1.8s" repeatCount="indefinite"/></circle>')
            o.append(f'<circle cx="{x}" cy="{ty}" r="16" fill="{t["bg"]}" stroke="{t["yellow"]}" stroke-width="3"/>')
            o.append(icon("kubernetes", x - 10, ty - 10, 20, brand("kubernetes", theme)))
            lw = text_w("I'm here", 12, mono=True) + 20
            o.append(f'<rect x="{x - lw/2:.0f}" y="{ty-58}" width="{lw:.0f}" height="24" rx="12" fill="{t["yellow"]}" fill-opacity="0.14" stroke="{t["yellow"]}" stroke-opacity="0.7"/>')
            o.append(f'<text x="{x}" y="{ty-41.5}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["yellow"]}">I\'m here</text>')
        else:
            o.append(f'<circle cx="{x}" cy="{ty}" r="11" fill="{t["bg"]}" stroke="{t["faint"]}" stroke-width="2" stroke-dasharray="4 3"/>')
        col = t["text"] if state != "next" else t["muted"]
        o.append(f'<text x="{x}" y="{ty+48}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{col}">{esc(name)}</text>')
        o.append(f'<text x="{x}" y="{ty+70}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{t["muted"]}">{esc(sub)}</text>')
    return svg(W, H, "\n".join(o), "Roadmap: Go + SQL, Docker and CI done; Kubernetes now; next Helm, OpenTofu, Yandex Cloud, observability")


# ──────────────────────────────── dotfiles ────────────────────────────────

def dotfiles(theme):
    t = THEMES[theme]
    H = 250
    o = [frame(W, H, t, glows=((1.0, 0.0, 0.5, "purple"), (0.0, 1.0, 0.45, "cyan")), uid="d"),
         f'<defs><linearGradient id="bar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{t["purple"]}"/>'
         f'<stop offset="1" stop-color="{t["cyan"]}"/></linearGradient></defs>',
         f'<rect x="0" y="32" width="4" height="{H-64}" rx="2" fill="url(#bar)"/>']
    o.append(f'<text x="34" y="46" font-family="{MONO}" font-size="13" fill="{t["muted"]}">van1dalgrr-arch /</text>')
    o.append(f'<text x="34" y="80" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["text"]}">dotfiles</text>')
    o.append(f'<text x="34" y="112" font-family="{SANS}" font-size="16" fill="{t["muted"]}">My macOS dev environment as code. A clean Mac becomes my Mac in one command,</text>')
    o.append(f'<text x="34" y="135" font-family="{SANS}" font-size="16" fill="{t["muted"]}">and CI tests the setup itself.</text>')
    x = 34
    for ic, label in (("ghostty", "Ghostty"), ("apple", "AeroSpace"), ("zsh", "pure-zsh prompt"), ("zedindustries", "Zed"), ("goland", "GoLand"), ("swift", "Swift")):
        w = text_w(label, 12, mono=True) + 42
        o.append(f'<rect x="{x}" y="160" width="{w:.0f}" height="28" rx="14" fill="{t["chip"]}" stroke="{t["border"]}"/>')
        o.append(icon(ic, x + 11, 167, 14, brand(ic, theme)))
        o.append(f'<text x="{x + 31}" y="178.5" font-family="{MONO}" font-size="12" fill="{t["text"]}">{esc(label)}</text>')
        x += w + 8
    o.append(f'<text x="34" y="{H-28}" font-family="{MONO}" font-size="13" fill="{t["muted"]}"><tspan fill="{t["purple"]}">❯</tspan> ./bootstrap.sh   '
             f'<tspan fill="{t["purple"]}">❯</tspan> dot doctor</text>')

    # stat tiles on the right
    tiles = [("8 GB", "of RAM, tuned to stay light"), ("~0.15 s", "zsh start"), ("25", "live wallpapers in Swift"), ("1", "command from clean Mac")]
    for i, (big, small) in enumerate(tiles):
        tx = 780 + (i % 2) * 196
        ty = 32 + (i // 2) * 96
        o.append(f'<rect x="{tx}" y="{ty}" width="184" height="84" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        o.append(f'<text x="{tx+18}" y="{ty+40}" font-family="{SANS}" font-size="28" font-weight="800" fill="{t["purple"] if i % 3 == 0 else t["cyan"]}">{esc(big)}</text>')
        o.append(f'<text x="{tx+18}" y="{ty+64}" font-family="{SANS}" font-size="12.5" fill="{t["muted"]}">{esc(small)}</text>')
    return svg(W, H, "\n".join(o), "dotfiles: macOS dev environment as code — Ghostty, AeroSpace, zsh, Zed, GoLand themes, live wallpapers in Swift")


# ───────────────────────────────── footer ─────────────────────────────────

def footer(theme):
    t = THEMES[theme]
    H = 90
    o = ["<defs>",
         f'<linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="{t["purple"]}"/><stop offset="1" stop-color="{t["cyan"]}"/></linearGradient>',
         "</defs>"]
    # two slow sine waves drifting sideways
    for k, (amp, op, dur) in enumerate(((10, 0.55, 9), (7, 0.3, 13))):
        pts = []
        for i in range(0, 2 * W + 1, 20):
            pts.append(f"{i},{30 + amp * math.sin(i / 95 + k):.1f}")
        d = "M" + " L".join(pts)
        o.append(f'<g opacity="{op}"><path d="{d}" fill="none" stroke="url(#w)" stroke-width="2">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;{-95 * 2 * 3.14159:.0f} 0" dur="{dur}s" repeatCount="indefinite"/></path></g>')
    o.append(f'<text x="{W/2}" y="76" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t["muted"]}">'
             f'<tspan fill="{t["purple"]}">❯</tspan> exit   <tspan fill="{t["faint"]}"># thanks for stopping by</tspan></text>')
    return svg(W, H, "\n".join(o), "thanks for stopping by")


def main():
    for theme in THEMES:
        write("hero", theme, hero(theme))
        write("pipeline", theme, pipeline(theme))
        write("stack", theme, stack(theme))
        write("roadmap", theme, roadmap(theme))
        write("dotfiles", theme, dotfiles(theme))
        write("footer", theme, footer(theme))
        for p in PROJECTS:
            write("card-" + p["slug"], theme, card(p, theme))
    print("assets written")


if __name__ == "__main__":
    main()
