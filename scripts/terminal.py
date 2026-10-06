#!/usr/bin/env python3
"""Анимированная карточка в стиле neofetch: python3 scripts/terminal.py <out.svg>
Живые цифры из GitHub API (GITHUB_TOKEN, USERNAME). Без зависимостей: только стандартная библиотека."""
import datetime as dt, json, os, sys, urllib.request
from xml.sax.saxutils import escape

USER = os.environ.get("USERNAME", "van1dalgrr-arch")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
NAME = os.environ.get("DISPLAY_NAME", "van1dal")

QUERY = """query($login: String!) { user(login: $login) {
  createdAt followers { totalCount }
  repos: repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER, isFork: false) {
    totalCount nodes { name primaryLanguage { name } } }
  latest: repositories(first: 3, privacy: PUBLIC, ownerAffiliations: OWNER, orderBy: {field: PUSHED_AT, direction: DESC}) {
    nodes { name pushedAt } }
  contributionsCollection { totalCommitContributions contributionCalendar { totalContributions
    weeks { contributionDays { contributionCount date } } } } } }"""

def fetch():
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))["data"]["user"]

def ago(iso):
    s = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds()
    for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
        if s >= n: return f"{int(s // n)}{unit} ago"
    return "just now"

def stats(u):
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    streak = 0
    for i, d in enumerate(reversed(days)):        # сегодня без коммитов ещё не обрывает серию
        if d["contributionCount"]: streak += 1
        elif i: break
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    # основной язык каждого репозитория — честнее байтов (один TS-плагин не перевешивает все Go-сервисы)
    langs = {}
    for r in u["repos"]["nodes"]:
        if r["primaryLanguage"] and r["name"] != USER:
            langs[r["primaryLanguage"]["name"]] = langs.get(r["primaryLanguage"]["name"], 0) + 1
    top = sorted(langs.items(), key=lambda x: -x[1])[:3]
    latest = next(r for r in u["latest"]["nodes"] if r["name"] != USER)   # не сам профиль
    return {
        "repos": u["repos"]["totalCount"],
        "contrib": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "commits": u["contributionsCollection"]["totalCommitContributions"],
        "streak": streak, "longest": longest,
        "langs": " · ".join(f"{n} — {c} repo{'s' if c > 1 else ''}" for n, c in top),
        "latest": f'{latest["name"]} ({ago(latest["pushedAt"])})',
        "since": u["createdAt"][:4],
    }

# логотип, как у дистрибутива в neofetch: GO шрифтом ANSI Shadow, строки темнеют сверху вниз
ART = [
    "  ██████╗   ██████╗ ",
    " ██╔════╝  ██╔═══██╗",
    " ██║  ███╗ ██║   ██║",
    " ██║   ██║ ██║   ██║",
    " ╚██████╔╝ ╚██████╔╝",
    "  ╚═════╝   ╚═════╝ ",
]
ART_SHADES = ["#ffffff", "#ffe3ec", "#ffcadb", "#ffb3c7", "#e598b0", "#c47e96"]   # белый → розовый

def svg(s):
    rows = [
        ("title", f"{NAME}@github"),
        ("rule", "─" * 26),
        ("kv", ("Role", "Go backend developer")),
        ("kv", ("Location", "Saint Petersburg")),
        ("kv", ("Stack", "Go · Gin · PostgreSQL · Redis · Docker")),
        ("kv", ("CI", "GitHub Actions · golangci-lint · govulncheck")),
        ("kv", ("Setup", "macOS · Ghostty · Zed · AeroSpace")),
        ("kv", ("Repos", f'{s["repos"]} public')),
        ("kv", ("Last push", s["latest"])),
        ("kv", ("This year", f'{s["contrib"]} contributions · {s["commits"]} commits')),
        ("kv", ("Streak", f'{s["streak"]} days now · best {s["longest"]}')),
        ("kv", ("Languages", s["langs"])),
        ("palette", ""),
    ]
    W, H, lh, x0, xr, y0 = 900, 470, 25, 34, 330, 104
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="neofetch-style card">',
           """<style>
  text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 15px; fill: #c9d1d9; }
  .k { fill: #ffb3c7; font-weight: 700; } .dim { fill: #6e7681; } .t { fill: #ffffff; font-weight: 700; } .art { font-size: 22px; font-weight: 700; }
  .ln { opacity: 0; animation: in .35s ease-out forwards; }
  .type { animation: type 1.1s steps(9, end) .3s both; }
  .cur { animation: blink 1s steps(1) infinite; }
  @keyframes in { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: none; } }
  @keyframes type { from { width: 0; } to { width: 110px; } }
  @keyframes blink { 50% { opacity: 0; } }
</style>""",
           f'<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>',
           f'<rect width="{W}" height="38" rx="12" fill="#161b22"/><rect y="26" width="{W}" height="12" fill="#161b22"/>',
           f'<line x1="0" y1="38" x2="{W}" y2="38" stroke="#30363d"/>']
    for i, c in enumerate(("#5c6370", "#8b949e", "#c9d1d9")):
        out.append(f'<circle cx="{24 + i * 20}" cy="19" r="6" fill="{c}"/>')
    out.append(f'<text x="{W / 2}" y="24" text-anchor="middle" class="dim">zsh — {escape(USER)}</text>')
    # команда печатается: обрезаем текст растущим прямоугольником
    out.append('<defs><clipPath id="c"><rect class="type" x="48" y="56" height="26" width="0"/></clipPath></defs>')
    out.append(f'<text x="{x0}" y="74" class="dim">$</text><text x="52" y="74" class="t" clip-path="url(#c)">neofetch</text>')
    t0 = 1.5
    for i, line in enumerate(ART):
        out.append(f'<text x="{x0}" y="{y0 + 60 + i * 26}" class="art ln" fill="{ART_SHADES[i]}" style="fill:{ART_SHADES[i]};animation-delay:{t0 + i * 0.08:.2f}s" xml:space="preserve">{escape(line)}</text>')
    for i, (kind, val) in enumerate(rows):
        y, d = y0 + i * lh, t0 + 0.25 + i * 0.12
        if kind == "title":
            out.append(f'<text x="{xr}" y="{y}" class="t ln" style="animation-delay:{d:.2f}s">{escape(val)}</text>')
        elif kind == "rule":
            out.append(f'<text x="{xr}" y="{y}" class="dim ln" style="animation-delay:{d:.2f}s">{val}</text>')
        elif kind == "kv":
            k, v = val
            out.append(f'<text x="{xr}" y="{y}" class="ln" style="animation-delay:{d:.2f}s"><tspan class="k">{escape(k)}</tspan><tspan class="dim">:</tspan> {escape(v)}</text>')
        else:   # палитра: серые и розовый акцент профиля, как блоки цветов у neofetch
            for j, g in enumerate(("#0d1117", "#21262d", "#3a3f47", "#5c6370", "#8b949e", "#c47e96", "#ffb3c7", "#ffffff")):
                out.append(f'<rect x="{xr + j * 30}" y="{y - 4}" width="26" height="16" rx="3" fill="{g}" stroke="#30363d" class="ln" style="animation-delay:{d + j * 0.04:.2f}s"/>')
    yc = H - 26
    out.append(f'<text x="{x0}" y="{yc}" class="dim ln" style="animation-delay:{t0 + 2.2:.2f}s">$</text>')
    out.append(f'<rect x="52" y="{yc - 14}" width="9" height="18" fill="#ffb3c7" class="cur"/>')
    out.append("</svg>")
    return "\n".join(out)

if __name__ == "__main__":
    data = stats(fetch())
    open(sys.argv[1] if len(sys.argv) > 1 else "terminal.svg", "w").write(svg(data))
