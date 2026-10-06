"""Live stats card for the profile, drawn in the same style as the rest of assets/.

Runs in .github/workflows/profile.yml with GITHUB_TOKEN and writes into dist/:

    python3 scripts/stats.py dist          # real data from the GitHub GraphQL API
    python3 scripts/stats.py dist --demo   # made-up numbers, to preview the layout locally
"""

import datetime as dt
import json
import os
import random
import sys
import urllib.request
from pathlib import Path

from svgkit import MONO, SANS, THEMES, blossom, esc, gtext, paper, svg

LOGIN = "van1dalgrr-arch"
# Not part of the Go/DevOps picture (or not code at all), so they stay out of the language bar.
EXCLUDE = {"van1dalgrr-arch", "dotfiles", "Luma", "Portfolio", "extensions", "UserForge",
           "SpringBoot-Templates", "TelegramRepo", "java-calculator"}

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { name languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
  }
}
"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL errors: {data['errors']}")
    return data["data"]["user"]


def demo():
    random.seed(7)
    today = dt.date.today()
    days = [{"date": (today - dt.timedelta(days=i)).isoformat(),
             "contributionCount": random.choice([0, 0, 1, 2, 3, 5, 8, 12]) if i < 120 else random.choice([0, 0, 0, 1])}
            for i in range(370)][::-1]
    weeks = [{"contributionDays": days[i:i + 7]} for i in range(0, len(days), 7)]
    langs = [("Go", "#00ADD8", 420000), ("Shell", "#89e051", 60000), ("Dockerfile", "#384d54", 9000), ("Makefile", "#427819", 4000)]
    return {
        "createdAt": "2026-07-01T00:00:00Z",
        "contributionsCollection": {
            "totalCommitContributions": 412, "totalPullRequestContributions": 37,
            "contributionCalendar": {"totalContributions": sum(d["contributionCount"] for d in days), "weeks": weeks},
        },
        "repositories": {"totalCount": 14, "nodes": [
            {"name": "demo", "languages": {"edges": [{"size": s, "node": {"name": n, "color": c}} for n, c, s in langs]}}]},
    }


def streaks(days):
    """Current and longest run of days with at least one contribution.
    An empty today doesn't break the current streak: the day isn't over yet."""
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur = 0
    for i, c in enumerate(reversed(counts)):
        if c:
            cur += 1
        elif i > 0:
            break
    return cur, longest


def render(u, theme):
    t = THEMES[theme]
    W, H = 1200, 320
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    cur, longest = streaks(days)

    o = [paper(W, H, t)]
    o.append(gtext("統計", 30, 50, 22, t["deep"], weight=900))
    o.append(f'<text x="84" y="45" font-family="{MONO}" font-size="13" fill="{t["muted"]}">last 12 months '
             f'<tspan fill="{t["faint"]}">· redrawn every day by GitHub Actions</tspan></text>')

    tiles = [
        (f'{cc["contributionCalendar"]["totalContributions"]:,}', "contributions", True),
        (f'{cc["totalCommitContributions"]:,}', "commits", False),
        (f'{cc["totalPullRequestContributions"]:,}', "pull requests", False),
        (str(u["repositories"]["totalCount"]), "public repos", False),
        (f"{cur}d", "current streak", True),
        (f"{longest}d", "longest streak", False),
    ]
    for i, (big, small, pink) in enumerate(tiles):
        x = 30 + (i % 3) * 172
        y = 74 + (i // 3) * 112
        o.append(f'<rect x="{x}" y="{y}" width="160" height="100" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        o.append(gtext(big, x + 18, y + 54, 38, t["deep"] if pink else t["ink"], weight=900))
        o.append(f'<text x="{x+18}" y="{y+80}" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{esc(small)}</text>')

    # weekly activity as falling-petal columns: one stem per week, a blossom on top
    weeks = cc["contributionCalendar"]["weeks"][-16:]
    totals = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    peak = max(totals) or 1
    bx, by, bw, bh = 570, 92, 320, 170
    o.append(f'<text x="{bx}" y="84" font-family="{MONO}" font-size="12" fill="{t["muted"]}">last 16 weeks</text>')
    o.append(f'<line x1="{bx}" y1="{by+bh}" x2="{bx+bw}" y2="{by+bh}" stroke="{t["faint"]}"/>')
    step = bw / len(totals)
    for i, v in enumerate(totals):
        h = v / peak * (bh - 26)
        x = bx + i * step + step / 2
        top = by + bh - h
        o.append(f'<line x1="{x:.1f}" y1="{by+bh}" x2="{x:.1f}" y2="{top:.1f}" stroke="{t["branch"]}" stroke-width="3" stroke-linecap="round">'
                 f'<animate attributeName="y2" from="{by+bh}" to="{top:.1f}" dur="0.8s" begin="{i*0.04:.2f}s" fill="freeze"/></line>')
        if v:
            o.append(blossom(x, top, 4 + 7 * v / peak, t, rot=i * 23))
    o.append(f'<text x="{bx+bw}" y="{by+bh+22}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["muted"]}">peak {peak} / week</text>')

    # languages by bytes across public, non-excluded repos: the top one pink, the rest in ink
    sizes = {}
    for r in u["repositories"]["nodes"]:
        if r["name"] in EXCLUDE:
            continue
        for e in r["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    total = sum(sizes.values()) or 1
    top5 = sorted(sizes.items(), key=lambda kv: -kv[1])[:5]
    shades = [t["deep"], t["ink"], t["muted"], t["faint"], t["border"]]
    lx, lw = 930, 240
    o.append(f'<text x="{lx}" y="84" font-family="{MONO}" font-size="12" fill="{t["muted"]}">languages</text>')
    o.append(f'<clipPath id="lb"><rect x="{lx}" y="96" width="{lw}" height="10" rx="5"/></clipPath><g clip-path="url(#lb)">')
    o.append(f'<rect x="{lx}" y="96" width="{lw}" height="10" fill="{t["ghost"]}"/>')
    x = lx
    for (n, sz), c in zip(top5, shades):
        w = sz / total * lw
        o.append(f'<rect x="{x:.1f}" y="96" width="{w:.1f}" height="10" fill="{c}"/>')
        x += w
    o.append("</g>")
    for i, ((n, sz), c) in enumerate(zip(top5, shades)):
        y = 140 + i * 26
        o.append(f'<circle cx="{lx+6}" cy="{y-4}" r="5" fill="{c}"/>')
        o.append(f'<text x="{lx+20}" y="{y}" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["text"]}">{esc(n)}</text>')
        o.append(f'<text x="{lx+lw}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{sz / total * 100:.1f}%</text>')

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    o.append(f'<text x="{W-30}" y="45" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{stamp}</text>')
    return svg(W, H, "\n".join(o), f"GitHub stats: {tiles[0][0]} contributions in the last year, current streak {cur} days")


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    out.mkdir(parents=True, exist_ok=True)
    u = demo() if "--demo" in sys.argv else fetch()
    for theme in THEMES:
        (out / f"stats{'' if theme == 'dark' else '-light'}.svg").write_text(render(u, theme))
    print(f"stats written to {out}/")


if __name__ == "__main__":
    main()
