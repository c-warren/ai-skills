# Lesson format — cadence-tutor

Every day directory `<course_dir>/day-NN/` contains exactly these files, and `<course_dir>/exercises/day-NN/` contains the exercise package. Total intended effort: 10-15 minutes (about 7 minutes reading, 3 minutes quiz, 4 minutes exercise).

## day-NN/lesson.md (~1000-1400 words)

```markdown
# Day NN: <topic title>

*Yesterday:* <2-3 sentence recap of day NN-1; omit on day 1.>

## The idea
<Plain-English explanation of today's concept. No code yet. Analogy welcome.>

## In the code
<Walk through 2-4 anchor locations with REAL, VERIFIED references in the form
`path/to/file.go:123` (repo-relative, prefixed with the repo role, e.g.
`server:` or `client:`). Quote 3-15 line snippets verbatim from the repo and
explain them. Every snippet must be copied from the actual file, not
reconstructed from memory.>

## Why it matters / where it bites
<1-3 paragraphs: the operational or correctness consequence — what breaks,
what races, what an oncall would see.>

## Go look for yourself (optional, 2 min)
<One concrete grep/read suggestion, e.g. "grep for X in dir Y and find who
calls it".>
```

## day-NN/quiz.md

3-5 questions. Mix of: one recall, one or two comprehension ("what happens if…"), one code-reading (paste a short real snippet, ask what it does or what input reaches it). In the interactive flow the agent asks these aloud; the file also carries `**Your answer:**` markers so it works as a standalone worksheet.

```markdown
# Day NN quiz

**Q1.** <question>

**Your answer:**

**Q2.** ...
```

## day-NN/.answer-key.md

Hidden answer key (dotfile so it does not spoil a directory listing). One paragraph per question: the expected answer plus what partial credit looks like. Written at generation time, used at grading time. Never shown to the user before grading.

## exercises/day-NN/ (Go package)

A simplified, self-contained re-implementation of today's concept in the standalone module at `<course_dir>/exercises/` (`module cadencetutor`, standard library only, no dependencies).

- `exercise.go` — a stub with `// TODO(you):` markers; the intended solution is 5-10 lines.
- `exercise_test.go` — a complete table test that fails against the stub (red) and passes against a correct solution. Must compile as delivered.
- `README.md` — 3-6 lines: what to implement, which real server or client code it mirrors (file reference), and the run command (`cd <course_dir>/exercises && go test ./day-NN/...`).
- `.solution.go.txt` — the reference solution (plain text so it does not compile into the package), used at grading time to comment on the user's approach versus the reference.

Package name: `dayNN` (for example `day07`). The stub must compile — return zero values, leave no syntax holes — so red means assertion failures, not build failures.

## day-NN/feedback.md (written at grading)

```markdown
# Day NN feedback

## Quiz: <score, e.g. 4/5>
<Per-question: verdict plus a one-sentence correction where wrong, citing the
lesson or a file:line.>

## Exercise: PASS | FAIL | NOT ATTEMPTED
<go test output summary; 2-4 sentences comparing the user's implementation
with .solution.go.txt — what was good, what the real code does differently.>

## Carry-forward
<One sentence on what tomorrow builds on and what to re-read if shaky.>
```

## Validation checklist (supervisor, before delivering a day)

1. Every `file.go:NNN` reference in `lesson.md`: grep the quoted symbol or snippet in that file and confirm the line number is within 15 lines. Fix drift in place; if a reference is fabricated, reject the draft.
2. `cd <course_dir>/exercises && go vet ./day-NN/... && go test ./day-NN/...` — must compile and fail (red). Then verify `.solution.go.txt` makes it pass: swap it in, run `go test -count=1`, swap back. Use `-count=1` because a drafter's own test runs may have populated the build cache.
3. `quiz.md` has 3-5 questions and `.answer-key.md` covers all of them.
4. `lesson.md` is 700-1600 words (about a 10-minute read with snippets).
