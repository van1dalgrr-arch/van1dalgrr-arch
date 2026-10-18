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
            f'<g fill="{t["dot"]}" mask="url(#{gid}m)">{pts}</g>')


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
    o = [frame(W, H, t, rx=20), dots(t, 600, 0, 600, H)]
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
    s, _ = para(INTRO["about"], 56, 268, 16, 560, t["muted"])
    o.append(s)

    # карточка с кодом
    cx, cy, cw, ch = 700, 60, 444, 240
    o.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="{t["panel"]}" stroke="{t["line"]}"/>')
    o.append(f'<line x1="{cx}" y1="{cy + 38}" x2="{cx + cw}" y2="{cy + 38}" stroke="{t["line"]}"/>')
    for i in range(3):
        o.append(f'<circle cx="{cx + 20 + i * 16}" cy="{cy + 19}" r="4.5" fill="{t["line2"]}"/>')
    o.append(f'<text x="{cx + cw - 18}" y="{cy + 23.5}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">cmd/api/main.go</text>')
    col = {"kw": t["kw"], "str": t["str"], "fn": t["accent"], "t": t["soft"]}
    y = cy + 68
    for n, (ind, parts) in enumerate(CODE):
        o.append(f'<text x="{cx + 20}" y="{y}" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{n + 1}</text>')
        spans = "".join(f'<tspan fill="{col[r]}">{esc(s_)}</tspan>' for s_, r in parts)
        o.append(f'<text x="{cx + 48 + ind * 29}" y="{y}" font-family="{MONO}" font-size="14" xml:space="preserve">{spans}</text>')
        y += 22
    last = "".join(s_ for s_, _ in CODE[-1][1])
    o.append(f'<rect x="{cx + 48 + tw(last, 14, mono=True) + 2:.0f}" y="{y - 22 - 13}" width="2" height="17" fill="{t["accent"]}">'
             '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
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


# ═══════════════════════════════ стек ═══════════════════════════════

STACK = [("go", "Go"), ("gin", "Gin"), ("postgresql", "PostgreSQL"), ("redis", "Redis"), ("docker", "Docker"), ("githubactions", "Actions"),
         ("linux", "Linux"), ("git", "Git"), ("gnubash", "Bash"), ("neovim", "Neovim"), ("openjdk", "Java"), ("spring", "Spring")]


def stack(theme):
    t = THEMES[theme]
    H = 150
    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    step = (W - 80) / len(STACK)
    for i, (ic, label) in enumerate(STACK):
        cx = 40 + step * (i + 0.5)
        o.append(icon(ic, cx - 15, 40, 30, t["text"]))
        o.append(f'<text x="{cx:.0f}" y="104" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{esc(label)}</text>')
    return svg(W, H, "\n".join(o), "Stack: " + ", ".join(l for _, l in STACK))


def main():
    for theme in THEMES:
        write("hero", theme, hero(theme))
        write("featured", theme, featured(theme))
        write("stack", theme, stack(theme))
        for p in PROJECTS:
            write("p-" + p["slug"], theme, project(p, theme))
    print("assets: ok")


if __name__ == "__main__":
    main()
