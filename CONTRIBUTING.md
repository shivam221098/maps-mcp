# Contributing to maps-mcp

## How we work (Scrum, epics first)

- **Discussions** are for ideas, design questions and polls. Anything labelled `needs-discussion` must be settled there before implementation.
- **Epics** (`epic`) group related stories. Each epic body has a task list linking its stories.
- **Stories** (`story`) deliver user-visible value. **Spikes** (`spike`) are time-boxed research with a written outcome. **Bugs**, **chores** and **docs** use their own labels.
- **Sprints** are not pre-assigned. Sprint planning picks issues from the board.
- One issue, one branch, one pull request. The PR description says `Closes #<n>`.

## Labels

| Group | Labels |
|---|---|
| Type | `epic`, `story`, `spike`, `bug`, `chore`, `docs` |
| Area | `area:core`, `area:google`, `area:osm`, `area:routing-engines`, `area:geocoders`, `area:tiles`, `area:security`, `area:release` |
| Priority | `P0` (must), `P1` (should), `P2` (could / icebox) |
| Estimate | `points:1`, `points:2`, `points:3`, `points:5`, `points:8` (an 8 should be split) |
| Workflow | `needs-discussion`, `ready` |

## Definition of Ready

An issue is `ready` when it has:

- a clear user story or goal,
- acceptance criteria,
- a points estimate,
- no open `needs-discussion` question,
- links to relevant provider docs and usage policies.

## Definition of Done

- Acceptance criteria are met.
- Tests pass, and `ruff` and `mypy` are clean.
- Docs are updated (README, tool descriptions, examples).
- The provider's usage policy and terms of service are respected (rate limits, caching, attribution, field masks).
- No secrets are committed or logged.

## Ground rules

- API keys come from environment variables or config only.
- Respect provider policies, especially the Nominatim public instance (max 1 request per second, identifying User-Agent, cache results).
- Keep the exposed tool count small. Prefer a few well-described tools over many narrow ones.
