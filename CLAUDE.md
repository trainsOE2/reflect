# CLAUDE.md

Guidance for Claude Code working in this repository.

## Source of truth

- **What to build:** `docs/REQUIREMENTS.md`. Read it in full before implementing anything. Do not restate its contracts here or anywhere else; point to it.
- **What exists:** the filesystem and the test suite. Docs describe intended design, not current state. Before claiming anything is implemented, verify it in code and run the tests.
- **Open decisions:** `docs/REQUIREMENTS.md` §8 lists decisions Mirik has not made yet. Do not silently resolve them. Surface them when the work reaches them.

## Invariants

Do not violate these without asking first.

- **The model emits a judgment; code decides the action.** Never prompt the model for an action (`allow`/`block`) or a boolean. Decision mapping lives in application code.
- **Money is integer minor units.** Never a float, anywhere.
- **Fail closed.** Classifier errors, malformed model output, and suspected injection never produce `allow`.
- **Listing content is untrusted.** XML-escape it, wrap it in tags, put the instruction after it. See REQUIREMENTS §7.6.
- **Only the provider adapter imports a vendor SDK.** Classifiers depend on the provider protocol, not on `anthropic`.
- **Tests run offline.** The test suite uses a stub provider and never needs a network connection or an API key.
- **Secrets stay out of git.** API keys come from `.env`, which must be gitignored. Never hard-code or log a key.

## How to work with Mirik

- **She is learning this stack while building it.** Before writing code for a concept new to the repo, name the specific resource to read first and ask whether she has read it. Don't get ahead of her. Current mapping:
  - Prompt construction and injection defense → Anthropic prompt engineering tutorial, Ch 4 "Separating Data from Instructions"
  - Structured output via tool use → tutorial Ch 5 "Formatting Output", then the Anthropic tool use docs
  - Rationale-before-label ordering → tutorial Ch 6 "Precognition"
  - Few-shot examples (first lever when eval accuracy is weak) → tutorial Ch 7 "Using Examples"
  - Redis Streams, consumer groups (`XADD`/`XREADGROUP`) → Redis Streams intro in the official docs
- **Small diffs, one concept at a time.** Each change comes with a short "why" she could repeat in an interview.
- **Prompt a commit every time tests go green.** Uncommitted work has been lost on this project before.
- **Correct terminology mistakes directly.**
- **Push back on scope creep.** If a request goes beyond the current stage in REQUIREMENTS §7, say so before doing it.
- She comes from C#/.NET. Analogies to that ecosystem are useful when introducing Python or FastAPI patterns.

## Commands

- Redis (not needed until Stage 2): `docker compose up -d redis`
- Python is pinned to 3.11.3 via `.python-version`.
- Dependency install, test, and run commands: not established yet. Add them here when the first dependency manifest and test exist.

## Intended layout

Planned, not built. Check the filesystem for what actually exists.

```
app/
  main.py                 FastAPI app, routes, exception handlers
  schemas.py              Pydantic request/response models
  decision.py             Judgment → action mapping (REQUIREMENTS FR-12)
  policies/               Tenant policy YAML files
  providers/
    base.py               Provider protocol and normalized errors
    anthropic_provider.py The only module importing the vendor SDK
  classifiers/
    text_policy.py        Prompt construction, tool schema, output validation
evals/                    Labeled cases and the eval runner
tests/                    Offline tests with a stub provider
```

## Notes

- `reflect-context.md` and `learning-log.md` are gitignored personal notes. They stay untracked.
- Portfolio scope: correctness and architectural clarity over feature completeness.