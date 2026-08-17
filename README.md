# BATT — Battista Bootcamp 2.0 demo

Playable prototype of a fitness-training app for Battista Bootcamp, replacing a
Trainerize-based setup. Personal project.

**Live:** https://bougie-atxp.github.io/batt-demo/

## What it is

A single self-contained HTML file that plays like an iOS app: fake springboard,
splash, and the app itself (Today / Train / Fuel / Crew / Progress tabs,
workout player, challenges, chat, PRs, on-demand classes). Zero dependencies,
zero network calls — the Montserrat variable font is base64-inlined, so it
works fully offline. Open `index.html` in any browser.

## Repo layout

| Path | Purpose |
|---|---|
| `src/index.template.html` | **The source. Edit this file.** |
| `assets/batt-mark-paths.html` | BATT logo mark (inner-SVG paths) injected at build |
| `assets/*.svg` | Logo source files (`batt-slim.svg` is where the mark came from) |
| `build.py` | Fills `<!--BATT_PATHS-->` placeholders → writes `index.html` |
| `index.html` | **Built output. Never edit by hand.** Served by GitHub Pages |
| `icon.png` | Springboard/app icon |
| `darren-punchlist.md` | Inputs still needed from the client (Darren Battista) |
| `HANDOFF.md` | Project state, known issues, roadmap to a real app |

`qa/` and `scratch/` are untracked local dirs (QA view snapshots, logo
intermediates).

## Workflow

```sh
# 1. edit src/index.template.html
python3 build.py        # 2. regenerate index.html
open index.html         # 3. check it
git add -A && git commit && git push   # 4. Pages redeploys in ~1–5 min
```

Verify a deploy landed:

```sh
curl -s https://bougie-atxp.github.io/batt-demo/index.html | shasum
shasum index.html   # hashes must match
```

## Rules

- All state is in-memory / demo-fake; a refresh resets the app. Intentional
  for now — see HANDOFF.md for the path to a real app.
- Keep the file dependency-free. No CDNs, no fetches — this gets demoed live
  on gym wifi.
