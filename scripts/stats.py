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

from svgkit import MONO, SANS, THEMES, esc, frame, svg, text_w

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
    W, H = 1200, 300
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    cur, longest = streaks(days)

    o = [frame(W, H, t, glows=((0.0, 0.0, 0.4, "cyan"), (1.0, 1.0, 0.5, "purple")), uid="st"),
         f'<defs><linearGradient id="bars" x1="0" x2="0" y1="1" y2="0"><stop offset="0" stop-color="{t["purple"]}"/>'
         f'<stop offset="1" stop-color="{t["cyan"]}"/></linearGradient></defs>']
    o.append(f'<text x="36" y="46" font-family="{MONO}" font-size="14" fill="{t["muted"]}"><tspan fill="{t["purple"]}">$</tspan> '
             f'gh stats --last-year   <tspan fill="{t["faint"]}"># updated daily by GitHub Actions</tspan></text>')

    # number tiles
    tiles = [
        (f'{cc["contributionCalendar"]["totalContributions"]:,}', "contributions", t["purple"]),
        (f'{cc["totalCommitContributions"]:,}', "commits", t["cyan"]),
        (f'{cc["totalPullRequestContributions"]:,}', "pull requests", t["cyan"]),
        (str(u["repositories"]["totalCount"]), "public repos", t["purple"]),
        (f"{cur} d", "current streak", t["green"]),
        (f"{longest} d", "longest streak", t["yellow"]),
    ]
    for i, (big, small, c) in enumerate(tiles):
        x = 36 + (i % 3) * 170
        y = 70 + (i // 3) * 102
        o.append(f'<rect x="{x}" y="{y}" width="158" height="90" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        o.append(f'<text x="{x+18}" y="{y+46}" font-family="{SANS}" font-size="30" font-weight="800" fill="{c}">{esc(big)}</text>')
        o.append(f'<text x="{x+18}" y="{y+70}" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{esc(small)}</text>')

    # weekly activity, last 16 weeks, bars grow in on load
    weeks = cc["contributionCalendar"]["weeks"][-16:]
    totals = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    peak = max(totals) or 1
    bx, by, bw, bh = 570, 84, 300, 150
    o.append(f'<text x="{bx}" y="76" font-family="{MONO}" font-size="12" fill="{t["muted"]}">last 16 weeks</text>')
    o.append(f'<line x1="{bx}" y1="{by+bh}" x2="{bx+bw}" y2="{by+bh}" stroke="{t["border"]}"/>')
    step = bw / len(totals)
    for i, v in enumerate(totals):
        h = max(2, v / peak * (bh - 10))
        x = bx + i * step + 1.5
        o.append(f'<rect x="{x:.1f}" y="{by+bh-h:.1f}" width="{step-3:.1f}" height="{h:.1f}" rx="2" fill="url(#bars)" opacity="{0.45 + 0.55 * v / peak:.2f}">'
                 f'<animate attributeName="height" from="0" to="{h:.1f}" dur="0.9s" begin="{i*0.03:.2f}s" fill="freeze"/>'
                 f'<animate attributeName="y" from="{by+bh}" to="{by+bh-h:.1f}" dur="0.9s" begin="{i*0.03:.2f}s" fill="freeze"/></rect>')
    o.append(f'<text x="{bx}" y="{by+bh+22}" font-family="{MONO}" font-size="11" fill="{t["faint"]}">peak {peak}/week</text>')

    # languages by bytes across public, non-excluded repos
    sizes, colors = {}, {}
    for r in u["repositories"]["nodes"]:
        if r["name"] in EXCLUDE:
            continue
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            sizes[n] = sizes.get(n, 0) + e["size"]
            colors[n] = e["node"]["color"] or t["muted"]
    total = sum(sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:5]
    lx, lw = 910, 254
    o.append(f'<text x="{lx}" y="76" font-family="{MONO}" font-size="12" fill="{t["muted"]}">languages</text>')
    o.append(f'<clipPath id="lb"><rect x="{lx}" y="88" width="{lw}" height="12" rx="6"/></clipPath>')
    x = lx
    o.append('<g clip-path="url(#lb)">')
    o.append(f'<rect x="{lx}" y="88" width="{lw}" height="12" fill="{t["chip"]}"/>')
    for n, s in top:
        w = s / total * lw
        o.append(f'<rect x="{x:.1f}" y="88" width="{w:.1f}" height="12" fill="{colors[n]}"/>')
        x += w
    o.append("</g>")
    for i, (n, s) in enumerate(top):
        y = 132 + i * 24
        o.append(f'<circle cx="{lx+6}" cy="{y-4}" r="5" fill="{colors[n]}"/>')
        o.append(f'<text x="{lx+20}" y="{y}" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["text"]}">{esc(n)}</text>')
        pct = f"{s / total * 100:.1f}%"
        o.append(f'<text x="{lx+lw}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{pct}</text>')

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    o.append(f'<text x="{W-36}" y="46" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{stamp}</text>')
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
