---
name: cadence-tutor
description: Turn the agent into a daily tutor that teaches a human developer Cadence internals from real source code. Load this skill when the user asks for a Cadence internals lesson, wants to start or resume a Cadence course, or says things like "cadence tutor", "next lesson", or "teach me how <Cadence subsystem> works". Each day is a 10-15 minute unit — a source-grounded lesson, an interactive quiz, and a small Go exercise the user implements and the agent grades on the spot.
version: 0.1.0
---

# cadence-tutor

An interactive daily curriculum engine that teaches Cadence internals to a human, one short lesson per day, grounded in the upstream source. This is the inverse of `cadence-developer`: that skill teaches agents to build Cadence applications; this one uses the agent as an instructor so a person can learn how Cadence itself works.

Topics are **tracks** — data files in `tracks/*.md`. Each track has a header (slug, days, source repos by role) and a week-by-week arc with anchor file paths. The engine below is track-agnostic.

**The user learns, not the agent.** Every day runs the same interactive loop:

1. **Read** — present the day's lesson in chat (from `day-NN/lesson.md`).
2. **Answer** — ask the quiz questions interactively. Use the agent's structured question mechanism if one exists (multiple-choice prompts); otherwise ask in chat and wait for answers. Randomize which position holds the correct option.
3. **Do** — the user implements 5-10 lines of Go in `exercises/day-NN/exercise.go` until the provided test passes. Wait for them to say "done" or "skip".
4. **Grade** — grade quiz answers immediately against the hidden answer key, run the exercise test, and deliver feedback in chat.

## Workspace and configuration

- `<skill_dir>` — this skill's directory.
- `<courses_dir>` — `~/cadence-courses` (create on first use).
- `<course_dir>` — `<courses_dir>/<slug>/` per track: `syllabus.md`, `progress.json`, `day-NN/`, and `exercises/` (a standalone Go module named `cadencetutor`, standard library only). Never scaffold exercises inside a repository checkout.

Tracks reference repos by role (`server:`, `client:`). Local checkout paths live in `<courses_dir>/config.json`:

```json
{"repos": {"server": "/path/to/cadence", "client": "/path/to/cadence-go-client"}}
```

On first use (or when a track needs a role that is not configured), ask the user where their checkouts live, or offer to clone the missing repo shallowly into `<courses_dir>/.repos/<name>`. Lessons cite code as `server:path/file.go:LINE`, so a local checkout of each repo the track uses is required.

## Modes

Invocation: `cadence-tutor [next [track] | start <track> | tracks | status [track] | reset <track> | custom "<topic>"]` — default `next`.

- **next [track]** — run today's lesson for the track. With no track argument: if exactly one track under `<courses_dir>` has in-flight progress, use it; otherwise list options and ask.
- **start <track>** — begin a track: scaffold `<course_dir>`, generate the syllabus (step 1), then run day 1 (or stop after the syllabus if the user only wants setup).
- **tracks** — list track files (curated and `custom-*`) with day counts, a one-line description, and per-track progress where started. No generation.
- **status [track]** — print progress for one or all started tracks.
- **reset <track>** — reset that track's `progress.json` to restart from day 1.
- **custom "<topic>"** — generate a new track file for an arbitrary Cadence topic (see "Custom tracks"), then offer to start it.

## State

Per-track ledger at `<course_dir>/progress.json`, managed by `scripts/progress.py` (a small standard-library module with no CLI; call its functions via `python3 -c`):

```bash
python3 -c "import sys; sys.path.insert(0,'<skill_dir>/scripts'); import progress; print(progress.current_day('<course_dir>/progress.json'))"
```

Functions: `current_day`, `mark_delivered`, `record_grade`, `status`, `ungraded_days`.

## Step 0: resolve the drafter

Lesson drafting is delegated to keep cost down; the supervising agent only briefs, validates, and presents. Ladder, in order:

1. **Local dispatch hook (optional)** — if an executable exists at `<skill_dir>/scripts/local/dispatch.sh`, run it as `dispatch.sh --workdir <course_dir> --brief <brief-file>`. This is a user-provided integration point for a local or cheaper drafting model; nothing in this repo installs one. Exit code 0 means the draft was written; any other exit code means fall to the next rung.
2. **Cheap subagent** — a delegated agent on the cheapest available model, prompt = the brief file contents.
3. **Stronger subagent** — same brief on a mid-tier model, after a failed validation on rung 2.
4. **Draft directly** — last resort: the supervising agent writes the content itself.

Move down a rung after a dispatch failure or two failed validations. Briefs are self-contained files (templates in `references/drafter-briefs.md`) — the drafter has no conversation context.

## Step 1: starting a track — scaffold and syllabus

On `start <track>` (or `next` when `<course_dir>/syllabus.md` is missing):

1. Read `tracks/<track>.md` — it defines days, repo roles, the week-by-week arc, and the syllabus format.
2. Resolve repo paths from `<courses_dir>/config.json` (see "Workspace and configuration").
3. Scaffold `<course_dir>/` with `exercises/go.mod` (`module cadencetutor`, a current stable Go version) and `.briefs/`.
4. If the track's anchor hints are sparse for some area, dispatch one or two exploration digest briefs (template in `references/drafter-briefs.md`).
5. Assemble `syllabus.md` yourself from the arc plus digests, following the syllabus format at the bottom of the track file. Verify every anchor path exists with `ls` or `grep` before finalizing — anchor hints in track files are starting points, and the repos evolve.

## Step 2: generate today's lesson

Let `N = current_day(<course_dir>/progress.json)`. If `None`, the track is complete — congratulate the user and suggest `tracks` for what to study next.

If `<course_dir>/day-NN/lesson.md` does not exist:

1. Read the day N entry from `<course_dir>/syllabus.md`.
2. Build the lesson brief (template in `references/drafter-briefs.md`), write it to `<course_dir>/.briefs/day-NN-lesson.md`, and dispatch it down the ladder.
3. Validate independently before presenting:
   - Spot-check at least three `file:line` citations with `grep`; the cited symbol must appear within 15 lines of the cited line. Fix drift in place; reject drafts with fabricated references.
   - `cd <course_dir>/exercises && go vet ./day-NN/... && go test ./day-NN/...` — must compile and fail (red).
   - Swap in `.solution.go.txt`, run `go test -count=1 ./day-NN/...` — must pass (green) — then restore the stub. Use `-count=1`: the drafter's own test runs may have populated the build cache.
   - `quiz.md` has 3-5 questions; `lesson.md` is 700-1600 words.

   Fix small defects in place. On structural defects, re-dispatch or fall down the ladder.

## Step 3: present the lesson interactively

1. **Read** — present `day-NN/lesson.md` in chat as formatted markdown. State the track, day number, and topic prominently.
2. **Quiz** — read `day-NN/quiz.md` and `day-NN/.answer-key.md`. Ask the questions one at a time (or grouped when short). Randomize which position holds the correct option. Do not show the answer key.
3. **Grade the quiz immediately** — for each question: correct, partial, or wrong, plus a one-sentence explanation citing the lesson or a `file:line`. Give an overall score.
4. **Exercise** — tell the user what to implement (from `exercises/day-NN/README.md`), the file to edit, and the test command (`cd <course_dir>/exercises && go test ./day-NN/...`). Say: "Edit the file and let me know when you're done, or say 'skip' to see the solution."
5. **Wait, then grade the exercise** — when the user says done, run the test and read their `exercise.go`. Report pass or fail with a test output summary, and two or three sentences comparing their approach to `.solution.go.txt`. On "skip", show the solution and explain it briefly.
6. **Record** — `mark_delivered(path, N, "<topic>")` and `record_grade(path, N, "<quiz_score>", <exercise_pass>, "<note>")`.
7. **Wrap up** — one sentence on what tomorrow covers and what to re-read if anything was shaky.

## Custom tracks

`custom "<topic>"` builds a new track file for any Cadence topic:

1. Slugify the topic to `custom-<slug>`. If a curated track already covers it, point the user there instead.
2. Write one or two exploration digest briefs for the topic (same template as step 1) and dispatch down the ladder. Digests land in `<courses_dir>/.briefs/`.
3. Curate `<skill_dir>/tracks/custom-<slug>.md` yourself from the digests: the shared header block (slug, days — usually 10-15 for a narrow topic, repo roles, `status: custom`) and the same week-by-week arc format as curated tracks. Grep-verify every anchor path.
4. Offer to start it. If the track turns out well, suggest contributing it to this repository as a curated track.

## Error recovery

| Issue | Fix |
| --- | --- |
| Drafter rung unavailable or failing | Fall down the ladder |
| Validation fails twice at one rung | Fall down a rung; note it in the ledger |
| Anchor file missing from the repo | Fix `syllabus.md` in place |
| User wants to redo a day | Reset that day in `progress.json` |
| Ambiguous `next` (several tracks in flight) | Ask which track |
| Repo role not configured | Ask for the checkout path or offer a shallow clone |

## References

- `references/lesson-format.md` — exact per-day file formats and the validation checklist.
- `references/drafter-briefs.md` — brief templates for digests, daily lessons, and quiz grading.
- `tracks/` — available curricula; each file is self-describing.
