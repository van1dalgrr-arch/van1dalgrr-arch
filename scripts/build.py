#!/usr/bin/env python3
"""Рисует все статичные картинки профиля в assets/:  python3 scripts/build.py

Тексты лежат здесь обычными списками (SECTIONS, TRACKS, FEATURED, PROJECTS, STACK) —
поправил строку, перезапустил скрипт, закоммитил. Живые цифры рисуют terminal.py и stats.py в workflow.
"""
import math, random
from kit import (C, GRAD, MONO, SANS, card, esc, glow, gt, gw, icon, lgrad, pixels, scanlines, stars, svg, tw, write)

W = 1200


def wrap(s, size, width):
    lines, cur = [], ""
    for word in s.split():
        nxt = f"{cur} {word}".strip()
        if tw(nxt, size, mono=False) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = nxt
    return lines + [cur]


def chips(items, x, y, size=12, h=26, color=None):
    out = []
    for it in items:
        w = tw(it, size) + 22
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{C["panel2"]}" stroke="{color or C["line"]}"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{C["soft"]}">{esc(it)}</text>')
        x += w + 8
    return "".join(out)


# ═════════════════════════════════ баннер: белая ночь над Невой ═════════════════════════════════

H_HORIZON = 440


def skyline():
    """Силуэт Петербурга: низкие фасады, Петропавловка, Исаакий, Адмиралтейство. Окна мерцают."""
    ink = "#0b0d15"
    rnd = random.Random(7)
    hz = H_HORIZON
    o = [f'<g fill="{ink}">']
    x = 0
    while x < W:   # сплошная линия набережных — в Петербурге город низкий и ровный
        w = rnd.randint(40, 110)
        h = rnd.randint(14, 34)
        o.append(f'<rect x="{x}" y="{hz - h}" width="{w + 1}" height="{h}"/>')
        if rnd.random() < 0.25:   # фронтон
            o.append(f'<path d="M{x + w * 0.3:.0f} {hz - h}L{x + w * 0.5:.0f} {hz - h - 9}L{x + w * 0.7:.0f} {hz - h}Z"/>')
        x += w
    # Петропавловский собор: ярусы башни и игла
    o.append(f'<rect x="1046" y="{hz - 32}" width="150" height="32"/>')
    o.append(f'<rect x="1102" y="{hz - 62}" width="36" height="32"/><rect x="1107" y="{hz - 92}" width="26" height="32"/>')
    o.append(f'<rect x="1112" y="{hz - 114}" width="16" height="24"/>')
    o.append(f'<path d="M1114 {hz - 114}L1120 {hz - 300}L1126 {hz - 114}Z"/>')
    o.append(f'<path d="M1120 {hz - 318}V{hz - 298}M1115 {hz - 311}H1125" stroke="{ink}" stroke-width="2.4"/>')
    # Исаакиевский собор: колоннада, барабан, купол, фонарь
    o.append(f'<rect x="820" y="{hz - 40}" width="130" height="40"/>')
    o.append(f'<rect x="845" y="{hz - 80}" width="80" height="42"/>')
    o.append(f'<path d="M838 {hz - 78}A47 54 0 0 1 932 {hz - 78}Z"/>')
    o.append(f'<rect x="878" y="{hz - 150}" width="14" height="24"/><circle cx="885" cy="{hz - 152}" r="8"/>')
    o.append(f'<path d="M885 {hz - 172}V{hz - 158}M880 {hz - 167}H890" stroke="{ink}" stroke-width="2"/>')
    o.append(f'<rect x="808" y="{hz - 56}" width="22" height="18"/><rect x="940" y="{hz - 56}" width="22" height="18"/>')
    # Адмиралтейство: длинный корпус, башня, игла с корабликом
    o.append(f'<rect x="565" y="{hz - 30}" width="200" height="30"/>')
    o.append(f'<rect x="648" y="{hz - 70}" width="30" height="42"/><rect x="652" y="{hz - 92}" width="22" height="24"/>')
    o.append(f'<path d="M659 {hz - 92}L663 {hz - 230}L667 {hz - 92}Z"/><circle cx="243" cy="{hz - 232}" r="3"/>')
    o.append(f'<path d="M657 {hz - 240}h12l-3 5h-6z"/>')
    o.append("</g>")
    # окна: тёплые точки, часть мерцает
    for _ in range(70):
        wx = rnd.uniform(5, W - 5)
        wy = hz - rnd.uniform(5, 26)
        col = rnd.choice((C["sun"], C["amber"], C["rose"]))
        d = rnd.uniform(3, 9)
        o.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="2.4" height="3" fill="{col}" opacity="0.8">'
                 f'<animate attributeName="opacity" values="0.85;0.85;0.1;0.85" keyTimes="0;0.7;0.8;1" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></rect>')
    return "\n".join(o)


def bridge():
    """Дворцовый мост: пролёты, фонари и разводной центр — крылья поднимаются и опускаются."""
    ink, y = "#10131c", 478
    o = [f'<g fill="{ink}">']
    o.append(f'<rect x="40" y="{y}" width="250" height="9"/><rect x="390" y="{y}" width="230" height="9"/>')
    for px in (40, 150, 260, 390, 500, 610):
        o.append(f'<rect x="{px}" y="{y + 9}" width="16" height="40"/>')
    for a, b in ((56, 150), (166, 260), (406, 500), (516, 610)):
        o.append(f'<path d="M{a} {y + 9}H{b}V{y + 22}Q{(a + b) / 2} {y + 6} {a} {y + 22}Z"/>')
    o.append("</g>")
    leaf = lambda x0, x1, sign: (
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'values="0 {x0} {y};0 {x0} {y};{sign * 64} {x0} {y};{sign * 64} {x0} {y};0 {x0} {y}" '
        f'keyTimes="0;0.2;0.42;0.78;1" dur="16s" repeatCount="indefinite" calcMode="spline" '
        f'keySplines="0 0 1 1;0.45 0 0.55 1;0 0 1 1;0.45 0 0.55 1"/>'
        f'<rect x="{min(x0, x1)}" y="{y}" width="{abs(x1 - x0)}" height="9" fill="{ink}"/>'
        + "".join(f'<circle cx="{min(x0, x1) + 8 + i * 16}" cy="{y - 3}" r="2" fill="{C["sun"]}"/>' for i in range(3))
        + "</g>")
    o.append(leaf(290, 340, -1))
    o.append(leaf(390, 340, 1))
    for lx in list(range(52, 290, 26)) + list(range(400, 620, 26)):   # фонари
        o.append(f'<line x1="{lx}" y1="{y}" x2="{lx}" y2="{y - 12}" stroke="{ink}" stroke-width="2"/>'
                 f'<circle cx="{lx}" cy="{y - 13}" r="2.3" fill="{C["sun"]}"><animate attributeName="opacity" values="1;0.6;1" dur="{2 + lx % 5 * 0.4:.1f}s" repeatCount="indefinite"/></circle>')
    return "\n".join(o)


def gulls():
    """Чайки над Невой: медленно летят через кадр и машут крыльями."""
    o = []
    for i, (y, dur, scale, delay) in enumerate(((62, 46, 0.9, 0), (108, 58, 0.7, 20), (40, 64, 0.55, 35), (120, 52, 0.75, 8))):
        o.append(f'<g><animateMotion path="M-40 {y} C300 {y - 30} 700 {y + 25} {W + 40} {y - 10}" dur="{dur}s" begin="-{delay}s" repeatCount="indefinite"/>'
                 f'<g transform="scale({scale})"><path d="M-11 0Q-5 -6 0 0Q5 -6 11 0" fill="none" stroke="{C["text"]}" stroke-opacity="0.75" stroke-width="1.8" stroke-linecap="round">'
                 f'<animateTransform attributeName="transform" type="scale" values="1 1;1 -0.5;1 1" dur="{0.9 + i * 0.15:.2f}s" repeatCount="indefinite"/></path></g></g>')
    return "\n".join(o)


def hero():
    H, hz = 620, H_HORIZON
    sx, sy, sr = 800, 392, 178
    o = ["<defs>",
         lgrad("sky", ["#090b11", "#141827", "#2a2b40", "#544a5e", "#a0807c"], 0, 0, 0, 1),
         lgrad("sea", ["#2c2a37", "#151821", "#090b11"], 0, 0, 0, 1),
         lgrad("sun", [C["sun"], C["amber"], C["pink"], "#7a6a8c"], 0, 0, 0, 1),
         lgrad("chrome", ["#f6f2ea", "#ece3d8", "#dcc6c0", C["rose"], C["amber"]], 0, 0, 0, 1),
         lgrad("refl", [C["sun"], C["pink"], C["violet"]], 0, 0, 0, 1),
         f'<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0.3" stop-color="{C["pink"]}" stop-opacity="0.22"/>'
         f'<stop offset="1" stop-color="{C["pink"]}" stop-opacity="0"/></radialGradient>',
         glow("nglow", 7, 0.3), glow("sglow", 4, 0.4),
         f'<clipPath id="hclip"><rect width="{W}" height="{H}" rx="22"/></clipPath>',
         f'<clipPath id="above"><rect width="{W}" height="{hz}"/></clipPath>',
         # «прорези» в солнце, ползут вниз
         f'<mask id="slits"><rect width="{W}" height="{H}" fill="#fff"/><g fill="#000">'
         + "".join(f'<rect x="0" y="{sy - 10 + i * 22}" width="{W}" height="{2 + i * 1.6:.1f}"/>' for i in range(-1, 6))
         + '<animateTransform attributeName="transform" type="translate" values="0 0;0 22" dur="2.2s" repeatCount="indefinite"/></g></mask>',
         "</defs>",
         '<g clip-path="url(#hclip)">',
         f'<rect width="{W}" height="{hz}" fill="url(#sky)"/>',
         f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="url(#sea)"/>',
         stars(90, W, hz - 120, seed=3)]
    o.append(f'<circle cx="{sx}" cy="{sy}" r="{sr * 1.9}" fill="url(#halo)"/>')
    o.append(f'<g clip-path="url(#above)"><circle cx="{sx}" cy="{sy}" r="{sr}" fill="url(#sun)" mask="url(#slits)"/></g>')
    # дымка над водой: белая ночь не бывает резкой
    o.append(f'<defs>{lgrad("fog", ["#d9c7c0", "#d9c7c0", "#d9c7c0"], 0, 0, 0, 1)}'
             f'<linearGradient id="haze" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#d9c7c0" stop-opacity="0"/>'
             f'<stop offset="0.6" stop-color="#d9c7c0" stop-opacity="0.16"/><stop offset="1" stop-color="#d9c7c0" stop-opacity="0"/></linearGradient></defs>')
    o.append(skyline())
    o.append(f'<rect y="{hz - 70}" width="{W}" height="110" fill="url(#haze)"/>')
    o.append(gulls())
    # отражение солнца в Неве: дрожащие полосы
    for i in range(12):
        y = hz + 8 + i * 13
        w = 330 * (1 - i * 0.065)
        op = 0.75 - i * 0.055
        d = 1.6 + (i % 4) * 0.35
        o.append(f'<rect x="{sx - w / 2:.0f}" y="{y}" width="{w:.0f}" height="{3 + i * 0.3:.1f}" rx="2" fill="url(#refl)" opacity="{op:.2f}">'
                 f'<animate attributeName="width" values="{w:.0f};{w * 0.82:.0f};{w:.0f}" dur="{d:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="x" values="{sx - w / 2:.0f};{sx - w * 0.41:.0f};{sx - w / 2:.0f}" dur="{d:.1f}s" repeatCount="indefinite"/></rect>')
    rnd = random.Random(11)
    for _ in range(26):   # рябь
        y = rnd.uniform(hz + 6, H - 10)
        x = rnd.uniform(0, W)
        w = rnd.uniform(20, 90)
        d = rnd.uniform(5, 11)
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="1.4" fill="{C["lilac"]}" opacity="0.25">'
                 f'<animate attributeName="x" values="{x:.0f};{x - 60:.0f}" dur="{d:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0.35;0" dur="{d:.1f}s" repeatCount="indefinite"/></rect>')
    o.append(bridge())

    # надписи
    o.append(gt("PLAYER 1", 64, 86, 13, C["rose"], font="pixel", tracking=2))
    o.append(f'<g>{gt("READY", 64 + gw("PLAYER 1 ", 13, "pixel", 2) + 10, 86, 13, C["sun"], font="pixel", tracking=2)}'
             '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/></g>')
    size = 118
    while gw("van1dal", size, "display", -2) > 560:
        size -= 2
    o.append(gt("van1dal", 58, 222, size, "url(#chrome)", tracking=-2, extra=' filter="url(#nglow)"'))
    o.append(gt("Go backend developer", 62, 278, 28, C["text"], font="bold"))
    o.append(f'<text x="64" y="316" font-family="{MONO}" font-size="16" fill="{C["soft"]}">Gin · PostgreSQL · Redis · Docker · CI on every push</text>')
    o.append(gt("SAINT PETERSBURG", 64, 356, 12, C["amber"], font="pixel", tracking=2))
    o.append(f'<text x="{64 + gw("SAINT PETERSBURG", 12, "pixel", 2) + 16}" y="356" font-family="{MONO}" font-size="13" fill="{C["muted"]}">59.94°N 30.31°E</text>')
    o.append(f'<g>{gt("PRESS START", W / 2, H - 26, 12, C["text"], font="pixel", anchor="middle", tracking=3)}'
             '<animate attributeName="opacity" values="1;0.15;1" dur="1.6s" repeatCount="indefinite"/></g>')
    o.append(scanlines(W, H))
    o.append("</g>")
    o.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="21" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
    return svg(W, H, "\n".join(o), "van1dal — Go backend developer from Saint Petersburg: a synthwave sun setting over the Neva, the spires, and Palace Bridge opening")


# ═════════════════════════════════ заголовки разделов ═════════════════════════════════

SECTIONS = {
    "about":    ("01", "About me", "neofetch"),
    "now":      ("02", "Now playing", "cat now.md"),
    "projects": ("03", "Projects", "ls ~/dev"),
    "stack":    ("04", "Stack", "go version"),
    "desk":     ("05", "Desk", "dot doctor"),
    "arcade":   ("06", "Arcade", "./insert-coin"),
    "contact":  ("07", "Contact", "open mail"),
}


def header(key):
    num, title, cmd = SECTIONS[key]
    H = 100
    o = ["<defs>",
         lgrad(f"t{key}", [C["lilac"], C["rose"], C["amber"], C["lilac"]], 0, 0, 1, 0,
               anim='<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;0 0" dur="14s" repeatCount="indefinite"/>'),
         f'<linearGradient id="u{key}" spreadMethod="repeat" x1="0" x2="0.35">'
         + "".join(f'<stop offset="{o_}" stop-color="{c}"/>' for o_, c in ((0, C["violet"]), (0.5, C["pink"]), (1, C["violet"])))
         + '<animateTransform attributeName="gradientTransform" type="translate" values="0 0;0.35 0" dur="7s" repeatCount="indefinite"/></linearGradient>',
         "</defs>",
         card(W, H, rx=18, gid=f"cs{key}")]
    o.append(gt(num, 30, 62, 18, C["orange"], font="pixel"))
    o.append(gt(title, 84, 66, 34, f"url(#t{key})"))
    prompt = f"van1dal@spb ~ ❯ {cmd}"
    pw = tw(prompt, 14)
    px = W - 40 - pw
    o.append(f'<clipPath id="ty{key}"><rect x="{px - 2}" y="40" height="30" width="0">'
             f'<animate attributeName="width" values="0;0;{pw + 6:.0f};{pw + 6:.0f};0" keyTimes="0;0.08;0.35;0.92;1" dur="7s" repeatCount="indefinite"/></rect></clipPath>')
    o.append(f'<text x="{px:.0f}" y="60" font-family="{MONO}" font-size="14" clip-path="url(#ty{key})">'
             f'<tspan fill="{C["rose"]}">van1dal</tspan><tspan fill="{C["muted"]}">@</tspan><tspan fill="{C["amber"]}">spb</tspan>'
             f'<tspan fill="{C["lilac"]}"> ~ ❯ </tspan><tspan fill="{C["text"]}">{esc(cmd)}</tspan></text>')
    o.append(f'<rect x="{W - 34}" y="46" width="8" height="17" fill="{C["orange"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect x="30" y="{H - 16}" width="{W - 60}" height="3" rx="1.5" fill="url(#u{key})"/>')
    return svg(W, H, "\n".join(o), f"{num} {title}")


# ═════════════════════════════════ кассета: над чем сейчас ═════════════════════════════════

TRACKS = [
    ("gw", "GitHub in the terminal: PRs, Actions, Telegram alerts", "4:12"),
    ("kinoza-back", "team project · the Go backend", "3:40"),
    ("berth", "containers in the terminal, Bubble Tea", "2:58"),
    ("logsence", "logs over HTTP, stored in PostgreSQL", "3:21"),
]


def reel(cx, cy, tape_r, dur):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{tape_r}" fill="#2a2328"/>',
         f'<circle cx="{cx}" cy="{cy}" r="22" fill="{C["text"]}"/>',
         f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="-360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>']
    for i in range(6):
        a = math.radians(i * 60)
        o.append(f'<rect x="{cx - 3}" y="{cy - 21}" width="6" height="9" rx="1" fill="#2a2328" transform="rotate({i * 60} {cx} {cy})"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#2a2328"/><circle cx="{cx}" cy="{cy}" r="3" fill="{C["text"]}"/></g>')
    return "".join(o)


def now():
    H = 380
    o = ["<defs>", lgrad("shell", ["#232838", "#33324a", "#4a4055"], 0, 0, 1, 1),
         lgrad("stripe", GRAD), lgrad("prog", GRAD), "</defs>",
         card(W, H, gid="nowc")]
    # кассета
    x0, y0, cw, ch = 40, 40, 520, 300
    o.append(f'<rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="20" fill="url(#shell)"/>')
    o.append(f'<rect x="{x0 + 3}" y="{y0 + 3}" width="{cw - 6}" height="{ch - 6}" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.12"/>')
    for sxp, syp in ((x0 + 16, y0 + 16), (x0 + cw - 16, y0 + 16), (x0 + 16, y0 + ch - 16), (x0 + cw - 16, y0 + ch - 16)):
        o.append(f'<circle cx="{sxp}" cy="{syp}" r="5" fill="#151927"/><path d="M{sxp - 3} {syp}h6" stroke="#6b6878" stroke-width="1.5"/>')
    lx, ly, lw_, lh = x0 + 32, y0 + 26, cw - 64, 176
    o.append(f'<rect x="{lx}" y="{ly}" width="{lw_}" height="{lh}" rx="10" fill="#ece6dc"/>')
    o.append(f'<rect x="{lx}" y="{ly + 12}" width="{lw_}" height="10" fill="url(#stripe)"/>')
    o.append(gt("VAN1DAL", lx + 16, ly + 52, 22, "#151927"))
    o.append(gt("SIDE A", lx + lw_ - 16, ly + 52, 13, C["pink"], font="pixel", anchor="end"))
    o.append(f'<text x="{lx + 16}" y="{ly + 72}" font-family="{MONO}" font-size="12" fill="#6b6878">backend mixtape · autumn 2026 · spb</text>')
    # окно с плёнкой
    wx, wy, ww, wh = lx + 60, ly + 84, lw_ - 120, 80
    o.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="40" fill="#151927"/>')
    o.append(f'<rect x="{wx + 70}" y="{wy + 54}" width="{ww - 140}" height="4" fill="#2a2328"/>')
    o.append(reel(wx + 52, wy + 40, 34, 2.4))
    o.append(reel(wx + ww - 52, wy + 40, 26, 1.9))
    # низ кассеты
    o.append(f'<path d="M{x0 + 110} {y0 + ch}L{x0 + 135} {y0 + ch - 58}H{x0 + cw - 135}L{x0 + cw - 110} {y0 + ch}Z" fill="#151927" opacity="0.7"/>')
    for hx in (x0 + 170, x0 + cw - 170):
        o.append(f'<circle cx="{hx}" cy="{y0 + ch - 26}" r="7" fill="#0d1017"/>')
    o.append(f'<rect x="{x0 + cw / 2 - 18}" y="{y0 + ch - 34}" width="36" height="14" rx="3" fill="#0d1017"/>')

    # трек-лист
    rx_ = 610
    o.append(gt("NOW PLAYING", rx_, 74, 15, C["rose"], font="pixel", tracking=2))
    for i in range(5):   # эквалайзер
        bx = rx_ + gw("NOW PLAYING", 15, "pixel", 2) + 18 + i * 9
        vals = ";".join(str(v) for v in random.Random(i).sample([4, 8, 12, 16, 20, 14, 6], 5))
        o.append(f'<rect x="{bx}" y="56" width="6" height="18" fill="{GRAD[i % 3]}"><animate attributeName="height" values="{vals}" dur="{0.9 + i * 0.13:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{";".join(str(74 - int(v)) for v in vals.split(";"))}" dur="{0.9 + i * 0.13:.2f}s" repeatCount="indefinite"/></rect>')
    for i, (name, desc, t) in enumerate(TRACKS):
        y = 110 + i * 54
        cur = i == 0
        if cur:
            o.append(f'<rect x="{rx_ - 14}" y="{y - 24}" width="{W - rx_ - 26}" height="48" rx="10" fill="{C["panel2"]}" stroke="{C["pink"]}" stroke-opacity="0.6"/>')
            o.append(f'<path d="M{rx_} {y - 9}l12 7-12 7z" fill="{C["orange"]}"/>')
        else:
            o.append(gt(f"0{i + 1}", rx_, y + 4, 11, C["faint"], font="pixel"))
        o.append(gt(name, rx_ + 34, y - 1, 18, C["text"] if cur else C["soft"], font="bold"))
        o.append(f'<text x="{rx_ + 34}" y="{y + 17}" font-family="{MONO}" font-size="12.5" fill="{C["muted"]}">{esc(desc)}</text>')
        o.append(f'<text x="{W - 52}" y="{y + 5}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{C["muted"]}">{t}</text>')
    # прогресс
    py = H - 52
    o.append(f'<rect x="{rx_}" y="{py}" width="{W - rx_ - 52}" height="4" rx="2" fill="{C["line"]}"/>')
    pw = W - rx_ - 52
    o.append(f'<rect x="{rx_}" y="{py}" width="0" height="4" rx="2" fill="url(#prog)"><animate attributeName="width" values="0;{pw}" dur="24s" repeatCount="indefinite"/></rect>')
    o.append(f'<circle cx="{rx_}" cy="{py + 2}" r="6" fill="{C["text"]}"><animate attributeName="cx" values="{rx_};{rx_ + pw}" dur="24s" repeatCount="indefinite"/></circle>')
    o.append(f'<text x="{rx_}" y="{py + 26}" font-family="{MONO}" font-size="12" fill="{C["muted"]}">◀◀   ▶   ▶▶      shuffle off · repeat on</text>')
    return svg(W, H, "\n".join(o), "Now playing: gw — GitHub in the terminal; kinoza-back — team Go backend; berth — containers in the terminal; logsence — logs into PostgreSQL")


# ═════════════════════════════════ проекты ═════════════════════════════════

ART = {
    "eye": ["............", "...pppppp...", ".pp......pp.", "p..........p", "p..........p",
            "p..........p", ".pp......pp.", "...pppppp...", "............"],
    "clap": ["wkwkwkwkwkww", "kwkwkwkwkwkw", "pppppppppppp", "p..........p", "p.mmmmmm...p", "p..........p",
             "p.oooo.....p", "p..........p", "p.mmmmmmmm.p", "p..........p", "pppppppppppp"],
    "scroll": [".llllllllll.", "lwwwwwwwwwwl", "lw.mmmmm..wl", "lwwwwwwwwwwl", "lw.oooooo.wl", "lwwwwwwwwwwl",
               "lw.mmm....wl", "lwwwwwwwwwwl", "lw.ooooo..wl", "lwwwwwwwwwwl", ".llllllllll."],
    "monitor": ["pppppppppppp", "pkkkkkkkkkkp", "pkmkkkkkkkkp", "pkkmkkkkkkkp", "pkmkkooookkp", "pkkkkkkkkkkp",
                "pkkkkkkkkkkp", "pppppppppppp", "....pppp....", "..pppppppp.."],
    "heart": ["..mm....mm..", ".mmmm..mmmm.", "mmwmmmmmmmmm", "mwmmmmmmmmmm", "mmmmmmmmmmmm", "mmmmmmmmmmmm",
              ".mmmmmmmmmm.", "..mmmmmmmm..", "...mmmmmm...", "....mmmm....", ".....mm....."],
    "dog": [".a........a.", ".aa......aa.", ".aaaaaaaaaa.", "aaaaaaaaaaaa", "aakkaaaakkaa", "aaaaaaaaaaaa",
            "aaaaakkaaaaa", ".aaaakkaaaa.", "..aaaaaaaa..", "...ammmma...", "....mmmm...."],
    "box": [".oooooooooo.", "oyyyyoyyyyyo", "oooooooooooo", "oaaaamaaaaao", "oaaaamaaaaao", "oaawwwwaaaao",
            "oaawwwwaaaao", "oaaaamaaaaao", "oaaaamaaaaao", "oooooooooooo"],
}

FEATURED = dict(
    name="gw", repo="github-watcher",
    desc="GitHub in the terminal, like on the site: repos, PRs with diff and review, Actions by job and step, "
         "inbox and search. A background daemon watches GitHub and pings my phone through Telegram.",
    chips=["Go", "Bubble Tea", "go-github", "cobra", "telebot"],
)

PROJECTS = [
    dict(slug="kinoza", name="kinoza-back", owner="orionvega2343-cloud", art="clap", badge="TEAM",
         desc="A team project. I work on its Go backend together with the rest of the crew.", chips=["Go", "backend", "team"]),
    dict(slug="logsence", name="logsence", owner="van1dalgrr-arch", art="scroll", badge="Go",
         desc="Log collection service: ingest logs over HTTP, store them in PostgreSQL, query them by service.",
         chips=["Gin", "pgx + sqlx", "migrations", "Docker"]),
    dict(slug="dotfiles", name="dotfiles", owner="van1dalgrr-arch", art="monitor", badge="macOS",
         desc="My Mac for Go work: one command to set up, dot doctor checks it, berth shows containers in the terminal.",
         chips=["zsh", "Neovim", "Ghostty", "Bubble Tea"]),
    dict(slug="pulse", name="Pulse", owner="van1dalgrr-arch", art="heart", badge="Go",
         desc="A small HTTP framework for Go on top of Gin: its own Context, routing and a middleware chain.",
         chips=["Gin", "Context", "middleware"]),
    dict(slug="watchdog", name="watchdog", owner="van1dalgrr-arch", art="dog", badge="Go",
         desc="Uptime monitor: polls a service's /health every 5 seconds and reports the moment it stops answering.",
         chips=["net/http", "no framework", "Docker"]),
    dict(slug="ordergo", name="OrderGo", owner="van1dalgrr-arch", art="box", badge="Go",
         desc="REST API for orders, built toward a production layout: cmd/ + internal/, PostgreSQL, Compose.",
         chips=["Gin", "PostgreSQL", "Compose", "Makefile"]),
]


def featured():
    p = FEATURED
    H = 400
    o = ["<defs>", lgrad("fg", GRAD), glow("fglow", 5, 0.3), "</defs>", card(W, H, gid="fcard")]
    o.append(gt("FEATURED", 40, 56, 12, C["orange"], font="pixel", tracking=2))
    # глаз: зрачок оглядывается
    ex, ey, s = 40, 82, 9
    o.append(pixels(ART["eye"], ex, ey, s))
    o.append(f'<g shape-rendering="crispEdges"><animateTransform attributeName="transform" type="translate" '
             f'values="0 0;0 0;-{2 * s} 0;-{2 * s} 0;{2 * s} 0;{2 * s} 0;0 0" keyTimes="0;0.2;0.3;0.5;0.6;0.85;1" dur="5s" repeatCount="indefinite"/>'
             f'<rect x="{ex + 4 * s}" y="{ey + 3 * s}" width="{4 * s}" height="{3 * s}" fill="{C["pink"]}"/>'
             f'<rect x="{ex + 5 * s}" y="{ey + 3 * s}" width="{2 * s}" height="{3 * s}" fill="{C["night"]}"/>'
             f'<rect x="{ex + 5 * s}" y="{ey + 3 * s}" width="{s}" height="{s}" fill="{C["text"]}"/></g>')
    o.append(f'<rect x="{ex}" y="{ey + 3 * s}" width="{12 * s}" height="0" fill="{C["bg"]}"><animate attributeName="height" values="0;0;{3 * s};0;0" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite"/></rect>')
    tx = 190
    o.append(gt(p["name"], tx, 140, 72, "url(#fg)", extra=' filter="url(#fglow)"'))
    o.append(f'<text x="{tx + 4}" y="170" font-family="{MONO}" font-size="14" fill="{C["muted"]}">van1dalgrr-arch/{p["repo"]}</text>')
    y = 214
    for line in wrap(p["desc"], 16, 470):
        o.append(f'<text x="40" y="{y}" font-family="{SANS}" font-size="16" fill="{C["soft"]}">{esc(line)}</text>')
        y += 25
    o.append(chips(p["chips"], 40, H - 78))
    o.append(f'<text x="40" y="{H - 24}" font-family="{MONO}" font-size="12" fill="{C["muted"]}">go install github.com/van1dalgrr-arch/github-watcher/cmd/gw@latest</text>')

    # окно TUI: курсор ходит по списку PR
    wx, wy, ww, wh = 600, 60, 560, 280
    o.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="12" fill="{C["night"]}" stroke="{C["line"]}"/>')
    o.append(f'<path d="M{wx} {wy + 12}a12 12 0 0 1 12-12h{ww - 24}a12 12 0 0 1 12 12v18h-{ww}z" fill="{C["panel2"]}"/>')
    for i, c in enumerate((C["pink"], C["orange"], C["lilac"])):
        o.append(f'<circle cx="{wx + 18 + i * 17}" cy="{wy + 15}" r="5" fill="{c}"/>')
    o.append(f'<text x="{wx + ww / 2}" y="{wy + 20}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{C["muted"]}">gw — me/api</text>')
    t = lambda x, y, s_, col, extra="": f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="12" fill="{col}" xml:space="preserve"{extra}>{s_}</text>'
    o.append(t(wx + 16, wy + 54, f'<tspan fill="{C["pink"]}">◆ gw</tspan>  me/api', C["text"]))
    o.append(t(wx + ww - 16, wy + 54, f'@me  <tspan fill="{C["amber"]}">✉ 2</tspan>  <tspan fill="{C["green"]}">● daemon</tspan>', C["muted"], ' text-anchor="end"'))
    tabs = ["1 Dashboard", "2 Repos", "3 PRs 2", "4 Issues", "5 Actions", "9 Inbox 2"]
    tx_ = wx + 16
    for i, tb in enumerate(tabs):
        col = C["night"] if i == 2 else C["muted"]
        w_ = tw(tb, 12) + 12
        if i == 2:
            o.append(f'<rect x="{tx_ - 6}" y="{wy + 64}" width="{w_}" height="20" rx="4" fill="{C["rose"]}"/>')
        o.append(t(tx_, wy + 78, esc(tb), col))
        tx_ += w_ + 6
    o.append(t(wx + 16, wy + 112, "Pull requests · open · 2", C["lilac"]))
    rows = [("#7", "✓", C["green"], "Add cache", "feat/cache → main", "@alice", "1h"),
            ("#6", "✗", C["pink"], "Fix login", "fix/login → main", "@bob", "3h"),
            ("#5", "✓", C["green"], "CI: govulncheck", "ci/vuln → main", "@me", "1d")]
    ry = wy + 140
    o.append(f'<rect x="{wx + 10}" y="{ry - 17}" width="{ww - 20}" height="26" rx="5" fill="{C["violet"]}" fill-opacity="0.35" stroke="{C["pink"]}" stroke-opacity="0.7">'
             f'<animate attributeName="y" values="{ry - 17};{ry - 17};{ry + 13};{ry + 13};{ry + 43};{ry + 43};{ry - 17}" keyTimes="0;0.28;0.33;0.61;0.66;0.95;1" dur="6s" repeatCount="indefinite"/></rect>')
    for i, (n, st, sc, title, br, who, ago) in enumerate(rows):
        y = ry + i * 30
        o.append(t(wx + 20, y, f'<tspan fill="{C["pink"]}">◆</tspan> {n:<4} <tspan fill="{sc}">{st}</tspan> {esc(title):<17}<tspan fill="{C["muted"]}">{esc(br):<19}{who:<8}{ago}</tspan>', C["text"]))
    o.append(t(wx + ww - 16, wy + wh - 18, f'<tspan fill="{C["rose"]}">enter</tspan> open  <tspan fill="{C["rose"]}">m</tspan> merge  <tspan fill="{C["rose"]}">c</tspan> comment  <tspan fill="{C["rose"]}">?</tspan> help', C["muted"], ' text-anchor="end"'))
    return svg(W, H, "\n".join(o), "Featured: gw — GitHub in the terminal with a daemon that sends Telegram alerts")


def project(i, p):
    w, h = 590, 300
    o = ["<defs>", lgrad(f"pg{i}", GRAD), "</defs>", card(w, h, gid=f"pc{i}")]
    s = 6
    art = ART[p["art"]]
    anim = ('<animateTransform attributeName="transform" type="scale" values="1;1.12;1;1.08;1" keyTimes="0;0.12;0.24;0.36;1" dur="1.4s" repeatCount="indefinite" additive="sum"/>'
            if p["art"] == "heart" else
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="{1.8 + i * 0.2:.1f}s" repeatCount="indefinite"/>')
    ax, ay = 34, 34
    if p["art"] == "heart":   # сердце бьётся из своего центра
        cx, cy = ax + 6 * s, ay + 5.5 * s
        o.append(f'<g transform="translate({cx} {cy})"><g>{anim}{pixels(art, -6 * s, -5.5 * s, s)}</g></g>')
    else:
        o.append(f'<g>{anim}{pixels(art, ax, ay, s)}</g>')
    o.append(f'<ellipse cx="{ax + 6 * s}" cy="{ay + 12 * s + 8}" rx="{4 * s}" ry="3" fill="{C["violet"]}" opacity="0.35"/>')
    # бейдж
    b = p["badge"]
    bw = gw(b, 10, "pixel", 1) + 22
    team = b == "TEAM"
    o.append(f'<rect x="{w - 30 - bw:.0f}" y="34" width="{bw:.0f}" height="26" rx="6" fill="{C["pink"] if team else C["panel2"]}" stroke="{C["pink"] if team else C["line"]}"/>')
    o.append(gt(b, w - 30 - bw / 2, 52, 10, C["night"] if team else C["soft"], font="pixel", anchor="middle", tracking=1))
    o.append(gt(p["name"], 130, 70, 30, C["text"]))
    o.append(f'<text x="131" y="96" font-family="{MONO}" font-size="12.5" fill="{C["muted"]}">{esc(p["owner"])}</text>')
    y = 142
    for line in wrap(p["desc"], 15.5, w - 70)[:3]:
        o.append(f'<text x="34" y="{y}" font-family="{SANS}" font-size="15.5" fill="{C["soft"]}">{esc(line)}</text>')
        y += 24
    o.append(chips(p["chips"], 34, h - 84))
    o.append(f'<rect x="34" y="{h - 40}" width="{w - 68}" height="1" fill="{C["line"]}"/>')
    o.append(f'<text x="34" y="{h - 16}" font-family="{MONO}" font-size="12" fill="{C["muted"]}">{"team project" if team else "github.com/" + p["owner"] + "/" + p["name"]}</text>')
    o.append(f'<text x="{w - 34}" y="{h - 16}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{C["rose"]}">open →</text>')
    return svg(w, h, "\n".join(o), f'{p["name"]}: {p["desc"]}')


# ═════════════════════════════════ стек ═════════════════════════════════

STACK = [("go", "Go"), ("gin", "Gin"), ("postgresql", "PostgreSQL"), ("redis", "Redis"), ("docker", "Docker"), ("githubactions", "Actions"),
         ("linux", "Linux"), ("git", "Git"), ("gnubash", "Bash · zsh"), ("neovim", "Neovim"), ("openjdk", "Java"), ("spring", "Spring Boot")]


def stack():
    H = 344
    o = [card(W, H, gid="stc")]
    cols, tw_, th_, gap = 6, 172, 118, 18
    x0 = (W - cols * tw_ - (cols - 1) * gap) / 2
    for i, (ic, label) in enumerate(STACK):
        r, c = divmod(i, cols)
        x, y = x0 + c * (tw_ + gap), 36 + r * (th_ + gap)
        acc = GRAD[(c + r) % 3]
        o.append(f'<rect x="{x:.0f}" y="{y}" width="{tw_}" height="{th_}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}"/>')
        # подсветка бежит по плиткам волной
        o.append(f'<rect x="{x:.0f}" y="{y}" width="{tw_}" height="{th_}" rx="14" fill="{acc}" fill-opacity="0.08" stroke="{acc}" stroke-width="1.2" opacity="0">'
                 f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;0.1;0.25;1" dur="9s" begin="{(c + r * 2) * 0.5:.2f}s" repeatCount="indefinite"/></rect>')
        o.append(icon(ic, x + tw_ / 2 - 20, y + 22, 40, C["text"]))
        o.append(f'<text x="{x + tw_ / 2:.0f}" y="{y + 92}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{C["soft"]}">{esc(label)}</text>')
        o.append(f'<rect x="{x + tw_ / 2 - 14:.0f}" y="{y + th_ - 10}" width="28" height="3" rx="1.5" fill="{acc}"/>')
    o.append(f'<text x="{W / 2}" y="{H - 20}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{C["muted"]}">'
             f'also: golangci-lint · govulncheck · hadolint · gitleaks · Bubble Tea · OrbStack · lazygit</text>')
    return svg(W, H, "\n".join(o), "Stack: Go, Gin, PostgreSQL, Redis, Docker, GitHub Actions, Linux, Git, Bash, Neovim, Java, Spring Boot")


# ═════════════════════════════════ финал: see you space cowboy ═════════════════════════════════

def footer():
    H, hz = 320, 150
    o = ["<defs>", lgrad("fsky", ["#090b11", "#1f2130", "#544a5e"], 0, 0, 0, 1),
         lgrad("fsun", [C["sun"], C["amber"], C["pink"]], 0, 0, 0, 1),
         f'<clipPath id="fclip"><rect width="{W}" height="{H}" rx="22"/></clipPath>',
         f'<clipPath id="fskyc"><rect width="{W}" height="{hz}"/></clipPath>', glow("tglow", 4, 0.35), "</defs>",
         '<g clip-path="url(#fclip)">',
         f'<rect width="{W}" height="{H}" fill="{C["night"]}"/>',
         f'<rect width="{W}" height="{hz}" fill="url(#fsky)"/>',
         stars(40, W, hz - 50, seed=9),
         f'<g clip-path="url(#fskyc)"><circle cx="{W / 2}" cy="{hz + 10}" r="70" fill="url(#fsun)"/></g>']
    # горы
    rnd = random.Random(2)
    pts = [(0, hz)]
    x = 0
    while x < W:
        x += rnd.randint(40, 90)
        pts.append((x, hz - rnd.randint(8, 46)))
    pts.append((W, hz))
    o.append(f'<path d="M{" L".join(f"{a} {b}" for a, b in pts)}Z" fill="#11131c"/>')
    # сетка в перспективе, едет на зрителя
    vx = W / 2
    for i in range(-14, 15):
        o.append(f'<line x1="{vx + i * 18}" y1="{hz}" x2="{vx + i * 170}" y2="{H}" stroke="{C["violet"]}" stroke-opacity="0.4" stroke-width="1"/>')
    ys = [hz + (H - hz) * (k / 10) ** 2 for k in range(1, 12)]
    for k in range(len(ys) - 1):
        o.append(f'<line x1="0" x2="{W}" y1="{ys[k]:.1f}" y2="{ys[k]:.1f}" stroke="{C["violet"]}" stroke-opacity="0.4" stroke-width="1">'
                 f'<animate attributeName="y1" values="{ys[k]:.1f};{ys[k + 1]:.1f}" dur="1.2s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y2" values="{ys[k]:.1f};{ys[k + 1]:.1f}" dur="1.2s" repeatCount="indefinite"/></line>')
    o.append(f'<rect y="{hz}" width="{W}" height="1.5" fill="{C["rose"]}" opacity="0.7"/>')
    o.append(f'<rect x="{W / 2 - 330}" y="200" width="660" height="80" rx="14" fill="{C["night"]}" fill-opacity="0.82"/>')
    o.append(f'<g>{gt("SEE YOU SPACE COWBOY...", W / 2, 248, 28, C["text"], font="bold", anchor="middle", tracking=3, extra=' filter="url(#tglow)"')}'
             '<animate attributeName="opacity" values="1;1;0.4;1;1;0.7;1" keyTimes="0;0.6;0.62;0.64;0.9;0.92;1" dur="5s" repeatCount="indefinite"/></g>')
    o.append(f'<text x="{W / 2}" y="270" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{C["muted"]}">thanks for stopping by · write in English or Russian</text>')
    o.append(scanlines(W, H, "fscan"))
    o.append("</g>")
    return svg(W, H, "\n".join(o), "See you space cowboy — thanks for stopping by")


def main():
    write("hero", hero())
    write("now", now())
    write("featured", featured())
    write("stack", stack())
    write("footer", footer())
    for k in SECTIONS:
        write("h-" + k, header(k))
    for i, p in enumerate(PROJECTS):
        write("p-" + p["slug"], project(i, p))
    print("assets: ok")


if __name__ == "__main__":
    main()
