#!/usr/bin/env python3
"""Рисует статичные картинки профиля в assets/ (тёмная и светлая версии):  python3 scripts/build.py

Тексты лежат здесь обычными списками (INTRO, FEATURED, PROJECTS, STACK) — поправил строку,
перезапустил скрипт, закоммитил. Живую статистику рисует stats.py в workflow.
"""
from kit import MONO, SANS, THEMES, arrow, esc, frame, gt, gw, icon, svg, tw, write

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


def hero(theme):
    t = THEMES[theme]
    H = 360
    o = [frame(W, H, t, rx=20), dots(t, 10, 10, W - 20, H - 20)]
    # статус: зелёная точка пульсирует
    st = INTRO["status"]
    pw = tw(st, 13) * 0.9 + 40
    o.append(f'<rect x="56" y="52" width="{pw:.0f}" height="30" rx="15" fill="{t["panel"]}" stroke="{t["line"]}"/>')
    o.append(f'<circle cx="74" cy="67" r="7" fill="{t["green"]}" opacity="0.25"><animate attributeName="r" values="4;8;4" dur="2.4s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.35;0;0.35" dur="2.4s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="74" cy="67" r="3.5" fill="{t["green"]}"/>')
    o.append(f'<text x="88" y="71.5" font-family="{SANS}" font-size="13" fill="{t["soft"]}">{esc(st)}</text>')
    o.append(gt(INTRO["name"], 52, 178, 92, t["text"], tracking=-3.5))
    o.append(gt(INTRO["role"], 56, 226, 26, t["soft"], font="body", tracking=-0.4))
    s, _ = para(INTRO["about"], 56, 276, 16, 560, t["muted"])
    o.append(s)

    # карточка с кодом
    cx, cy, cw, ch = 700, 60, 444, 240
    o.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="{t["panel"]}" stroke="{t["line"]}"/>')
    o.append(f'<line x1="{cx}" y1="{cy + 38}" x2="{cx + cw}" y2="{cy + 38}" stroke="{t["line"]}"/>')
    for i in range(3):
        o.append(f'<circle cx="{cx + 20 + i * 16}" cy="{cy + 19}" r="4.5" fill="{t["line2"]}"/>')
    o.append(f'<text x="{cx + cw - 18}" y="{cy + 23.5}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">cmd/api/main.go</text>')
    col = {"kw": t["kw"], "str": t["str"], "fn": t["accent"], "t": t["soft"]}
    # строки «печатаются» по кругу; без анимации (превью) код просто виден целиком
    T, clock, y = 14.0, 0.6, cy + 68
    for n, (ind, parts) in enumerate(CODE):
        o.append(f'<text x="{cx + 20}" y="{y}" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{n + 1}</text>')
        text = "".join(s_ for s_, _ in parts)
        x0 = cx + 48 + ind * 29
        full = tw(text, 14, mono=True) + 6
        st, dur = clock, max(0.05, 0.05 * len(text))
        clock += dur + 0.15
        o.append(f'<clipPath id="cl{n}"><rect x="{x0 - 2}" y="{y - 16}" width="{full:.0f}" height="22">'
                 f'<animate attributeName="width" values="0;0;{full:.0f};{full:.0f};0" keyTimes="0;{st / T:.4f};{(st + dur) / T:.4f};0.94;1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        spans = "".join(f'<tspan fill="{col[r]}">{esc(s_)}</tspan>' for s_, r in parts)
        o.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="14" xml:space="preserve" clip-path="url(#cl{n})">{spans}</text>')
        y += 22
    last = "".join(s_ for s_, _ in CODE[-1][1])
    o.append(f'<rect x="{cx + 48 + tw(last, 14, mono=True) + 2:.0f}" y="{y - 22 - 13}" width="2" height="17" fill="{t["accent"]}">'
             '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    # подпись под ролью тянется акцентной линией
    o.append(f'<rect x="56" y="240" width="64" height="2" rx="1" fill="{t["accent"]}"><animate attributeName="width" values="64;180;64" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/></rect>')
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
    return svg(W, H, "\n".join(o), f'Featured: gw — {p["desc"]}')


def project(p, theme):
    t = THEMES[theme]
    w, h = 590, 200
    o = [frame(w, h, t, rx=16, fill=t["panel"])]
    o.append(gt(p["name"], 30, 62, 26, t["text"], tracking=-0.6))
    nx = 30 + gw(p["name"], 26, tracking=-0.6) + 12
    if p.get("team"):
        o.append(f'<rect x="{nx:.0f}" y="43" width="50" height="22" rx="11" fill="none" stroke="{t["line2"]}"/>'
                 f'<text x="{nx + 25:.0f}" y="58" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{t["muted"]}">Team</text>')
    o.append(arrow(w - 46, 42, 11, t["faint"]))
    o.append(f'<text x="30" y="88" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{esc(p["repo"])}</text>')
    s, _ = para(p["desc"], 30, 122, 15, w - 70, t["soft"], limit=2)
    o.append(s)
    o.append(tags(p["tags"], 30, h - 26, t))
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

def footer(theme):
    t = THEMES[theme]
    H = 120
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    msg = "exit  # thanks for stopping by"
    full = tw("$ " + msg, 15, mono=True) + 8
    o.append(f'<clipPath id="ft"><rect x="38" y="44" width="{full:.0f}" height="30"><animate attributeName="width" values="0;0;{full:.0f};{full:.0f};0" keyTimes="0;0.1;0.45;0.92;1" dur="8s" repeatCount="indefinite"/></rect></clipPath>')
    o.append(f'<text x="40" y="65" font-family="{MONO}" font-size="15" clip-path="url(#ft)" xml:space="preserve"><tspan fill="{t["accent"]}">$</tspan> '
             f'<tspan fill="{t["text"]}">exit</tspan>  <tspan fill="{t["muted"]}"># thanks for stopping by</tspan></text>')
    o.append(f'<rect x="{40 + full:.0f}" y="51" width="8" height="17" fill="{t["accent"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    o.append(f'<text x="{W - 40}" y="65" text-anchor="end" font-family="{SANS}" font-size="13" fill="{t["muted"]}">van1dal · Saint Petersburg · English or Russian</text>')
    return svg(W, H, "\n".join(o), "Thanks for stopping by")


def main():
    for theme in THEMES:
        write("hero", theme, hero(theme))
        write("featured", theme, featured(theme))
        write("stack", theme, stack(theme))
        write("now", theme, now(theme))
        write("flow", theme, flow(theme))
        write("ci", theme, ci(theme))
        write("footer", theme, footer(theme))
        for p in PROJECTS:
            write("p-" + p["slug"], theme, project(p, theme))
    print("assets: ok")


if __name__ == "__main__":
    main()
