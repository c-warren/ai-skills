# AGENTS.md

Operating rules for AI agents (and the humans pairing with them) editing files in this repository.

> Audience: anyone authoring or updating skill content under `skills/`. These rules govern *how we write the skills* — they are not the runtime instructions an end-user's agent should follow when a skill is loaded.

## Orientation

This repo is a library of Cadence-focused Agent Skills. Every change should make a skill more correct, more concise, or more useful. Avoid adding speculative scaffolding (CI we haven't decided to run, installers for tools that don't exist, documentation for features we haven't shipped).

Before editing, read:

1. [`README.md`](./README.md) — repo vision, layout, available skills.
2. The `SKILL.md` of any skill you are changing.
3. Relevant files under `knowledge/shared/` and the language directory you touch.

## Cadence terminology (non-negotiable)

Use Cadence's vocabulary in prose. General workflow-engine literature on the internet uses synonyms from adjacent projects, and LLM completions drift toward those synonyms — actively correct for that drift.

Canonical terms (parenthetical items are common drifts to avoid):

- **domain** (not namespace)
- **task list** — `tasklist` in code identifiers — (not task queue)
- **`cadence` CLI**
- **Cadence Cluster**, **Cadence Server**
- **Cadence Web**

If you reach for vocabulary, branding, or examples that don't appear in the upstream Cadence sources listed below, stop and re-derive from those sources. Do not reference other vendors' managed orchestration offerings inside skill content. If a concept genuinely has no Cadence equivalent, leave it out.

The Cadence SDKs themselves sometimes carry both legacy and modern API names — verify against the relevant SDK source before writing API names into a skill. When the SDK exposes both, for example `WorkflowTask*` next to older `Decision*` helpers in `cadence-go-client`, prefer the modern name in new examples, but explain the legacy term once so readers searching old code or docs can connect the dots.

## Sources of truth

Skill claims must be grounded. When prior LLM knowledge disagrees with project material, prefer in this order:

1. [`cadence-workflow/Cadence-Docs`](https://github.com/cadence-workflow/Cadence-Docs) — the canonical narrative at <https://cadenceworkflow.io>.
2. [`cadence-workflow/cadence`](https://github.com/cadence-workflow/cadence) — server source, the ultimate authority on protocol behavior.
3. [`cadence-workflow/cadence-go-client`](https://github.com/cadence-workflow/cadence-go-client), [`cadence-java-client`](https://github.com/cadence-workflow/cadence-java-client), [`cadence-python-client`](https://github.com/cadence-workflow/cadence-python-client) — language SDK source and tests.
4. General LLM knowledge — last resort, and only after verification.

When a non-obvious claim lands in a knowledge file, cite the upstream URL inline.

## Originality

This repository is original work. Do not copy text verbatim from any other skill project, blog post, or documentation site. Structural similarities are inevitable because the underlying problems are the same, but wording, examples, ordering, and emphasis must be ours. If you find yourself reaching for an outside paragraph, rewrite it from the upstream Cadence source instead.

## File conventions

### `SKILL.md`

Every `SKILL.md` begins with YAML frontmatter:

```yaml
---
name: <skill-name>
description: <one-paragraph description of when an agent should load this skill>
version: <semver>
---
```

- The H1 under the frontmatter matches the `name` field.
- Top-level sections use H2 (`##`); avoid going deeper than H4.
- Reference knowledge files with relative paths (`knowledge/shared/<topic>.md`).
- Keep `SKILL.md` itself focused on orientation and pointers — the depth lives in `knowledge/`.

### `knowledge/`

- `shared/` — language-agnostic Cadence concepts.
- `<sdk-lang>/` — language-specific guidance (`go/`, `java/`, `python/` for now).
- A `shared/` file may point readers to language-specific guidance using the pattern `knowledge/<sdk-lang>/<topic>.md`.
- One topic per file. Prefer multiple short files over one omnibus file.

### Code samples

- Samples must compile or run against a currently supported release of the relevant SDK.
- Prefer minimal, focused examples over kitchen-sink demos.
- Mirror the parameter names, struct names, and import paths used in the SDK source so readers can grep upstream.

## Writing style

- US English. Oxford comma. Sentence case for headings.
- Plain, declarative prose. No marketing copy.
- Avoid filler: "simply", "just", "easy", "obviously", "of course".
- Tables for comparisons; numbered lists for ordered steps; bullets for unordered sets.
- Hyperlinks use descriptive text, not bare URLs in prose.

## Commits and PRs

- Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes (`docs:`, `feat:`, `fix:`, `chore:`, `refactor:` …).
- Sign every commit with `-s`.
- One logical change per commit. A new knowledge file is its own commit; structural moves are separate from content changes.
- PR titles match the commit convention. PR descriptions explain *why* the change makes the skill more correct or useful, and link the upstream source backing any new factual claim.

## Things not to do

- Don't add files for tooling that doesn't exist yet (installer scripts, CI workflows we haven't agreed on, packaging metadata for a registry we don't publish to).
- Don't introduce dependencies. This repo is markdown plus the rare shell helper.
- Don't reorganize the `skills/<name>/knowledge/{shared,<lang>}/` layout without an issue or prior discussion.
- Don't promise features in skill content. Describe what works today; mention the roadmap only in `README.md`.
