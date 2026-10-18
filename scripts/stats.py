#!/usr/bin/env python3
"""Таблица рекордов в аркадном стиле — живые цифры из GitHub API (GITHUB_TOKEN, USERNAME).

    python3 scripts/stats.py dist/scores.svg          # в workflow
    python3 scripts/stats.py scores.svg --demo        # выдуманные цифры, посмотреть вёрстку
"""
import json, os, random, sys, urllib.request
from kit import C, GRAD, MONO, card, esc, gt, gw, svg

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


def render(u):
    W, H = 1200, 400
    cc = u["contributionsCollection"]
    weeks = cc["contributionCalendar"]["weeks"]
    days = [d["contributionCount"] for w in weeks for d in w["contributionDays"]]
    cur, best = streaks(days)
    rows = [("1ST", "CONTRIBUTIONS", f'{cc["contributionCalendar"]["totalContributions"]:06d}'),
            ("2ND", "COMMITS", f'{cc["totalCommitContributions"]:06d}'),
            ("3RD", "PULL REQUESTS", f'{cc["totalPullRequestContributions"]:06d}'),
            ("4TH", "PUBLIC REPOS", f'{u["repos"]["totalCount"]:06d}'),
            ("5TH", "STREAK NOW", f"{cur} DAYS"),
            ("6TH", "BEST STREAK", f"{best} DAYS")]
    colors = [C["sun"], C["amber"], C["orange"], C["rose"], C["pink"], C["lilac"]]

    o = [card(W, H, gid="sc")]
    o.append(f'<g>{gt("HIGH SCORES", 300, 66, 20, C["rose"], font="pixel", anchor="middle", tracking=3)}'
             '<animate attributeName="opacity" values="1;1;0.2;1" keyTimes="0;0.7;0.8;1" dur="1.4s" repeatCount="indefinite"/></g>')
    o.append(gt("LAST 12 MONTHS", 300, 92, 10, C["muted"], font="pixel", anchor="middle", tracking=2))
    for i, (rank, name, score) in enumerate(rows):
        y = 140 + i * 40
        col = colors[i]
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{0.2 + i * 0.15:.2f}s" dur="0.01s" fill="freeze"/>'
                 + gt(rank, 60, y, 14, col, font="pixel")
                 + gt(name, 130, y, 14, col, font="pixel")
                 + gt(score, 540, y, 14, col, font="pixel", anchor="end") + "</g>")
    o.append(f'<line x1="600" y1="40" x2="600" y2="{H - 40}" stroke="{C["line"]}" stroke-dasharray="4 6"/>')

    # 16 недель пиксельными столбиками
    tot = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks[-16:]]
    peak = max(tot) or 1
    o.append(gt("16 WEEKS", 650, 66, 12, C["soft"], font="pixel", tracking=2))
    bx, by, cell = 650, 230, 9
    for i, v in enumerate(tot):
        n = max(0, round(v / peak * 14))
        for k in range(n):
            col = GRAD[min(2, k * 3 // 14)]
            o.append(f'<rect x="{bx + i * 32}" y="{by - k * (cell + 2)}" width="26" height="{cell}" fill="{col}" opacity="0">'
                     f'<animate attributeName="opacity" values="0;1" begin="{0.3 + (i * 0.04) + k * 0.03:.2f}s" dur="0.01s" fill="freeze"/></rect>')
        if n == 0:
            o.append(f'<rect x="{bx + i * 32}" y="{by}" width="26" height="2" fill="{C["faint"]}"/>')
    o.append(f'<text x="{bx + 16 * 32 - 6}" y="{by + 30}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{C["muted"]}">peak {peak} / week</text>')

    # языки — по основному языку каждого репозитория
    langs = {}
    for r in u["repos"]["nodes"]:
        if r["primaryLanguage"] and r["name"] not in SKIP:
            langs[r["primaryLanguage"]["name"]] = langs.get(r["primaryLanguage"]["name"], 0) + 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:4]
    total = sum(langs.values()) or 1
    o.append(gt("CHARACTERS", 650, 296, 12, C["soft"], font="pixel", tracking=2))
    x = 650
    for i, (n, c) in enumerate(top):
        label = f"{n.upper()} x{c}"
        col = [C["rose"], C["amber"], C["lilac"], C["sun"]][i]
        w = gw(label, 10, "pixel", 1) + 20
        o.append(f'<rect x="{x:.0f}" y="314" width="{w:.0f}" height="28" rx="4" fill="none" stroke="{col}"/>')
        o.append(gt(label, x + 10, 333, 10, col, font="pixel", tracking=1))
        x += w + 10
    o.append(f'<text x="650" y="370" font-family="{MONO}" font-size="12" fill="{C["muted"]}">public repos by main language · {total} counted · redrawn daily</text>')
    return svg(W, H, "\n".join(o), f"High scores: {rows[0][2].lstrip('0')} contributions in the last year, streak {cur} days, best {best}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "scores.svg"
    open(out, "w").write(render(demo() if "--demo" in sys.argv else fetch()))
    print("written", out)
