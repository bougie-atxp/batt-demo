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
| `icon.png` | Springboard/app icon (1024²; also the PWA icon source) |
| `icon-192.png`, `icon-512.png` | PWA icons (regenerate from icon.png with `sips -z`) |
| `manifest.webmanifest` | PWA manifest — makes Add-to-Home-Screen launch standalone |
| `sw.js` | Service worker: stale-while-revalidate cache (bump `CACHE` to force-refresh) |
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

## Demo state & reset

Interactions (habits, check-in, joined challenges, workout complete, PR,
snapped meal) persist in localStorage (`batt-demo-v1`) so the demo survives a
refresh. Two ways to restore the canned state:

- Open with `?reset=1` (e.g. `https://bougie-atxp.github.io/batt-demo/?reset=1`)
- Triple-tap the date line ("Monday · Aug 17 · Week 3") on the Today screen

## Install on a phone

Open the live URL in Safari (iOS) → Share → **Add to Home Screen**. It launches
full-screen like a native app and works offline after the first load (service
worker caches everything; fonts are inlined anyway).

## Rules

- Keep the file dependency-free. No CDNs, no fetches — this gets demoed live
  on gym wifi.
- All dates are computed at load — never hard-code a calendar date in a
  user-visible string.
