<picture><source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg"><img width="100%" src="assets/hero.svg" alt="van1dal — Go backend developer moving into DevOps"></picture>

<br>

I build **backend services in Go** (REST APIs on Gin with PostgreSQL), package them in **Docker**, and check
every push with **CI**. Now I'm moving further into **DevOps**: Kubernetes, infrastructure as code, cloud.

I learn by shipping small, real projects: a log collector, an uptime monitor, an orders API, a tiny HTTP framework,
a Telegram AI bot. Each one adds a skill I didn't have before.

## 🧭 Right now

- **Building** [logsence](https://github.com/van1dalgrr-arch/logsence): log ingestion and querying on Gin + PostgreSQL. Next up: handler tests and a Docker image published by CI
- **Learning** Kubernetes on a local cluster (kubectl, Helm, k9s), then infrastructure as code with OpenTofu
- **Keeping** my whole dev environment in code: [dotfiles](https://github.com/van1dalgrr-arch/dotfiles). A clean Mac becomes my Mac in one command

<picture><source media="(prefers-color-scheme: light)" srcset="assets/roadmap-light.svg"><img width="100%" src="assets/roadmap.svg" alt="Roadmap: Go + SQL, Docker and CI done; learning Kubernetes now; next Helm, OpenTofu, Yandex Cloud, observability"></picture>

## 🛠️ Projects

Every card is a link. All of them are Go.

<p>
  <a href="https://github.com/van1dalgrr-arch/logsence"><picture><source media="(prefers-color-scheme: light)" srcset="assets/card-logsence-light.svg"><img width="49%" src="assets/card-logsence.svg" alt="logsence: log collection service on Gin + PostgreSQL"></picture></a>
  <a href="https://github.com/van1dalgrr-arch/OrderGo"><picture><source media="(prefers-color-scheme: light)" srcset="assets/card-ordergo-light.svg"><img width="49%" src="assets/card-ordergo.svg" alt="OrderGo: REST API for orders"></picture></a>
</p>
<p>
  <a href="https://github.com/van1dalgrr-arch/watchdog"><picture><source media="(prefers-color-scheme: light)" srcset="assets/card-watchdog-light.svg"><img width="49%" src="assets/card-watchdog.svg" alt="watchdog: uptime monitor"></picture></a>
  <a href="https://github.com/van1dalgrr-arch/Pulse"><picture><source media="(prefers-color-scheme: light)" srcset="assets/card-pulse-light.svg"><img width="49%" src="assets/card-pulse.svg" alt="Pulse: small HTTP framework for Go"></picture></a>
</p>
<p>
  <a href="https://github.com/van1dalgrr-arch/MINI-deploy"><picture><source media="(prefers-color-scheme: light)" srcset="assets/card-mini-deploy-light.svg"><img width="49%" src="assets/card-mini-deploy.svg" alt="MINI-deploy: deployment API for DevOps practice"></picture></a>
  <a href="https://github.com/van1dalgrr-arch/NEXA-AI-BOT"><picture><source media="(prefers-color-scheme: light)" srcset="assets/card-nexa-light.svg"><img width="49%" src="assets/card-nexa.svg" alt="NEXA AI: Telegram bot with an LLM"></picture></a>
</p>

## 🧰 Stack

Sorted by how I actually use it, not by how good it looks on a list.

<picture><source media="(prefers-color-scheme: light)" srcset="assets/stack-light.svg"><img width="100%" src="assets/stack.svg" alt="Every day: Go, Gin, PostgreSQL, Docker, Git, zsh. In projects: GitHub Actions, golangci-lint, Telegram Bot API, LLM APIs. Learning: Kubernetes, Helm, OpenTofu, Yandex Cloud"></picture>

## 🚢 How my code ships

Every Go project gets the same path from commit to image. It's the same CI that runs in
[logsence](https://github.com/van1dalgrr-arch/logsence/blob/main/.github/workflows/ci.yml),
and new projects start with it via my `gonew` template.

<picture><source media="(prefers-color-scheme: light)" srcset="assets/pipeline-light.svg"><img width="100%" src="assets/pipeline.svg" alt="git push runs gofmt, tests, golangci-lint, govulncheck and a Docker build in parallel; all green, then merge; next: image to Kubernetes"></picture>

Before a commit even leaves my laptop, **gitleaks** checks it for secrets in every repo.

## 💻 Where I work

<img src="https://raw.githubusercontent.com/van1dalgrr-arch/dotfiles/main/docs/desktop.jpg" width="100%" alt="Ghostty and Zed tiled by AeroSpace over a sakura wallpaper">

A MacBook Air with **8 GB of RAM**, so everything is tuned to stay light: **Ghostty** + **AeroSpace** tiling,
a hand-written zsh prompt, **Zed** with my own Dev Night / Dev Day themes (also ported to GoLand),
and **OrbStack** instead of Docker Desktop. All of it lives in dotfiles: `bootstrap.sh` sets up a clean Mac,
`dot doctor` checks that everything is in place, and CI tests the setup itself.

<a href="https://github.com/van1dalgrr-arch/dotfiles"><picture><source media="(prefers-color-scheme: light)" srcset="assets/dotfiles-light.svg"><img width="100%" src="assets/dotfiles.svg" alt="dotfiles: macOS dev environment as code"></picture></a>

## 📊 Activity

<picture><source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/stats-light.svg"><img width="100%" src="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/stats.svg" alt="GitHub stats: contributions, commits, streaks, weekly activity and languages"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/snake-light.svg"><img width="100%" src="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/snake.svg" alt="Contribution graph being eaten by a snake"></picture>

## 📫 Contact

[![GitHub](https://img.shields.io/badge/van1dalgrr--arch-0d1117?style=for-the-badge&logo=github&logoColor=white)](https://github.com/van1dalgrr-arch)
[![Email](https://img.shields.io/badge/van1dalgrr@gmail.com-0d1117?style=for-the-badge&logo=gmail&logoColor=EA4335)](mailto:van1dalgrr@gmail.com)

Write in English or Russian.

<picture><source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg"><img width="100%" src="assets/footer.svg" alt="thanks for stopping by"></picture>

<sub>Every image here is an SVG drawn by [`scripts/build.py`](scripts/build.py); stats and the snake are redrawn daily by
[a workflow](.github/workflows/profile.yml). Source: [van1dalgrr-arch/van1dalgrr-arch](https://github.com/van1dalgrr-arch/van1dalgrr-arch).</sub>
