# Drafter briefs — cadence-tutor

Prompt templates for delegated drafting. The same brief text is used verbatim at every rung of the drafting ladder (local dispatch hook, cheap subagent, stronger subagent). Write each brief to `<course_dir>/.briefs/<name>.md` first — briefs are self-contained; the drafter has no conversation context.

Rules for every brief:

- State the exact output file paths to write. The drafter writes files directly — it should not print the content to stdout as its answer.
- Substitute real absolute paths for `<server_repo>` and `<client_repo>` from `<courses_dir>/config.json`, and forbid invention: "Only cite code you have actually opened. If you cannot find something, say NOT FOUND rather than guessing."
- Include: "Work directly in this session; do not spawn subagents." (A drafter that delegates produces no visible progress, and a dispatch watchdog may kill the run as stuck.)
- End with: "When finished, print exactly one line: `DRAFT_DONE <list of files written>`."

## Brief: syllabus digest (track day 0 or custom-track authoring, one per exploration area)

```
You are preparing source material for a Cadence internals course track on
<TRACK TITLE>.
Repos (read-only):
  server: <server_repo>
  client: <client_repo>

Task: digest <AREA — e.g. "how transfer tasks are generated and typed">.
Explore: <2-4 starting paths from the track file>.
Write to <course_dir>/.briefs/digest-<area>.md:
- the key files (verified paths) with 1-2 sentences each on their role
- the main types/functions involved (name + file:line)
- 3-5 facts a course should teach about this area
Only cite code you actually opened; write NOT FOUND rather than guessing.
Work directly in this session; do not spawn subagents.
When finished, print exactly one line: DRAFT_DONE <files written>
```

The supervisor assembles `syllabus.md` itself from these digests (cheap: the digests are small), following the syllabus format at the bottom of the track file and verifying every anchor path exists. For custom tracks, the same digest brief feeds the track file instead (add a request for a proposed week-by-week arc with per-day anchors and exercise ideas).

## Brief: daily lesson

```
You are drafting day <NN> of a Cadence internals course track on
<TRACK TITLE>. Audience: a Cadence server developer. Follow the file formats
below EXACTLY.

Repos (read-only):
  server: <server_repo>
  client: <client_repo>

Today's topic (from the syllabus):
<paste the full day NN syllabus entry, including anchors and exercise idea>

Context: yesterday covered <day NN-1 topic one-liner>; do not re-teach it.

Write these files:
1. <course_dir>/day-NN/lesson.md
2. <course_dir>/day-NN/quiz.md
3. <course_dir>/day-NN/.answer-key.md
4. <course_dir>/exercises/day-NN/exercise.go   (package dayNN)
5. <course_dir>/exercises/day-NN/exercise_test.go
6. <course_dir>/exercises/day-NN/README.md
7. <course_dir>/exercises/day-NN/.solution.go.txt

Format requirements (follow exactly):
<paste the full contents of references/lesson-format.md>

Hard rules:
- Every code snippet in lesson.md must be copied verbatim from a file you
  opened, cited as `server:path/file.go:LINE` or `client:path/file.go:LINE`.
- The exercise stub must compile (zero-value returns, no syntax holes); the
  test must fail against the stub and pass against .solution.go.txt. The
  module already exists at <course_dir>/exercises (module cadencetutor);
  standard library only. Run `cd <course_dir>/exercises && go test ./day-NN/...`
  yourself to confirm the failure before finishing.
- Intended solution length: 5-10 lines.
- Work directly in this session; do not spawn subagents.
When finished, print exactly one line: DRAFT_DONE <files written>
```

## Brief: quiz grading (first pass)

```
Grade a quiz. Below are the questions with the student's answers, followed by
the answer key. For each question output: verdict (correct / partial / wrong)
and a one-sentence justification. Then an overall score "N/M". Be strict on
facts, lenient on wording.

Write your grading to <course_dir>/day-NN/.grade-draft.md.

--- QUIZ WITH STUDENT ANSWERS ---
<paste day-NN/quiz.md>
--- ANSWER KEY ---
<paste day-NN/.answer-key.md>

When finished, print exactly one line: DRAFT_DONE <files written>
```

The supervisor reads `.grade-draft.md`, spot-checks any harsh or generous calls against the key, runs the exercise test itself, and writes the final `feedback.md` (the drafter never writes `feedback.md` directly). In the fully interactive flow the supervisor usually grades the quiz itself, since the answers are already in the conversation.

## Fallback ladder

1. Local dispatch hook at `<skill_dir>/scripts/local/dispatch.sh`, if the user installed one. Non-zero exit or two failed validations → step 2.
2. Cheap subagent, prompt = the same brief contents. Failed validation → step 3.
3. Stronger subagent. Failed validation → the supervisor writes the content itself (last resort).
