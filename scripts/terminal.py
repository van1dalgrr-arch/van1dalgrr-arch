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
        if r["primaryLanguage"] and r["name"] not in (USER, "Portfolio", "UserForge"):   # вёрстка и пустой Dockerfile — не языки
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
ART_SHADES = ["#a78bfa", "#c084fc", "#e879f9", "#ec4899", "#f472b6", "#fb923c"]   # фиолетовый → розовый → оранжевый, как баннер

def svg(s):
    rows = [
        ("title", f"{NAME}@github"),
        ("rule", "─" * 26),
        ("kv", ("Role", "Go backend developer")),
        ("kv", ("Location", "Saint Petersburg")),
        ("kv", ("Stack", "Go · Gin · PostgreSQL · Redis · Docker")),
        ("kv", ("CI", "GitHub Actions · golangci-lint · govulncheck")),
        ("kv", ("Setup", "macOS · Ghostty · Neovim · AeroSpace")),
        ("kv", ("Building", "gw — GitHub in the terminal")),
        ("kv", ("Repos", f'{s["repos"]} public')),
        ("kv", ("Last push", s["latest"])),
        ("kv", ("This year", f'{s["contrib"]} contributions · {s["commits"]} commits')),
        ("kv", ("Streak", f'{s["streak"]} day{"s" if s["streak"] != 1 else ""} now · best {s["longest"]}')),
        ("kv", ("Languages", s["langs"])),
        ("palette", ""),
    ]
    W, lh, x0, xr, y0 = 1200, 28, 50, 450, 108
    H = max(470, y0 + len(rows) * lh + 46)   # высота — по числу строк: новая строка не налезет на курсор
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="neofetch-style card">',
           """<style>
  text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 17px; fill: #c9bfe6; }
  .k { fill: #f472b6; font-weight: 700; } .dim { fill: #9a8fbd; } .t { fill: #ffffff; font-weight: 700; } .art { font-size: 30px; font-weight: 700; }
  /* по кругу каждые 16 с: команда печатается, строки выезжают, держатся и гаснут — видно, когда ни долистай */
  .ln { opacity: 0; animation: in 16s ease-out infinite both; }
  .type { animation: type 16s .3s infinite both; }
  .cur { animation: blink 1s steps(1) infinite; }
  @keyframes in { 0% { opacity: 0; transform: translateX(-6px); } 3% { opacity: 1; transform: none; }
                  84% { opacity: 1; transform: none; } 90%, 100% { opacity: 0; transform: none; } }
  @keyframes type { 0% { width: 0; animation-timing-function: steps(9, end); } 7% { width: 120px; }
                    84% { width: 120px; } 90%, 100% { width: 0; } }
  @keyframes blink { 50% { opacity: 0; } }
</style>""",
           f'<rect width="{W}" height="{H}" rx="20" fill="#0c0718" stroke="#2c1f4a" stroke-width="1.5"/>',
           f'<rect width="{W}" height="38" rx="20" fill="#1c1233"/><rect y="20" width="{W}" height="18" fill="#1c1233"/>',
           f'<line x1="0" y1="38" x2="{W}" y2="38" stroke="#2c1f4a"/>']
    for i, c in enumerate(("#ec4899", "#f97316", "#a78bfa")):
        out.append(f'<circle cx="{24 + i * 20}" cy="19" r="6" fill="{c}"/>')
    out.append(f'<text x="{W / 2}" y="24" text-anchor="middle" class="dim">zsh — {escape(USER)}</text>')
    # команда печатается: обрезаем текст растущим прямоугольником
    out.append('<defs><clipPath id="c"><rect class="type" x="64" y="56" height="26" width="0"/></clipPath></defs>')
    out.append(f'<text x="{x0}" y="74" class="dim">$</text><text x="68" y="74" class="t" clip-path="url(#c)">neofetch</text>')
    t0 = 1.5
    for i, line in enumerate(ART):
        out.append(f'<text x="{x0}" y="{y0 + 70 + i * 32}" class="art ln" fill="{ART_SHADES[i]}" style="fill:{ART_SHADES[i]};animation-delay:{t0 + i * 0.08:.2f}s" xml:space="preserve">{escape(line)}</text>')
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
            for j, g in enumerate(("#7c3aed", "#a78bfa", "#c026d3", "#ec4899", "#f472b6", "#f97316", "#fb923c", "#ffffff")):
                out.append(f'<rect x="{xr + j * 38}" y="{y - 4}" width="32" height="18" rx="3" fill="{g}" stroke="#2c1f4a" class="ln" style="animation-delay:{d + j * 0.04:.2f}s"/>')
    yc = H - 26
    out.append(f'<text x="{x0}" y="{yc}" class="dim ln" style="animation-delay:{t0 + 2.2:.2f}s">$</text>')
    out.append(f'<rect x="68" y="{yc - 15}" width="10" height="20" fill="#f97316" class="cur"/>')
    out.append("</svg>")
    return "\n".join(out)

if __name__ == "__main__":
    data = stats(fetch())
    open(sys.argv[1] if len(sys.argv) > 1 else "terminal.svg", "w").write(svg(data))
