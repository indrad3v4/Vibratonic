# Vibratonic: Hack, Demo, Fund Offline

[![Sponsor Vibratonic](https://img.shields.io/badge/GitHub%20Sponsors-%E2%9D%A4-ff00a8?style=flat)](https://github.com/sponsors/indrad3v4)

### Turn any room into a funded hackathon in minutes.

## Vision
Vibratonic scales offline VibeCoding hackathons by bundling event setup, demo space, and funding rails into one neon‑themed app. Teams code without the cloud, investors browse on‑device, and a decentralised coding movement sparks wherever a laptop opens.

## Key Features
- **Offline‑first core** – session state caching and service‑worker hooks keep hackathons running even when Wi‑Fi drops.
- **One‑tap Hackathon Launcher** – the Create wizard spawns venues, teams, and submission tracking in a single flow.
- **MVP Showcase Gallery** – the `/pages` directory renders dynamic cards with media, funding goals, and tech stacks.
- **Funding Board** – investor feed links winning MVPs to sponsors with live activity and payment breakdowns.

## Quick Start (≤5 commands)
```bash
# 1. Get the code
$ git clone https://github.com/indrad3v4/Vibratonic.git
$ cd Vibratonic

# 2. Install dependencies with uv
$ uv sync

# 3. Launch locally (no cloud needed)
$ uv run streamlit run app.py
```
Runs fully offline; add `MOLLIE_API_KEY` later for live payments.

## Roadmap
- [ ] Service‑worker PWA for full offline caching
- [ ] FastAPI WebSocket backend
- [ ] PostgreSQL + Drizzle ORM storage
- [ ] Polish/English i18n stubs
- [ ] "AI Mentor" tips across the UI

## Why Sponsor?
Sponsoring Vibratonic fuels a self‑sustaining ecosystem where local hackers become investible founders, with transparent 20 % platform fees ensuring longevity. Backers gain early access to talent, brand visibility at grassroots events, and a direct hand in shaping open‑source tooling. [Pledge via GitHub Sponsors](https://github.com/sponsors/indrad3v4) and pick a tier that matches your vibe.

## Contributing & Licence
Pull requests and issue reports are welcome—just keep the tone friendly and code readable. This project is released under the MIT Licence. See `LICENSE` for details.

Ready to build the future of vibecoding together?
