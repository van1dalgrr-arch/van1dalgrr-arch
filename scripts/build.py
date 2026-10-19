#!/usr/bin/env python3
"""Рисует статичные картинки профиля в assets/ (тёмная и светлая версии):  python3 scripts/build.py

Тексты лежат здесь обычными списками (INTRO, FEATURED, PROJECTS, STACK) — поправил строку,
перезапустил скрипт, закоммитил. Живую статистику рисует stats.py в workflow.
"""
from kit import ROOT, MONO, SANS, THEMES, arrow, esc, frame, gopher, gt, gw, icon, svg, tw, write

W = 1200


def wrap(s, size, width):
    lines, cur = [], ""
    for word in s.split():
        nxt = f"{cur} {word}".strip()
        if tw(nxt, size) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = nxt
    return lines + [cur]


def para(s, x, y, size, width, color, lh=1.55, limit=4):
    out = []
    for line in wrap(s, size, width)[:limit]:
        out.append(f'<text x="{x}" y="{y:.0f}" font-family="{SANS}" font-size="{size}" fill="{color}">{esc(line)}</text>')
        y += size * lh
    return "".join(out), y


def dots(t, x0, y0, w, h, step=22, gid="fade"):
    """Точечная сетка, которая растворяется к краям."""
    pts = "".join(f'<circle cx="{x}" cy="{y}" r="1.1"/>' for x in range(x0, x0 + w, step) for y in range(y0, y0 + h, step))
    return (f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="{gid}m"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#{gid})"/></mask></defs>'
            f'<g fill="{t["dot"]}" mask="url(#{gid}m)">{pts}</g>'
            f'<defs><radialGradient id="{gid}s" cx="0" cy="0.5" r="0.32"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            f'<animate attributeName="cx" values="-0.3;1.3" dur="9s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="0.2;0.8;0.2" dur="13s" repeatCount="indefinite"/></radialGradient>'
            f'<mask id="{gid}sm"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#{gid}s)"/></mask></defs>'
            f'<g mask="url(#{gid}m)"><g fill="{t["accent"]}" opacity="0.8" mask="url(#{gid}sm)">{pts}</g></g>')


# ═══════════════════════════════ шапка ═══════════════════════════════

INTRO = dict(
    status="Building gw — GitHub in the terminal",
    name="van1dal",
    role="Go backend developer in Saint Petersburg.",
    about="I build REST services with Gin, PostgreSQL, Redis and Docker: tested, linted and shipped through CI on every push.",
)

CODE = [   # (отступ, [(текст, роль)]) — роль: kw ключевое слово, str строка, fn вызов, t обычный
    (0, [("package", "kw"), (" main", "t")]),
    (0, []),
    (0, [("func", "kw"), (" main", "fn"), ("() {", "t")]),
    (1, [("r := gin.", "t"), ("Default", "fn"), ("()", "t")]),
    (1, [("r.", "t"), ("GET", "fn"), ("(", "t"), ('"/health"', "str"), (", health)", "t")]),
    (1, [("r.", "t"), ("POST", "fn"), ("(", "t"), ('"/logs"', "str"), (", ingest)", "t")]),
    (1, [("r.", "t"), ("Run", "fn"), ("(", "t"), ('":8080"', "str"), (")", "t")]),
    (0, [("}", "t")]),
]


BUILD = ["REST APIs in Go", "terminal tools", "CI that says no", "my own dev setup"]


def wireframe(t, cx, cy, r, T=28, frames=72):
    """Икосаэдр из тонких линий медленно вращается; координаты посчитаны на каждый кадр заранее."""
    import math
    ph = (1 + 5 ** 0.5) / 2
    V = [(-1, ph, 0), (1, ph, 0), (-1, -ph, 0), (1, -ph, 0), (0, -1, ph), (0, 1, ph), (0, -1, -ph), (0, 1, -ph),
         (ph, 0, -1), (ph, 0, 1), (-ph, 0, -1), (-ph, 0, 1)]
    n = math.sqrt(1 + ph * ph)
    V = [(x / n, y / n, z / n) for x, y, z in V]
    E = sorted({tuple(sorted((i, j))) for i in range(12) for j in range(12) if i != j
                and abs(sum((V[i][k] - V[j][k]) ** 2 for k in range(3)) - (2 / n) ** 2) < 1e-6})
    proj = []
    for f in range(frames + 1):
        a, b = 2 * math.pi * f / frames, 0.42   # поворот вокруг вертикали и постоянный наклон
        pts = []
        for x, y, z in V:
            x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
            y, z = y * math.cos(b) - z * math.sin(b), y * math.sin(b) + z * math.cos(b)
            k = 1 / (1.9 - z * 0.45)   # лёгкая перспектива
            pts.append((cx + x * r * k * 1.6, cy + y * r * k * 1.6, z))
        proj.append(pts)
    o = [f'<g stroke="{t["accent"]}" stroke-width="1.2" fill="none" stroke-linecap="round">']
    for i, j in E:
        attrs = []
        for nm, idx, c in (("x1", i, 0), ("y1", i, 1), ("x2", j, 0), ("y2", j, 1)):
            vals = ";".join(f"{fr[idx][c]:.1f}" for fr in proj)
            attrs.append(f'<animate attributeName="{nm}" values="{vals}" dur="{T}s" repeatCount="indefinite"/>')
        op = ";".join(f"{0.18 + 0.5 * (1 + (fr[i][2] + fr[j][2]) / 2) / 2:.2f}" for fr in proj)   # дальние рёбра бледнее
        p0 = proj[0]
        o.append(f'<line x1="{p0[i][0]:.1f}" y1="{p0[i][1]:.1f}" x2="{p0[j][0]:.1f}" y2="{p0[j][1]:.1f}">{"".join(attrs)}'
                 f'<animate attributeName="stroke-opacity" values="{op}" dur="{T}s" repeatCount="indefinite"/></line>')
    o.append("</g>")
    for v in range(12):
        xs = ";".join(f"{fr[v][0]:.1f}" for fr in proj)
        ys = ";".join(f"{fr[v][1]:.1f}" for fr in proj)
        o.append(f'<circle r="2.6" fill="{t["accent"]}" cx="{proj[0][v][0]:.1f}" cy="{proj[0][v][1]:.1f}">'
                 f'<animate attributeName="cx" values="{xs}" dur="{T}s" repeatCount="indefinite"/><animate attributeName="cy" values="{ys}" dur="{T}s" repeatCount="indefinite"/></circle>')
    # две орбиты вокруг
    for k, (rx_, ry_, rot, d) in enumerate(((r * 1.55, r * 0.42, -18, 40), (r * 1.3, r * 0.3, 24, 55))):
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx_:.0f}" ry="{ry_:.0f}" fill="none" stroke="{t["muted"]}" stroke-opacity="0.35" stroke-dasharray="2 7" transform="rotate({rot} {cx} {cy})">'
                 f'<animate attributeName="stroke-dashoffset" values="0;{-90 if k else 90}" dur="{d / 4:.0f}s" repeatCount="indefinite"/></ellipse>')
    return "".join(o)


def hero(theme):
    t = THEMES[theme]
    H = 470
    o = [frame(W, H, t, rx=24, n=4, seed=3)]
    o.append(wireframe(t, 930, 170, 150))
    # статус: стеклянная плашка, зелёная точка пульсирует
    st = INTRO["status"]
    pw = tw(st, 13) * 0.9 + 40
    o.append(f'<rect x="56" y="58" width="{pw:.0f}" height="30" rx="15" fill="{t["glass"]}" fill-opacity="{t["glass_op"] * 2:.3f}" stroke="{t["line2"]}"/>')
    o.append(f'<circle cx="74" cy="73" r="7" fill="{t["green"]}" opacity="0.25"><animate attributeName="r" values="4;8;4" dur="2.4s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.35;0;0.35" dur="2.4s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="74" cy="73" r="3.5" fill="{t["green"]}"/>')
    o.append(f'<text x="88" y="77.5" font-family="{SANS}" font-size="13" fill="{t["soft"]}">{esc(st)}</text>')
    o.append(gt(INTRO["name"], 50, 200, 110, t["text"], tracking=-4.5))
    o.append(gt(INTRO["role"], 56, 252, 26, t["soft"], font="body", tracking=-0.4))
    o.append(f'<rect x="56" y="268" width="64" height="2" rx="1" fill="{t["accent"]}"><animate attributeName="width" values="64;200;64" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/></rect>')
    s, _ = para(INTRO["about"], 56, 306, 16, 540, t["muted"])
    o.append(s)
    # «I build …» — слово меняется по кругу, выезжая снизу
    yb = 380
    o.append(f'<text x="56" y="{yb}" font-family="{SANS}" font-size="15" fill="{t["muted"]}">I build</text>')
    o.append(f'<clipPath id="rot"><rect x="110" y="{yb - 18}" width="300" height="24"/></clipPath><g clip-path="url(#rot)">')
    n = len(BUILD)
    for i, wd in enumerate(BUILD):
        a0, a1 = i / n, (i + 1) / n
        vals = "0 24;0 24;0 0;0 0;0 -24;0 -24" if i else "0 0;0 0;0 -24;0 -24;0 24;0 0"
        # моменты не должны выходить за 1, иначе браузер выбрасывает анимацию целиком
        kts = (f"0;{a0:.3f};{a0 + 0.03:.3f};{a1 - 0.015:.3f};{min(a1 + 0.015, 1):.3f};1" if i else
               f"0;{a1 - 0.015:.3f};{a1 + 0.015:.3f};0.985;0.986;1")
        base = "" if i == 0 else ' transform="translate(0 24)"'   # без анимации видно только первое слово
        o.append(f'<g{base}><animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kts}" dur="{n * 2.6}s" repeatCount="indefinite"/>'
                 f'<text x="112" y="{yb}" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["text"]}">{esc(wd)}</text></g>')
    o.append("</g>")

    # стеклянная карточка с кодом поверх каркаса
    cx, cy, cw, ch = 652, 116, 420, 236
    o.append(f'<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000" flood-opacity="{t["shadow"]}"/></filter></defs>')
    o.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" fill="{t["panel"]}" fill-opacity="0.72" stroke="{t["line2"]}" filter="url(#sh)"/>')
    o.append(f'<rect x="{cx + 0.5}" y="{cy + 0.5}" width="{cw - 1}" height="{ch - 1}" rx="13.5" fill="none" stroke="{t["rim"]}" stroke-opacity="{t["rim_op"] * 0.6:.2f}"/>')
    o.append(f'<line x1="{cx}" y1="{cy + 38}" x2="{cx + cw}" y2="{cy + 38}" stroke="{t["line2"]}"/>')
    for i in range(3):
        o.append(f'<circle cx="{cx + 20 + i * 16}" cy="{cy + 19}" r="4.5" fill="{t["line2"]}"/>')
    o.append(f'<text x="{cx + cw - 18}" y="{cy + 23.5}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">cmd/api/main.go</text>')
    col = {"kw": t["kw"], "str": t["str"], "fn": t["accent"], "t": t["soft"]}
    T, clock, y = 14.0, 0.6, cy + 66
    for n_, (ind, parts) in enumerate(CODE):
        o.append(f'<text x="{cx + 20}" y="{y}" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{n_ + 1}</text>')
        text = "".join(s_ for s_, _ in parts)
        x0 = cx + 48 + ind * 29
        full = tw(text, 14, mono=True) + 6
        st_, dur = clock, max(0.05, 0.05 * len(text))
        clock += dur + 0.15
        o.append(f'<clipPath id="cl{n_}"><rect x="{x0 - 2}" y="{y - 16}" width="{full:.0f}" height="22">'
                 f'<animate attributeName="width" values="0;0;{full:.0f};{full:.0f};0" keyTimes="0;{st_ / T:.4f};{(st_ + dur) / T:.4f};0.94;1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        spans = "".join(f'<tspan fill="{col[r]}">{esc(s_)}</tspan>' for s_, r in parts)
        o.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="14" xml:space="preserve" clip-path="url(#cl{n_})">{spans}</text>')
        y += 21
    # гофер vim-go парит у края карточки
    img, gwid = gopher("vim-go", 0, 0, 200)
    gx, gy = 948, 252
    o.append(f'<ellipse cx="{gx + gwid / 2:.0f}" cy="{gy + 205}" rx="{gwid * 0.32:.0f}" ry="7" fill="#000" opacity="{t["shadow"] * 0.6:.2f}">'
             '<animate attributeName="rx" values="62;52;62" dur="4s" repeatCount="indefinite"/></ellipse>')
    o.append(f'<g transform="translate({gx} {gy})"><g><animateTransform attributeName="transform" type="translate" values="0 0;0 -10;0 0" dur="4s" repeatCount="indefinite" '
             f'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>{img}</g></g>')
    return svg(W, H, "\n".join(o), f'{INTRO["name"]} — {INTRO["role"]} {INTRO["about"]}')


# ═══════════════════════════════ проекты ═══════════════════════════════

FEATURED = dict(
    name="gw", repo="van1dalgrr-arch/github-watcher",
    desc="GitHub in the terminal, the way it looks on the site: repos, pull requests with diff and review, "
         "Actions by job and step, inbox and search. A background daemon watches GitHub and sends what matters to my phone through Telegram.",
    tags=["Go", "Bubble Tea", "go-github", "cobra", "telebot"],
)

PROJECTS = [
    dict(slug="kinoza", name="kinoza-back", repo="orionvega2343-cloud/kinoza-back", team=True,
         desc="Team project. I work on its Go backend together with the rest of the team.", tags=["Go", "backend"]),
    dict(slug="logsence", name="logsence", repo="van1dalgrr-arch/logsence",
         desc="Log collection service: ingest logs over HTTP, store them in PostgreSQL, query them by service.",
         tags=["Go", "Gin", "PostgreSQL", "Docker"]),
    dict(slug="dotfiles", name="dotfiles", repo="van1dalgrr-arch/dotfiles",
         desc="My Mac for Go work: one command to set up, dot doctor to check it, berth for containers in the terminal.",
         tags=["zsh", "Neovim", "Go", "Swift"]),
    dict(slug="pulse", name="Pulse", repo="van1dalgrr-arch/Pulse",
         desc="A small HTTP framework for Go on top of Gin: its own Context, routing and a middleware chain.",
         tags=["Go", "Gin"]),
    dict(slug="watchdog", name="watchdog", repo="van1dalgrr-arch/watchdog",
         desc="Uptime monitor: polls a service's /health every 5 seconds and reports when it stops answering.",
         tags=["Go", "net/http", "Docker"]),
    dict(slug="ordergo", name="OrderGo", repo="van1dalgrr-arch/OrderGo",
         desc="REST API for orders, built toward a production layout: cmd/ and internal/, PostgreSQL, Compose.",
         tags=["Go", "Gin", "PostgreSQL"]),
]


def tags(items, x, y, t):
    """Теги одной строкой через точку; перед первым — цветная точка, как у языка на GitHub."""
    o = [f'<circle cx="{x + 5}" cy="{y - 4.5}" r="5" fill="{t["accent"]}"/>']
    x += 18
    for i, it in enumerate(items):
        if i:
            o.append(f'<text x="{x:.0f}" y="{y}" font-family="{SANS}" font-size="13" fill="{t["faint"]}">·</text>')
            x += 14
        o.append(f'<text x="{x:.0f}" y="{y}" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{esc(it)}</text>')
        x += tw(it, 13) + 10
    return "".join(o)


def featured(theme):
    t = THEMES[theme]
    p, H = FEATURED, 300
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    o.append(f'<text x="44" y="58" font-family="{SANS}" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t["accent"]}">FEATURED</text>')
    o.append(gt(p["name"], 42, 114, 48, t["text"], tracking=-1.5))
    o.append(f'<text x="{44 + gw(p["name"], 48, tracking=-1.5) + 16:.0f}" y="112" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{p["repo"]}</text>')
    s, _ = para(p["desc"], 44, 156, 15.5, 520, t["soft"], limit=5)
    o.append(s)
    o.append(tags(p["tags"], 44, H - 40, t))
    o.append(arrow(W - 50, 40, 12, t["muted"]))

    # срез интерфейса gw: подсветка неспешно переходит по строкам
    x, y, w, h = 626, 50, 500, 214
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    T = lambda xx, yy, s_, c, extra="": f'<text x="{xx}" y="{yy}" font-family="{MONO}" font-size="12.5" fill="{c}" xml:space="preserve"{extra}>{s_}</text>'
    o.append(T(x + 18, y + 30, f'<tspan fill="{t["text"]}">gw</tspan>  me/api', t["muted"]))
    o.append(T(x + w - 18, y + 30, f'✉ 2   <tspan fill="{t["green"]}">●</tspan> daemon', t["muted"], ' text-anchor="end"'))
    o.append(T(x + 18, y + 56, f'Dashboard  Repos  <tspan fill="{t["text"]}">Pull requests 2</tspan>  Issues  Actions', t["muted"]))
    o.append(f'<line x1="{x}" y1="{y + 70}" x2="{x + w}" y2="{y + 70}" stroke="{t["line"]}"/>')
    rows = [("#7", "✓", t["green"], "Add cache", "feat/cache", "1h"),
            ("#6", "✗", "#e5534b", "Fix login", "fix/login", "3h"),
            ("#5", "✓", t["green"], "CI: govulncheck", "ci/vuln", "1d")]
    ry = y + 100
    o.append(f'<rect x="{x + 8}" y="{ry - 18}" width="{w - 16}" height="28" rx="6" fill="{t["accent"]}" fill-opacity="0.1">'
             f'<animate attributeName="y" values="{ry - 18};{ry - 18};{ry + 14};{ry + 14};{ry + 46};{ry + 46};{ry - 18}" '
             f'keyTimes="0;0.3;0.34;0.63;0.67;0.96;1" dur="9s" repeatCount="indefinite"/></rect>')
    for i, (n, st, sc, title, br, ago) in enumerate(rows):
        yy = ry + i * 32
        o.append(T(x + 22, yy, f'{n}  <tspan fill="{sc}">{st}</tspan>  <tspan fill="{t["text"]}">{esc(title):<17}</tspan>{br:<13}{ago}', t["muted"]))
    o.append(T(x + w - 18, y + h - 16, 'enter open · m merge · ? help', t["faint"], ' text-anchor="end"'))
    # уведомление в Telegram: выезжает справа, висит, уходит
    tx, ty, tw_, th = x + w - 268, y + h - 84, 290, 56
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.35;0.4;0.75;0.8;1" dur="9s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="translate" values="40 0;40 0;0 0;0 0;40 0;40 0" keyTimes="0;0.35;0.4;0.75;0.8;1" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.2 0.8 0.3 1;0 0 1 1;0.5 0 0.8 0.2;0 0 1 1"/>'
             f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th}" rx="12" fill="{t["panel"]}" stroke="{t["line2"]}"/>'
             f'{icon("telegram", tx + 14, ty + 15, 26, t["accent"])}'
             f'<text x="{tx + 52}" y="{ty + 24}" font-family="{SANS}" font-size="13" font-weight="600" fill="{t["text"]}">gw</text>'
             f'<text x="{tx + 76}" y="{ty + 24}" font-family="{SANS}" font-size="12" fill="{t["faint"]}">now</text>'
             f'<text x="{tx + 52}" y="{ty + 42}" font-family="{SANS}" font-size="12.5" fill="{t["soft"]}">#7 Add cache — all checks passed ✓</text></g>')
    return svg(W, H, "\n".join(o), f'Featured: gw — {p["desc"]}')


# ── маленькие живые иллюстрации для карточек: (x, y) — левый верхний угол окна 176×150

def art_watchdog(t, x, y):
    """Кардиограмма сервиса: бежит линия пульса, раз в пять секунд — запрос к /health."""
    beat = "h22l6 -18l7 34l6 -26l5 10h22"   # один удар, 68 по ширине
    d = f"M{x - 68} {y + 78}" + beat * 6
    o = [f'<clipPath id="ecg"><rect x="{x + 1}" y="{y + 1}" width="174" height="148" rx="10"/></clipPath><g clip-path="url(#ecg)">',
         f'<path d="{d}" fill="none" stroke="{t["green"]}" stroke-width="1.8" stroke-linejoin="round">'
         f'<animateTransform attributeName="transform" type="translate" values="0 0;68 0" dur="1.6s" repeatCount="indefinite"/></path></g>',
         f'<text x="{x + 14}" y="{y + 26}" font-family="{MONO}" font-size="11" fill="{t["muted"]}">GET /health</text>',
         f'<text x="{x + 162}" y="{y + 26}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["green"]}">200<animate attributeName="opacity" values="1;0.3;1" dur="5s" repeatCount="indefinite"/></text>',
         f'<text x="{x + 14}" y="{y + 136}" font-family="{MONO}" font-size="11" fill="{t["faint"]}">every 5s</text>',
         f'<circle cx="{x + 158}" cy="{y + 132}" r="4" fill="{t["green"]}"><animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/></circle>']
    return "".join(o)


def art_logsence(t, x, y):
    """Логи бегут вверх строками: уровень и сообщение."""
    lv = [("INFO", t["accent"], 0.7), ("WARN", t["kw"], 0.5), ("INFO", t["accent"], 0.85), ("ERROR", "#e5534b", 0.6),
          ("INFO", t["accent"], 0.45), ("DEBUG", t["muted"], 0.75)]
    rows = lv + lv[:6]
    o = [f'<clipPath id="lg"><rect x="{x + 1}" y="{y + 1}" width="174" height="148" rx="10"/></clipPath><g clip-path="url(#lg)"><g>',
         f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {-len(lv) * 22}" dur="{len(lv) * 1.2}s" repeatCount="indefinite"/>']
    for i, (name, c, ln) in enumerate(rows):
        yy = y + 24 + i * 22
        o.append(f'<text x="{x + 14}" y="{yy}" font-family="{MONO}" font-size="10.5" fill="{c}">{name}</text>'
                 f'<rect x="{x + 62}" y="{yy - 7}" width="{100 * ln:.0f}" height="6" rx="3" fill="{t["line2"]}"/>')
    o.append("</g></g>")
    return "".join(o)


def art_ordergo(t, x, y):
    """Заказ проходит статусы: точка заполняет шаги по очереди."""
    steps = ["created", "paid", "shipped", "delivered"]
    T = 8
    o = [f'<line x1="{x + 30}" y1="{y + 26}" x2="{x + 30}" y2="{y + 26 + 3 * 32}" stroke="{t["line2"]}" stroke-width="2"/>',
         f'<rect x="{x + 29}" y="{y + 26}" width="2" height="{3 * 32}" fill="{t["accent"]}"><animate attributeName="height" values="0;{3 * 32};{3 * 32};0" keyTimes="0;0.75;0.95;1" dur="{T}s" repeatCount="indefinite"/></rect>']
    for i, st in enumerate(steps):
        yy = y + 26 + i * 32
        at = 0.75 * i / 3
        o.append(f'<circle cx="{x + 30}" cy="{yy}" r="7" fill="{t["bg"]}" stroke="{t["line2"]}" stroke-width="2"/>')
        o.append(f'<circle cx="{x + 30}" cy="{yy}" r="7" fill="{t["accent"]}"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{at:.3f};{at + 0.02:.3f};0.95;1" dur="{T}s" repeatCount="indefinite"/></circle>')
        o.append(f'<text x="{x + 48}" y="{yy + 4}" font-family="{MONO}" font-size="11.5" fill="{t["soft"]}">{st}</text>')
    o.append(f'<text x="{x + 162}" y="{y + 30}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{t["faint"]}">#1042</text>')
    return "".join(o)


def art_pulse(t, x, y):
    """Запрос проходит цепочку middleware и возвращается ответом."""
    chain = ["Logger", "Recovery", "Auth", "Handler"]
    T = 4.8
    o = []
    for i, name in enumerate(chain):
        yy = y + 16 + i * 32
        o.append(f'<rect x="{x + 34}" y="{yy}" width="108" height="24" rx="6" fill="{t["panel"]}" stroke="{t["line2"]}"/>'
                 f'<text x="{x + 88}" y="{yy + 16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["soft"]}">{name}</text>')
        o.append(f'<rect x="{x + 34}" y="{yy}" width="108" height="24" rx="6" fill="none" stroke="{t["accent"]}" stroke-width="1.5" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;0;0;1;0;0" keyTimes="0;{i * 0.1:.2f};{i * 0.1 + 0.04:.2f};{i * 0.1 + 0.1:.2f};{0.9 - i * 0.1 - 0.1:.2f};{0.9 - i * 0.1 - 0.04:.2f};{0.9 - i * 0.1:.2f};1" dur="{T}s" repeatCount="indefinite"/></rect>')
    o.append(f'<circle cx="{x + 22}" r="4" fill="{t["accent"]}"><animate attributeName="cy" values="{y + 28};{y + 124};{y + 124};{y + 28};{y + 28}" keyTimes="0;0.4;0.5;0.9;1" dur="{T}s" repeatCount="indefinite"/>'
             f'<animate attributeName="fill" values="{t["accent"]};{t["accent"]};{t["green"]};{t["green"]}" keyTimes="0;0.45;0.5;1" dur="{T}s" repeatCount="indefinite"/></circle>')
    o.append(f'<line x1="{x + 22}" y1="{y + 24}" x2="{x + 22}" y2="{y + 128}" stroke="{t["line2"]}" stroke-dasharray="2 4"/>')
    return "".join(o)


def art_kinoza(t, x, y):
    """Плёнка едет: кадры с треугольником «play»."""
    fw = 46
    o = [f'<clipPath id="fl"><rect x="{x + 1}" y="{y + 1}" width="174" height="148" rx="10"/></clipPath><g clip-path="url(#fl)"><g>',
         f'<animateTransform attributeName="transform" type="translate" values="0 0;{-fw} 0" dur="1.4s" repeatCount="indefinite"/>',
         f'<rect x="{x - 10}" y="{y + 36}" width="{fw * 6}" height="78" fill="{t["soft"]}" opacity="0.9"/>']
    for k in range(6):
        fx = x - 10 + k * fw
        for hy in (y + 41, y + 103):
            o.append(f'<rect x="{fx + 8}" y="{hy}" width="10" height="6" rx="1.5" fill="{t["panel"]}"/><rect x="{fx + 28}" y="{hy}" width="10" height="6" rx="1.5" fill="{t["panel"]}"/>')
        o.append(f'<rect x="{fx + 5}" y="{y + 52}" width="{fw - 10}" height="46" rx="3" fill="{t["panel"]}"/>')
        o.append(f'<path d="M{fx + 19} {y + 66}l11 9-11 9z" fill="{t["accent"] if k % 2 else t["faint"]}"/>')
    o.append("</g></g>")
    return "".join(o)


def art_dotfiles(t, x, y):
    """dot doctor: команда печатается, проверки отмечаются по одной."""
    T = 7
    checks = ["brew", "zsh", "nvim", "ghostty"]
    o = [f'<clipPath id="dd"><rect x="{x + 12}" y="{y + 12}" width="0" height="20"><animate attributeName="width" values="0;0;150;150;0" keyTimes="0;0.05;0.22;0.95;1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>',
         f'<text x="{x + 14}" y="{y + 27}" font-family="{MONO}" font-size="12" clip-path="url(#dd)"><tspan fill="{t["accent"]}">$</tspan> <tspan fill="{t["text"]}">dot doctor</tspan></text>']
    for i, c in enumerate(checks):
        at = 0.3 + i * 0.12
        o.append(f'<text x="{x + 14}" y="{y + 54 + i * 22}" font-family="{MONO}" font-size="12"><tspan fill="{t["green"]}">✓</tspan> <tspan fill="{t["soft"]}">{c}</tspan>'
                 f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{at:.2f};{at + 0.02:.2f};0.95;1" dur="{T}s" repeatCount="indefinite"/></text>')
    return "".join(o)


ART = {"watchdog": art_watchdog, "logsence": art_logsence, "ordergo": art_ordergo, "pulse": art_pulse,
       "kinoza": art_kinoza, "dotfiles": art_dotfiles}


def project(p, theme):
    t = THEMES[theme]
    w, h = 590, 230
    o = [frame(w, h, t, rx=16, fill=t["panel"])]
    o.append(gt(p["name"], 30, 60, 26, t["text"], tracking=-0.6))
    nx = 30 + gw(p["name"], 26, tracking=-0.6) + 12
    if p.get("team"):
        o.append(f'<rect x="{nx:.0f}" y="41" width="50" height="22" rx="11" fill="none" stroke="{t["line2"]}"/>'
                 f'<text x="{nx + 25:.0f}" y="56" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{t["muted"]}">Team</text>')
    o.append(f'<text x="30" y="86" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(p["repo"])}</text>')
    s, _ = para(p["desc"], 30, 122, 14.5, 330, t["soft"], limit=3)
    o.append(s)
    o.append(tags(p["tags"], 30, h - 28, t))
    ax, ay = 384, 28
    o.append(f'<rect x="{ax}" y="{ay}" width="176" height="150" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    o.append(ART[p["slug"]](t, ax, ay))
    o.append(arrow(w - 44, h - 40, 11, t["faint"]))
    return svg(w, h, "\n".join(o), f'{p["name"]}: {p["desc"]}')


# ═══════════════════════════════ сейчас: лента демона gw ═══════════════════════════════

NOW = [   # (что, подробности, цвет точки)
    ("Building gw", "GitHub in the terminal: PRs, Actions, inbox, search", "green"),
    ("Team: kinoza-back", "the Go backend, together with the team", "accent"),
    ("Tuning dotfiles", "berth for containers, Neovim, one-command setup", "kw"),
]
FEED = [   # пример того, что gw daemon шлёт в Telegram
    ("12:04", "pull_request", "#7 Add cache — checks passed", "green"),
    ("12:06", "actions", "ci on main — success in 1m 12s", "green"),
    ("12:09", "review", "@alice requested changes on #6", "kw"),
    ("12:15", "issue", "#12 opened: rate limit on /search", "accent"),
    ("12:21", "actions", "release v0.4.0 — success", "green"),
    ("12:30", "pull_request", "#6 Fix login — merged", "kw"),
    ("12:34", "mention", "@me in #13: can you take a look?", "accent"),
]


def now(theme):
    t = THEMES[theme]
    H = 300
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    o.append(f'<text x="40" y="52" font-family="{SANS}" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t["accent"]}">RIGHT NOW</text>')
    for i, (head, sub, c) in enumerate(NOW):
        y = 104 + i * 64
        col = t[c]
        o.append(f'<circle cx="46" cy="{y - 6}" r="9" fill="{col}" opacity="0.2"><animate attributeName="opacity" values="0.25;0;0.25" dur="2.6s" begin="{i * 0.8}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="r" values="4;10;4" dur="2.6s" begin="{i * 0.8}s" repeatCount="indefinite"/></circle>')
        o.append(f'<circle cx="46" cy="{y - 6}" r="4" fill="{col}"/>')
        o.append(gt(head, 66, y, 20, t["text"], tracking=-0.3))
        o.append(f'<text x="66" y="{y + 24}" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{esc(sub)}</text>')
        if i < len(NOW) - 1:
            o.append(f'<line x1="46" y1="{y + 8}" x2="46" y2="{y + 46}" stroke="{t["line2"]}" stroke-dasharray="2 4"/>')

    # окно ленты: события выезжают снизу одно за другим
    x, y0, w, h = 560, 36, 604, 228
    o.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    o.append(f'<text x="{x + 18}" y="{y0 + 28}" font-family="{MONO}" font-size="12.5" fill="{t["text"]}">gw daemon</text>')
    o.append(f'<text x="{x + w - 18}" y="{y0 + 28}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">'
             f'<tspan fill="{t["green"]}">●</tspan> watching · sends to Telegram</text>')
    o.append(f'<line x1="{x}" y1="{y0 + 42}" x2="{x + w}" y2="{y0 + 42}" stroke="{t["line"]}"/>')
    o.append(f'<clipPath id="feed"><rect x="{x + 1}" y="{y0 + 44}" width="{w - 2}" height="{h - 46}" rx="10"/></clipPath>')
    lh, vis = 30, 5
    n = len(FEED)
    rows = FEED + FEED[:vis]   # хвост повторяет начало — прокрутка замыкается без скачка
    steps, T = n, 2.2 * n
    vals, kts = [], []   # сдвиг на строку: стоим, потом плавно едем
    for k in range(steps):
        a_, b_ = k / steps, (k + 0.85) / steps
        vals += [f"0 {-k * lh}", f"0 {-k * lh}"]
        kts += [a_, b_]
    vals.append(f"0 {-steps * lh}")
    kts.append(1)
    g = [f'<g clip-path="url(#feed)"><g><animateTransform attributeName="transform" type="translate" values="{";".join(vals)}" '
         f'keyTimes="{";".join(f"{k:.4f}" for k in kts)}" dur="{T}s" repeatCount="indefinite"/>']
    for i, (tm, kind, msg, c) in enumerate(rows):
        yy = y0 + 72 + i * lh
        g.append(f'<text x="{x + 18}" y="{yy}" font-family="{MONO}" font-size="12.5" fill="{t["faint"]}" xml:space="preserve">{tm}  '
                 f'<tspan fill="{t[c]}">{kind:<13}</tspan><tspan fill="{t["soft"]}">{esc(msg)}</tspan></text>')
    g.append("</g></g>")
    o.append("".join(g))
    return svg(W, H, "\n".join(o), "Right now: building gw, the Go backend of kinoza-back with a team, tuning dotfiles. Example gw daemon feed.")


# ═══════════════════════════════ путь запроса в logsence ═══════════════════════════════

def flow(theme):
    t = THEMES[theme]
    H = 260
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    o.append(f'<text x="40" y="52" font-family="{SANS}" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t["accent"]}">HOW A LOG TRAVELS IN LOGSENCE</text>')
    nodes = [("client", "any service", None, 60), ("Gin router", "/logs", "gin", 340), ("handler", "validate · batch", None, 620), ("PostgreSQL", "pgx + sqlx", "postgresql", 900)]
    bw, bh, by = 220, 84, 104
    for name, sub, ic, x in nodes:
        o.append(f'<rect x="{x}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="{t["bg"]}" stroke="{t["line2"]}"/>')
        tx = x + 22
        if ic:
            o.append(icon(ic, x + 20, by + 22, 22, t["text"]))
            tx = x + 54
        o.append(gt(name, tx, by + 40, 18, t["text"], tracking=-0.3))
        o.append(f'<text x="{tx}" y="{by + 64}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(sub)}</text>')
    T = 6
    for i in range(3):   # стрелки и пакеты: туда — POST, обратно — ответ запроса
        x1, x2 = nodes[i][3] + bw, nodes[i + 1][3]
        yf, yb = by + 30, by + 56
        o.append(f'<line x1="{x1}" y1="{yf}" x2="{x2}" y2="{yf}" stroke="{t["line2"]}"/><line x1="{x1}" y1="{yb}" x2="{x2}" y2="{yb}" stroke="{t["line2"]}" stroke-dasharray="3 4"/>')
        s1, s2 = i * 0.12, 0.5 + (2 - i) * 0.12
        o.append(f'<circle r="4" cy="{yf}" fill="{t["accent"]}"><animate attributeName="cx" values="{x1};{x1};{x2};{x2}" keyTimes="0;{s1:.2f};{s1 + 0.12:.2f};1" dur="{T}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{s1:.2f};{s1 + 0.06:.2f};{s1 + 0.12:.2f};1" dur="{T}s" repeatCount="indefinite"/></circle>')
        o.append(f'<circle r="4" cy="{yb}" fill="{t["green"]}"><animate attributeName="cx" values="{x2};{x2};{x1};{x1}" keyTimes="0;{s2:.2f};{s2 + 0.12:.2f};1" dur="{T}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{s2:.2f};{s2 + 0.06:.2f};{s2 + 0.12:.2f};1" dur="{T}s" repeatCount="indefinite"/></circle>')
    o.append(f'<text x="40" y="{H - 34}" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}">'
             f'<tspan fill="{t["accent"]}">●</tspan> POST /logs  {{"service":"api","level":"error",…}}      '
             f'<tspan fill="{t["green"]}">●</tspan> GET /logs?service=api  → 200, newest first</text>')
    return svg(W, H, "\n".join(o), "How a log travels in logsence: client to Gin router to handler to PostgreSQL, and back on a query by service")


# ═══════════════════════════════ CI ═══════════════════════════════

CI = ["gofmt · vet", "test -race", "golangci-lint", "govulncheck", "docker build"]


def ci(theme):
    t = THEMES[theme]
    H, T = 230, 10.0
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    o.append(f'<text x="40" y="52" font-family="{SANS}" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t["accent"]}">EVERY PUSH</text>')
    o.append(f'<text x="{W - 40}" y="52" text-anchor="end" font-family="{SANS}" font-size="13" fill="{t["muted"]}">the same CI in every Go repo, from my gonew template</text>')
    steps = ["git push"] + CI + ["merge"]
    n = len(steps)
    x0, x1, y = 90, W - 90, 128
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    o.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{t["line2"]}" stroke-width="2"/>')
    o.append(f'<rect x="{x0}" y="{y - 1}" height="2" width="{x1 - x0}" fill="{t["accent"]}"><animate attributeName="width" values="0;{x1 - x0};{x1 - x0};0" keyTimes="0;0.8;0.95;1" dur="{T}s" repeatCount="indefinite"/></rect>')
    for i, (x, name) in enumerate(zip(xs, steps)):
        at = 0.8 * i / (n - 1)   # когда до шага доходит линия
        o.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{t["bg"]}" stroke="{t["line2"]}" stroke-width="2"/>')
        o.append(f'<g><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{at:.3f};{min(at + 0.02, 0.9):.3f};0.95;1" dur="{T}s" repeatCount="indefinite"/>'
                 f'<circle cx="{x}" cy="{y}" r="13" fill="{t["green"] if 0 < i < n - 1 else t["accent"]}"/>'
                 f'<path d="M{x - 5} {y}l3.5 3.6 6.5-7" fill="none" stroke="{t["bg"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        o.append(f'<text x="{x}" y="{y + 44}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["text"] if i in (0, n - 1) else t["soft"]}">{esc(name)}</text>')
    o.append(f'<text x="40" y="{H - 28}" font-family="{SANS}" font-size="13" fill="{t["muted"]}">Before a commit leaves the laptop, gitleaks checks it for secrets.</text>')
    return svg(W, H, "\n".join(o), "Every push: gofmt and vet, tests with -race, golangci-lint, govulncheck and a Docker build, then merge")


# ═══════════════════════════════ стек ═══════════════════════════════

STACK = [
    ("Backend", [("go", "Go"), ("gin", "Gin"), ("openjdk", "Java"), ("spring", "Spring")]),
    ("Data", [("postgresql", "PostgreSQL"), ("redis", "Redis")]),
    ("Ship", [("docker", "Docker"), ("githubactions", "Actions"), ("linux", "Linux")]),
    ("Tools", [("git", "Git"), ("gnubash", "Bash"), ("neovim", "Neovim")]),
]


def stack(theme):
    t = THEMES[theme]
    H = 200
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    total = sum(len(items) for _, items in STACK)
    gap, x = 34, 40
    step = (W - 80 - gap * (len(STACK) - 1)) / total
    k = 0
    for gi, (group, items) in enumerate(STACK):
        gw_ = step * len(items)
        o.append(f'<text x="{x:.0f}" y="52" font-family="{SANS}" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t["muted"]}">{group.upper()}</text>')
        o.append(f'<line x1="{x:.0f}" y1="64" x2="{x + gw_ - 10:.0f}" y2="64" stroke="{t["line"]}"/>')
        for j, (ic, label) in enumerate(items):
            cx = x + step * (j + 0.5)
            # подсветка по очереди пробегает по всем иконкам
            o.append(f'<g>{icon(ic, cx - 16, 92, 32, t["text"])}</g>')
            o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;0.04;0.1;1" dur="{total * 0.7:.1f}s" begin="{k * 0.7:.1f}s" repeatCount="indefinite"/>'
                     f'{icon(ic, cx - 16, 92, 32, t["accent"])}</g>')
            o.append(f'<text x="{cx:.0f}" y="156" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{esc(label)}</text>')
            k += 1
        x += gw_ + gap
    return svg(W, H, "\n".join(o), "Stack — " + "; ".join(f'{g}: ' + ", ".join(l for _, l in items) for g, items in STACK))


# ═══════════════════════════════ финал ═══════════════════════════════

def runner(y, scale=4, dur=11):
    """Пиксельный гофер (спрайт Эгона Элбре, CC0) бежит через весь кадр; кадры бега 16–23 по 12×14."""
    import base64
    data = base64.b64encode((ROOT / "assets" / "gophers" / "sprite-sheet.png").read_bytes()).decode()
    fw, fh = 12 * scale, 14 * scale
    xs = ";".join(str(-12 * f) for f in range(16, 24))
    return (f'<g><animateTransform attributeName="transform" type="translate" values="-60 0;{W + 10} 0" dur="{dur}s" repeatCount="indefinite"/>'
            f'<svg x="0" y="{y - fh}" width="{fw}" height="{fh}" viewBox="0 0 12 14">'
            f'<image x="-192" y="0" width="324" height="14" style="image-rendering:pixelated" href="data:image/png;base64,{data}">'
            f'<animate attributeName="x" values="{xs}" calcMode="discrete" dur="0.8s" repeatCount="indefinite"/></image></svg></g>')


def footer(theme):
    t = THEMES[theme]
    H = 170
    o = [frame(W, H, t, rx=16, fill=t["panel"], seed=29)]
    msg = "exit  # thanks for stopping by"
    full = tw("$ " + msg, 15, mono=True) + 8
    o.append(f'<clipPath id="ft"><rect x="38" y="44" width="{full:.0f}" height="30"><animate attributeName="width" values="0;0;{full:.0f};{full:.0f};0" keyTimes="0;0.1;0.45;0.92;1" dur="8s" repeatCount="indefinite"/></rect></clipPath>')
    o.append(f'<text x="40" y="65" font-family="{MONO}" font-size="15" clip-path="url(#ft)" xml:space="preserve"><tspan fill="{t["accent"]}">$</tspan> '
             f'<tspan fill="{t["text"]}">exit</tspan>  <tspan fill="{t["muted"]}"># thanks for stopping by</tspan></text>')
    o.append(f'<rect x="{40 + full:.0f}" y="51" width="8" height="17" fill="{t["accent"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    o.append(f'<text x="{W - 40}" y="65" text-anchor="end" font-family="{SANS}" font-size="13" fill="{t["muted"]}">van1dal · Saint Petersburg · English or Russian</text>')
    o.append(f'<line x1="24" y1="{H - 30}" x2="{W - 24}" y2="{H - 30}" stroke="{t["line2"]}" stroke-dasharray="3 6"/>')
    o.append(f'<clipPath id="fr"><rect width="{W}" height="{H}" rx="16"/></clipPath><g clip-path="url(#fr)">{runner(H - 30)}</g>')
    o.append(f'<text x="{W - 40}" y="{H - 10}" text-anchor="end" font-family="{SANS}" font-size="11" fill="{t["faint"]}">gophers by Egon Elbre, CC0</text>')
    return svg(W, H, "\n".join(o), "Thanks for stopping by — a pixel gopher runs across")


# ═══════════════════════════════ заголовки разделов ═══════════════════════════════

SECTIONS = {   # ключ → (номер, заголовок, подпись)
    "now": ("01", "Right now", "what I'm on this week"),
    "about": ("02", "About", "the short version"),
    "projects": ("03", "Projects", "things I built and keep building"),
    "journey": ("04", "Journey", "2026, month by month"),
    "ship": ("05", "How I ship", "every push, every repo"),
    "habits": ("06", "Habits", "rules I don't break"),
    "stack": ("07", "Stack", "what I reach for"),
    "activity": ("08", "Activity", "redrawn every day"),
    "contact": ("09", "Contact", "say hi"),
}


MASCOTS = {   # раздел → (гофер, высота)
    "now": ("music", 84), "about": ("gamer", 84), "projects": ("soldering", 80), "journey": ("hiking", 78),
    "ship": ("rocket", 92), "habits": ("knight", 84), "stack": ("network", 80), "activity": ("lifting", 74),
    "contact": ("heart-balloon", 92),
}


def header(key, theme):
    t = THEMES[theme]
    num, title, sub = SECTIONS[key]
    H = 110
    o = []   # фон прозрачный — заголовок ложится прямо на страницу GitHub
    o.append(f'<text x="4" y="52" font-family="{MONO}" font-size="13" fill="{t["accent"]}">{num}</text>')
    o.append(gt(title, 40, 56, 30, t["text"], tracking=-0.8))
    o.append(f'<text x="{40 + gw(title, 30, tracking=-0.8) + 16:.0f}" y="55" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{esc(sub)}</text>')
    if key in MASCOTS:   # гофер сидит на линии справа и слегка покачивается
        name, gh = MASCOTS[key]
        img, gwid = gopher(name, 0, 0, gh)
        o.append(f'<g transform="translate({W - 40 - gwid:.0f} {H - 12 - gh:.0f})"><g><animateTransform attributeName="transform" type="rotate" '
                 f'values="-3 {gwid / 2:.0f} {gh:.0f};3 {gwid / 2:.0f} {gh:.0f};-3 {gwid / 2:.0f} {gh:.0f}" dur="{4 + len(key) % 3}s" repeatCount="indefinite" '
                 f'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>{img}</g></g>')
    o.append(f'<line x1="4" y1="{H - 14}" x2="{W - 4}" y2="{H - 14}" stroke="{t["line"]}"/>')
    # по линии скользит короткий акцентный отрезок
    o.append(f'<rect x="4" y="{H - 15}" width="90" height="2" rx="1" fill="{t["accent"]}"><animate attributeName="x" values="4;{W - 94};4" dur="12s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></rect>')
    return svg(W, H, "\n".join(o), f"{num} {title} — {sub}")


# ═══════════════════════════════ путь по месяцам (даты создания репозиториев) ═══════════════════════════════

JOURNEY = [   # (дата, заголовок, подпись)
    ("2026-07-07", "Hello, GitHub", "this profile"),
    ("2026-08-01", "Java first", "calculator, Telegram bot, Spring Boot"),
    ("2026-08-20", "First Go", "NEXA bot, then Pulse"),
    ("2026-08-30", "watchdog", "uptime monitor, Docker"),
    ("2026-09-12", "OrderGo", "production-style layout"),
    ("2026-09-27", "logsence", "logs into PostgreSQL, full CI"),
    ("2026-10-03", "dotfiles", "the whole Mac as code"),
    ("2026-10-11", "gw", "GitHub in the terminal"),
]


def journey(theme):
    import datetime as dt
    t = THEMES[theme]
    H, T = 360, 12.0
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    d0, d1 = dt.date(2026, 7, 1), dt.date(2026, 11, 1)
    x0, x1, ly = 60, W - 60, 176
    levels = [(-1, 34), (1, 34), (-1, 86), (1, 86)]   # над/под линией, близко/далеко — подписи не налезают
    X = lambda d: x0 + (d - d0).days / (d1 - d0).days * (x1 - x0)
    o.append(f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{t["line2"]}" stroke-width="2"/>')
    for m, name in ((7, "Jul"), (8, "Aug"), (9, "Sep"), (10, "Oct"), (11, "")):
        mx = X(dt.date(2026, m, 1))
        o.append(f'<line x1="{mx:.0f}" y1="{ly - 6}" x2="{mx:.0f}" y2="{ly + 6}" stroke="{t["line2"]}" stroke-width="2"/>')
        if name:
            o.append(f'<text x="{mx + 8:.0f}" y="{H - 20}" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{name} 2026</text>')
    last = X(dt.date.fromisoformat(JOURNEY[-1][0]))
    o.append(f'<rect x="{x0}" y="{ly - 1}" height="2" width="{last - x0:.0f}" fill="{t["accent"]}">'
             f'<animate attributeName="width" values="0;{last - x0:.0f};{last - x0:.0f};0" keyTimes="0;0.7;0.95;1" dur="{T}s" repeatCount="indefinite"/></rect>')
    for i, (ds, head, sub) in enumerate(JOURNEY):
        x = X(dt.date.fromisoformat(ds))
        at = 0.7 * (x - x0) / (last - x0)
        side, dist = levels[i % 4]
        ty = ly - dist - 22 if side < 0 else ly + dist + 6
        o.append(f'<line x1="{x:.0f}" y1="{ly}" x2="{x:.0f}" y2="{ly + side * (dist - 12)}" stroke="{t["line2"]}" stroke-dasharray="2 3"/>')
        o.append(f'<circle cx="{x:.0f}" cy="{ly}" r="6" fill="{t["bg"]}" stroke="{t["line2"]}" stroke-width="2"/>')
        o.append(f'<circle cx="{x:.0f}" cy="{ly}" r="6" fill="{t["accent"]}" opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{at:.3f};{at + 0.01:.3f};0.95;1" dur="{T}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="r" values="6;6;9;6;6" keyTimes="0;{at:.3f};{at + 0.02:.3f};{at + 0.05:.3f};1" dur="{T}s" repeatCount="indefinite"/></circle>')
        anchor = "start" if x < 160 else "end" if x > W - 160 else "middle"
        o.append(f'<text x="{x:.0f}" y="{ty}" text-anchor="{anchor}" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["text"]}">{esc(head)}</text>')
        o.append(f'<text x="{x:.0f}" y="{ty + 18}" text-anchor="{anchor}" font-family="{SANS}" font-size="12" fill="{t["muted"]}">{esc(sub)}</text>')
    return svg(W, H, "\n".join(o), "Journey in 2026: " + "; ".join(f"{d} {h} — {s_}" for d, h, s_ in JOURNEY))


# ═══════════════════════════════ привычки ═══════════════════════════════

HABITS = [
    ("check", "Green or it doesn't merge", "fmt, vet, race tests, lint and govulncheck on every push"),
    ("lock", "No secrets in git", "gitleaks checks each commit before it leaves the laptop"),
    ("term", "Setup as code", "one command rebuilds my Mac, dot doctor checks it"),
    ("boxes", "Small, plain services", "cmd/ and internal/, plain net/http when it's enough"),
]


def habit_icon(kind, t, x, y):
    a = t["accent"]
    if kind == "check":   # галочка рисуется заново
        return (f'<circle cx="{x + 18}" cy="{y + 18}" r="16" fill="none" stroke="{t["line2"]}" stroke-width="2"/>'
                f'<path d="M{x + 10} {y + 18}l6 6 11-12" fill="none" stroke="{a}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="26">'
                '<animate attributeName="stroke-dashoffset" values="26;0;0;26" keyTimes="0;0.25;0.85;1" dur="3s" repeatCount="indefinite"/></path>')
    if kind == "lock":    # дужка замка защёлкивается
        return (f'<rect x="{x + 6}" y="{y + 16}" width="24" height="19" rx="4" fill="none" stroke="{a}" stroke-width="2"/>'
                f'<path d="M{x + 11} {y + 16}v-5a7 7 0 0 1 14 0v5" fill="none" stroke="{t["soft"]}" stroke-width="2">'
                '<animateTransform attributeName="transform" type="translate" values="0 -4;0 -4;0 0;0 0;0 -4" keyTimes="0;0.3;0.4;0.9;1" dur="3s" repeatCount="indefinite"/></path>'
                f'<circle cx="{x + 18}" cy="{y + 25}" r="2" fill="{a}"/>')
    if kind == "term":    # приглашение и мигающий курсор
        return (f'<rect x="{x + 2}" y="{y + 4}" width="32" height="28" rx="5" fill="none" stroke="{t["line2"]}" stroke-width="2"/>'
                f'<path d="M{x + 9} {y + 13}l5 4-5 4" fill="none" stroke="{a}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<rect x="{x + 17}" y="{y + 20}" width="9" height="2" fill="{t["soft"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect>')
    return (f'<rect x="{x + 4}" y="{y + 20}" width="12" height="12" rx="2" fill="none" stroke="{t["soft"]}" stroke-width="2"/>'
            f'<rect x="{x + 20}" y="{y + 20}" width="12" height="12" rx="2" fill="none" stroke="{t["soft"]}" stroke-width="2"/>'
            f'<rect x="{x + 12}" y="{y + 4}" width="12" height="12" rx="2" fill="none" stroke="{a}" stroke-width="2">'
            '<animateTransform attributeName="transform" type="translate" values="0 -3;0 0;0 0;0 -3" keyTimes="0;0.2;0.8;1" dur="2.6s" repeatCount="indefinite"/></rect>')


def habits(theme):
    t = THEMES[theme]
    H, gap = 210, 16
    cw = (W - 3 * gap) / 4
    o = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}" opacity="0"/>']
    for i, (kind, head, sub) in enumerate(HABITS):
        x = i * (cw + gap)
        o.append(f'<g transform="translate({x:.1f} 0)">{frame(int(cw), H, t, rx=16, seed=11 + i * 5, n=2, uid=f"h{i}")}</g>')
        o.append(habit_icon(kind, t, x + 26, 28))
        o.append(gt(head, x + 26, 112, 18, t["text"], tracking=-0.3))
        s_, _ = para(sub, x + 26, 140, 13.5, cw - 52, t["muted"], limit=3)
        o.append(s_)
    return svg(W, H, "\n".join(o), "Habits: " + "; ".join(f"{h} — {s_}" for _, h, s_ in HABITS))


def main():
    for theme in THEMES:
        write("hero", theme, hero(theme))
        write("featured", theme, featured(theme))
        write("stack", theme, stack(theme))
        write("now", theme, now(theme))
        write("flow", theme, flow(theme))
        write("ci", theme, ci(theme))
        write("footer", theme, footer(theme))
        write("journey", theme, journey(theme))
        write("habits", theme, habits(theme))
        for k in SECTIONS:
            write("h-" + k, theme, header(k, theme))
        for p in PROJECTS:
            write("p-" + p["slug"], theme, project(p, theme))
    print("assets: ok")


if __name__ == "__main__":
    main()
