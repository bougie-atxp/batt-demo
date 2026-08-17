# HANDOFF — project state & path to a real app

For anyone (future eng included) picking this up. Read README.md first for the
edit → build → deploy loop.

## Where this stands (2026-08-17)

- Playable single-file demo is live and fully offline-capable (fonts inlined).
- Client (Darren Battista, owner of Battista Bootcamp) has seen it and is in.
  Next step is an in-person session where he walks through his current
  Trainerize setup and lists everything the real app needs.
- Inputs still owed by Darren are tracked in `darren-punchlist.md` — Stripe
  access, content library, Trainerize export, brand files, domain, Apple dev
  account, coach list, schedule. Most build work past the demo is gated on
  these.

## Roadmap

### Stage 1 — playable v2 (no backend needed, can start now)
- Persistence: localStorage for completed workouts, PRs, joined challenges,
  streaks — so the demo survives refresh and feels alive across days.
- Every visible control does something; no dead buttons in front of a client.
- Demo reset (hidden gesture or `?reset=1`) to restore the canned state.
- PWA: manifest + service worker so Darren can Add-to-Home-Screen and carry
  it on his phone like a real app. Keep the zero-dependency rule.

### Stage 2 — real content (gated on punchlist)
- Ingest Trainerize export: real clients, program templates, pricing.
- Wire the actual video library (wherever it lives) into Train/On-Demand.
- Swap canned brand assets for Darren's real files.

### Stage 3 — real app (decision point, do NOT start before a sit-down)
- Choose PWA vs native iOS. Bias to boring, maintainable stack — this must be
  runnable by a normal contractor eng, not a research project.
- Backend: auth, Stripe payments (Darren's account, team-member access only),
  video hosting, workout/program data.
- Migration plan off Trainerize with zero client downtime.

## Next-session capture sheet (Trainerize walkthrough)

Get concrete answers while screen-sharing his Trainerize:
1. Which Trainerize features does he actually use weekly? (ignore the rest)
2. Program structure: how are workouts templated, assigned, progressed?
3. What do clients touch daily — logging, messaging, habit tracking?
4. Payments: what plans exist, how do people sign up today, churn points?
5. What does Trainerize do badly — the reason he wants out?
6. Coaches: what would other coaches need to run their own groups/challenges?
7. Non-negotiables for launch vs nice-to-have.

## Maintainer notes

- One source file: `src/index.template.html` (HTML+CSS+JS, ~1700 lines).
  `build.py` only injects the logo mark. No framework, no npm, no build deps
  beyond Python 3 stdlib.
- Deploy = push to `main`; GitHub Pages serves the repo root. Verify with the
  shasum check in README.md — Pages can lag a few minutes.
- The demo is demoed live on gym wifi: never reintroduce a network dependency.
- Git identity for this repo is set locally to the GitHub noreply address;
  keep it that way.

## QA (2026-08-17 agent sweep)

53-agent workflow: 6 parallel dimension reviews (handlers, nav, state, layout,
copy, robustness) with adversarial verification of every finding. 41 findings
confirmed, 5 refuted. Fixes landed same day.

### Fixed
- Browser back / iOS edge-swipe now pops the in-app nav stack (History API).
- Summary screen has a back button (was a dead end besides "Lock it in").
- Today's JOINED challenge pill kept a baked array index — broke after a coach
  published a new challenge. Now holds an object reference.
- Set tracker: can't edit weight/reps on a completed set (volume desync),
  unchecking the PR set re-arms the PR trigger, elapsed timer resets on start.
- PR flow is dynamic: popup shows the actual weight; locking it in updates the
  PR wall, lift history "best ever", and the Today tile.
- Dates are computed at load (greeting, week strip, HQ/booking rows,
  challenge start) — the demo never shows a stale calendar again.
- Fuel math consistent: meals sum to shown macros, ring is 1,710 of 2,600 cal
  (matches 200g/270g/80g targets), snapped meal macros match its calories.
- iOS polish: no input auto-zoom (maximum-scale=1), real safe-area insets,
  no pull-to-refresh, app-open animation no longer kills the splash-out.
- Desktop: phone frame no longer clips on short windows (flex centering bug).
- User text is HTML-escaped in chat / live chat / challenge builder.
- Pay sheet has a Cancel button; live-class viewers/chat reset per visit;
  Today tiles deep-link to the right Progress segment; copy contradictions
  fixed ("Open to everyone", weight-chart title, leaderboard streak syncs).

### Known limitations (accepted for demo)
- On-screen keyboard can cover the chat/live inputs on iOS (no
  visualViewport handling).
- Landscape phones / tablets >860px wide get the desktop frame view.
- Photo compare slider is a hidden range input — coarse on touch.
- You can reach the summary by completing only the last exercise; the demo
  doesn't force every set.
- Classes segment is sticky: "Book with Darren" on Today lands on HQ and the
  tab stays there until switched (state preservation, arguably correct).
