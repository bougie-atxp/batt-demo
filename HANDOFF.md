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

### Stage 1 — playable v2 — DONE 2026-08-17
- ✅ Persistence: localStorage (`batt-demo-v1`) for habits, check-in, joined
  challenges, workout complete, PR, snapped meal. Mutations are factored into
  `apply*()` functions replayed silently by the `restore()` block at script end.
- ✅ Demo reset: `?reset=1` URL param, or triple-tap the date line on Today.
- ✅ PWA: manifest + service worker (stale-while-revalidate) + icons.
  Add-to-Home-Screen launches standalone and works offline.

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

### Second sweep (same day) — adversarial verify of the fix commit

19-agent workflow re-reviewed commit 3f941e7 itself: 14 findings confirmed,
1 refuted. All 14 fixed in the follow-up commit:
- Nav/history was desynced 4 ways (back() never consumed its pushState entry,
  tab switches/summary orphaned entries, forward-swipe popped backward, the
  340ms debounce swallowed popstates). Rewritten: history entry depth
  (`state.batt`) is the source of truth; popstate syncs the stack to it;
  in-app back calls history.back(); base-screen jumps rewind via history.go().
  Logic unit-simulated in node across 9 scenarios (see git log for receipts).
- PR flow: re-logging works (a second, heavier PR updates the wall); trigger
  compares against the current best (`bestW`, seeded 310) instead of a
  hardcoded 315, so a sub-best weight no longer announces "NEW PR".
- Dates: booking rows sort chronologically on Fri/Sat, HQ row says "Today" on
  Saturdays, weekstrip dot marks actual future weekend days, remaining
  hard-coded challenge dates (Sep 1 / Aug 25 / Sep 5) made dynamic.
- Escaping moved from store-time to render-site (no more double-escaped
  entities in textContent surfaces); `.livebar` bottom padding uses the
  bottom safe-area inset; Today macro rings refresh after snapping a meal.

### Known limitations (accepted for demo)
- On-screen keyboard can cover the chat/live inputs on iOS (no
  visualViewport handling).
- Landscape phones / tablets >860px wide get the desktop frame view.
- Photo compare slider is a hidden range input — coarse on touch.
- You can reach the summary by completing only the last exercise; the demo
  doesn't force every set.
- Classes segment is sticky: "Book with Darren" on Today lands on HQ and the
  tab stays there until switched (state preservation, arguably correct).
