#!/usr/bin/env python3
"""Таблица рекордов: живые цифры из GitHub API (GITHUB_TOKEN, USERNAME), тёмная и светлая версии.

    python3 scripts/stats.py dist            # в workflow: dist/scores.svg и dist/scores-light.svg
    python3 scripts/stats.py out --demo      # выдуманные цифры, посмотреть вёрстку
"""
import json, os, random, sys, urllib.request
from kit import MONO, SANS, THEMES, esc, frame, gt, svg, write

USER = os.environ.get("USERNAME", "van1dalgrr-arch")
SKIP = {USER, "dotfiles", "Luma", "extensions", "Portfolio", "UserForge"}   # профиль и не-код не тянут языки в свою сторону

QUERY = """query($login: String!) { user(login: $login) {
  repos: repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER, isFork: false) {
    totalCount nodes { name primaryLanguage { name } } }
  contributionsCollection { totalCommitContributions totalPullRequestContributions
    contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } } } } }"""


def fetch():
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    if "errors" in data:
        sys.exit(f"GraphQL: {data['errors']}")
    return data["data"]["user"]


def demo():
    rnd = random.Random(3)
    weeks = [{"contributionDays": [{"contributionCount": rnd.choice([0, 0, 1, 3, 6, 9])} for _ in range(7)]} for _ in range(53)]
    return {"repos": {"totalCount": 15, "nodes": [{"name": f"r{i}", "primaryLanguage": {"name": l}} for i, l in enumerate(["Go"] * 9 + ["Java"] * 3 + ["Python", "Swift"])]},
            "contributionsCollection": {"totalCommitContributions": 412, "totalPullRequestContributions": 31,
                                        "contributionCalendar": {"totalContributions": 530, "weeks": weeks}}}


def streaks(days):
    longest = run = 0
    for c in days:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur = 0
    for i, c in enumerate(reversed(days)):   # сегодня без коммитов ещё не обрывает серию
        if c:
            cur += 1
        elif i:
            break
    return cur, longest


def render(u, theme):
    t = THEMES[theme]
    W, H = 1200, 300
    cc = u["contributionsCollection"]
    weeks = cc["contributionCalendar"]["weeks"]
    days = [d["contributionCount"] for w in weeks for d in w["contributionDays"]]
    cur, best = streaks(days)
    rows = [(f'{cc["contributionCalendar"]["totalContributions"]:,}', "contributions"),
            (f'{cc["totalCommitContributions"]:,}', "commits"),
            (f'{cc["totalPullRequestContributions"]:,}', "pull requests"),
            (f'{u["repos"]["totalCount"]}', "public repos"),
            (f"{cur}d", "current streak"),
            (f"{best}d", "best streak")]

    o = [frame(W, H, t, rx=16, fill=t["panel"])]
    o.append(f'<text x="40" y="52" font-family="{SANS}" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t["accent"]}">LAST 12 MONTHS</text>')
    for i, (big, small) in enumerate(rows):   # шесть рекордов сеткой 3×2
        x, y = 40 + (i % 3) * 180, 118 + (i // 3) * 110
        o.append(gt(big, x, y, 40, t["text"], tracking=-1.2))
        o.append(f'<text x="{x + 1}" y="{y + 28}" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{small}</text>')
    o.append(f'<line x1="600" y1="40" x2="600" y2="{H - 40}" stroke="{t["line"]}"/>')

    # 26 недель тонкими столбиками
    tot = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks[-26:]]
    peak = max(tot) or 1
    bx, by, bh = 640, 170, 110
    o.append(f'<text x="{bx}" y="52" font-family="{SANS}" font-size="13" fill="{t["muted"]}">Contributions per week · last 26 weeks</text>')
    step = 520 / len(tot)
    for i, v in enumerate(tot):
        h = max(2, v / peak * bh)
        o.append(f'<rect x="{bx + i * step:.1f}" y="{by - h:.1f}" width="{step - 6:.1f}" height="{h:.1f}" rx="2" fill="{t["accent"] if i == len(tot) - 1 else t["line2"] if v == 0 else t["faint"]}"/>')
    o.append(f'<text x="{bx + 520 - 6}" y="{by + 22}" text-anchor="end" font-family="{SANS}" font-size="12" fill="{t["faint"]}">peak {peak}</text>')

    # языки — по основному языку каждого репозитория
    langs = {}
    for r in u["repos"]["nodes"]:
        if r["primaryLanguage"] and r["name"] not in SKIP:
            langs[r["primaryLanguage"]["name"]] = langs.get(r["primaryLanguage"]["name"], 0) + 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:4]
    total = sum(n for _, n in top) or 1
    shades = [t["accent"], t["soft"], t["muted"], t["faint"]]
    o.append(f'<clipPath id="lb"><rect x="{bx}" y="216" width="514" height="8" rx="4"/></clipPath><g clip-path="url(#lb)">')
    x = bx
    for (n, c), col in zip(top, shades):
        w = c / total * 514
        o.append(f'<rect x="{x:.1f}" y="216" width="{w:.1f}" height="8" fill="{col}"/>')
        x += w
    o.append("</g>")
    x = bx
    for (n, c), col in zip(top, shades):
        o.append(f'<circle cx="{x + 4}" cy="{250}" r="4" fill="{col}"/>')
        label = f"{n} {c}"
        o.append(f'<text x="{x + 14}" y="254.5" font-family="{SANS}" font-size="13" fill="{t["soft"]}">{esc(n)} <tspan fill="{t["muted"]}">{c}</tspan></text>')
        x += len(label) * 7.4 + 34
    return svg(W, H, "\n".join(o), f"Last 12 months: {rows[0][0]} contributions, {rows[1][0]} commits, current streak {cur} days, best {best}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "dist"
    u = demo() if "--demo" in sys.argv else fetch()
    for theme in THEMES:
        write("scores", theme, render(u, theme), folder=out)
    print("written to", out)
