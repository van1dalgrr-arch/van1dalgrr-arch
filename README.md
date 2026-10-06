<picture><source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg"><img width="100%" src="assets/hero.svg" alt="van1dal — Go backend developer on the way to DevOps"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-about-light.svg"><img width="100%" src="assets/h-about.svg" alt="01 About"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/about-light.svg"><img width="100%" src="assets/about.svg" alt="Character sheet: backend developer in Go, on the way to DevOps. Main quest: Kubernetes"></picture>

I write **backend services in Go**: REST APIs on Gin, data in PostgreSQL, everything packed into **Docker**
and checked by **CI** on every push. The next chapter is **DevOps**: Kubernetes, infrastructure as code, the cloud.

I learn by shipping small, real things: a log collector, an uptime monitor, an orders API, a tiny HTTP framework,
a Telegram bot that talks to an LLM. Each one teaches me something the previous one didn't.

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-now-light.svg"><img width="100%" src="assets/h-now.svg" alt="02 Right now"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/roadmap-light.svg"><img width="100%" src="assets/roadmap.svg" alt="Roadmap as a cherry branch: Go + SQL, Docker and CI have bloomed; Kubernetes is blooming now; Helm, OpenTofu, Yandex Cloud and observability are buds"></picture>

- **Building** [logsence](https://github.com/van1dalgrr-arch/logsence): log ingestion and querying on Gin + PostgreSQL. Next: handler tests and a Docker image published by CI
- **Training** on Kubernetes in a local cluster (kubectl, Helm, k9s), then infrastructure as code with OpenTofu
- **Keeping** my whole dev environment in code: [dotfiles](https://github.com/van1dalgrr-arch/dotfiles). A clean Mac becomes my Mac in one command

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-projects-light.svg"><img width="100%" src="assets/h-projects.svg" alt="03 Projects"></picture>

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

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-stack-light.svg"><img width="100%" src="assets/h-stack.svg" alt="04 Stack"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/stack-light.svg"><img width="100%" src="assets/stack.svg" alt="Every day: Go, Gin, PostgreSQL, Docker, Git, zsh. In my projects: GitHub Actions, golangci-lint, Telegram API, LLM APIs. In training: Kubernetes, Helm, OpenTofu, Yandex Cloud"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-ci-light.svg"><img width="100%" src="assets/h-ci.svg" alt="05 How code ships"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/pipeline-light.svg"><img width="100%" src="assets/pipeline.svg" alt="CI as a metro map: git push departs, five jobs run in parallel (gofmt and vet, tests with -race, golangci-lint, govulncheck, hadolint and docker build), all green, merge; next line: Kubernetes"></picture>

Every Go repo rides the same line: it's the CI from
[logsence](https://github.com/van1dalgrr-arch/logsence/blob/main/.github/workflows/ci.yml), and new projects start with it through my `gonew` template.
Before a commit even leaves the laptop, **gitleaks** checks it for secrets.

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-desk-light.svg"><img width="100%" src="assets/h-desk.svg" alt="06 Where I work"></picture>

<img src="https://raw.githubusercontent.com/van1dalgrr-arch/dotfiles/main/docs/desktop.jpg" width="100%" alt="Ghostty and Zed tiled by AeroSpace over a sakura wallpaper">

A MacBook Air with **8 GB of RAM**, so everything is tuned to stay light: **Ghostty** and **AeroSpace** tiling,
a hand-written zsh prompt, **Zed** with my own Dev Night / Dev Day themes (ported to GoLand too)
and **OrbStack** instead of Docker Desktop.

<a href="https://github.com/van1dalgrr-arch/dotfiles"><picture><source media="(prefers-color-scheme: light)" srcset="assets/dotfiles-light.svg"><img width="100%" src="assets/dotfiles.svg" alt="dotfiles: my whole Mac as code"></picture></a>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-stats-light.svg"><img width="100%" src="assets/h-stats.svg" alt="07 Stats"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/stats-light.svg"><img width="100%" src="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/stats.svg" alt="GitHub stats: contributions, commits, streaks, weekly activity and languages"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/snake-light.svg"><img width="100%" src="https://raw.githubusercontent.com/van1dalgrr-arch/van1dalgrr-arch/output/snake.svg" alt="A snake eating the contribution graph"></picture>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/h-contact-light.svg"><img width="100%" src="assets/h-contact.svg" alt="08 Contact"></picture>

<p>
  <a href="https://github.com/van1dalgrr-arch"><img src="https://img.shields.io/badge/github-van1dalgrr--arch-0a0a0b?style=for-the-badge&logo=github&logoColor=ffb3c7&labelColor=0a0a0b" alt="GitHub"></a>
  <a href="mailto:van1dalgrr@gmail.com"><img src="https://img.shields.io/badge/mail-van1dalgrr@gmail.com-0a0a0b?style=for-the-badge&logo=gmail&logoColor=ffb3c7&labelColor=0a0a0b" alt="Email"></a>
</p>

Write in English or Russian.

<picture><source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg"><img width="100%" src="assets/footer.svg" alt="mata ne: see you, thanks for stopping by"></picture>

<sub>Every image here is an SVG drawn by [`scripts/build.py`](scripts/build.py), headlines in Noto Serif JP baked into paths.
Stats and the snake are redrawn daily by [a workflow](.github/workflows/profile.yml).</sub>
