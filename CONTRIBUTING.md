# Contributing

Thanks for working on Cadence AI Skills. This file describes the contribution workflow. The style, terminology, and content rules that apply once you start writing live in [`AGENTS.md`](./AGENTS.md) — read that first.

## What we're looking for

In priority order:

1. **Accuracy fixes.** Any factual error in a knowledge file — an API name that drifted, a default value that's wrong, a behavior described from memory rather than source — is high-value to fix.
2. **Filling roadmap gaps.** New knowledge files inside an existing skill (for example, a new file under `skills/cadence-developer/knowledge/go/`) are welcome.
3. **New skills.** New top-level skills (for example, `cadence-operator`) need a brief design discussion in an issue before code; the per-skill structure is the same.
4. **Repo plumbing.** Updates to `README.md`, `AGENTS.md`, this file, or `LICENSE`.

Speculative scaffolding (CI we haven't decided to run, tooling for features that don't exist, content describing roadmap items as if they shipped) is explicitly out of scope. See the "Things not to do" section of [`AGENTS.md`](./AGENTS.md).

## Local setup

There is no build step. Clone the repo and edit Markdown:

```bash
git clone https://github.com/<your-org>/ai-skills.git
cd ai-skills
```

The repo has no dependencies and no generated content. If you want to verify a claim against an upstream Cadence repo, clone the relevant project somewhere alongside this one so you can grep:

```bash
git clone https://github.com/cadence-workflow/cadence
git clone https://github.com/cadence-workflow/cadence-go-client
git clone https://github.com/cadence-workflow/Cadence-Docs
```

## Workflow

1. **Open an issue first** for any of: a new skill, a structural change to an existing skill's `knowledge/` layout, removal of an existing file, or anything that touches more than a handful of files. Small accuracy fixes don't need an issue — go straight to a PR.
2. **Branch off `main`.** One topic per branch.
3. **Make the change.** Keep edits tight; the smaller the diff, the faster the review.
4. **Verify against upstream.** Cite the file path (and line if helpful) in the commit message or PR body for any new factual claim. The [Sources of truth](./AGENTS.md#sources-of-truth) section of `AGENTS.md` defines the canonical ordering.
5. **Commit.** [Conventional Commits](https://www.conventionalcommits.org/) prefixes, one logical change per commit, signed with `-s`:

    ```bash
    git commit -s -m "docs(cadence-developer): fix activity timeout type names"
    ```

6. **Open a PR.** Use the same Conventional Commits style in the title. The body should explain *why* the change makes the skill more correct or useful, and link the upstream source backing any new factual claim. One PR per logical change; stack PRs rather than batching unrelated edits.

## What reviewers check

Reviewers will be opinionated about:

- **Cadence terminology.** No `namespace`, `task queue`, or vocabulary lifted from adjacent workflow-engine projects. See [`AGENTS.md`](./AGENTS.md#cadence-terminology-non-negotiable).
- **API accuracy.** Every named function, struct field, constant, or CLI flag must exist in the upstream source you cited. Reviewers will spot-check.
- **Originality.** Wording, examples, and ordering must be ours. Pull facts from the upstream Cadence sources and write them in your own voice.
- **Cross-references.** If you add or rename a knowledge file, update every other file that points to it, plus the skill's `SKILL.md` knowledge map.
- **Style.** US English, Oxford comma, sentence-case headings, no marketing fluff. See [`AGENTS.md`](./AGENTS.md#writing-style).

If a reviewer's comment isn't obviously actionable, push back. We'd rather discuss than guess.

## Versioning a skill

Each skill's `SKILL.md` carries a semver `version` field. The scheme is:

| Range | Meaning |
| --- | --- |
| `0.1.x` – `0.4.x` | Early development. One band per SDK coming online (Go, Java, Python, …). |
| `0.5.x` – `0.9.x` | Validation phase. Real-world usage by coding agents, fixes from feedback, gap-filling. |
| `1.0.0` | Proven in production after sustained use. |

When to bump:

- **Patch** (`0.2.0` → `0.2.1`): adding a knowledge file, fixing accuracy bugs, rewording.
- **Minor** (`0.2.x` → `0.3.0`): a milestone event such as a new SDK's first knowledge file landing or a substantial restructure of the knowledge map.
- **Major** (`0.x.y` → `1.0.0`): reserved for the production-validated transition. Don't bump this without explicit maintainer sign-off.

Update the `version` field in the same commit as the change it tracks. The version bump appears in the diff alongside the substantive change.

## Reporting an issue

A good bug report includes:

- The skill, the knowledge file, and the section (heading or line range).
- The claim you think is wrong, verbatim.
- The upstream source (file path and ideally a permalink) that contradicts it.
- Optionally, a proposed correction.

If you're a coding agent filing the issue, say so — it helps maintainers calibrate the review.

## License

By contributing you agree that your contribution is licensed under [Apache 2.0](./LICENSE) on the same terms as the rest of the repo. Don't submit content you don't have the right to license under those terms.
