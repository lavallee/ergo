# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues on **`lavallee/ergo-private`** — *not* on
`lavallee/ergo`, which is this clone's origin. Use the `gh` CLI for all operations,
and pass `--repo lavallee/ergo-private` to every one of them.

> **Why a different repo.** ergo's work spans public repositories (`lavallee/ergo`,
> `lavallee/ergo-directory`) and private corpora (aquifer, njschooldata). Planning
> that references private data should not be charted in a public tracker, so the
> planning surface is the private sibling while the artifacts stay where they belong.
>
> **This means `gh`'s repo inference is wrong here.** Left to itself, `gh` targets the
> origin remote and would publish to `lavallee/ergo`. Never drop the `--repo` flag.

## Conventions

- **Create an issue**: `gh issue create --repo lavallee/ergo-private --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view --repo lavallee/ergo-private <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --repo lavallee/ergo-private --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment --repo lavallee/ergo-private <number> --body "..."`
- **Apply / remove labels**: `gh issue edit --repo lavallee/ergo-private <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close --repo lavallee/ergo-private <number> --comment "..."`

Do **not** infer the repo from `git remote -v`. This tracker is deliberately not the
origin remote; always state `--repo lavallee/ergo-private` explicitly.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues, using the `gh pr` equivalents:

- **Read a PR**: `gh pr view --repo lavallee/ergo-private <number> --comments` and `gh pr diff --repo lavallee/ergo-private <number>` for the diff.
- **List external PRs for triage**: `gh pr list --repo lavallee/ergo-private --state open --json number,title,body,labels,author,authorAssociation,comments` then keep only `authorAssociation` of `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE` (drop `OWNER`/`MEMBER`/`COLLABORATOR`).
- **Comment / label / close**: `gh pr comment --repo lavallee/ergo-private`, `gh pr edit --repo lavallee/ergo-private --add-label`/`--remove-label`, `gh pr close --repo lavallee/ergo-private`.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either — resolve with `gh pr view --repo lavallee/ergo-private 42` and fall back to `gh issue view --repo lavallee/ergo-private 42`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view --repo lavallee/ergo-private <number> --comments`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `gh issue create --repo lavallee/ergo-private --label wayfinder:map`.
- **Child ticket**: an issue linked to the map as a GitHub sub-issue (`gh api` on the sub-issues endpoint). Where sub-issues aren't enabled, add the child to a task list in the map body and put `Part of #<map>` at the top of the child body. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: GitHub's **native issue dependencies** — the canonical, UI-visible representation. Add an edge with `gh api --method POST repos/lavallee/ergo-private/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id** (`gh api repos/lavallee/ergo-private/issues/<n> --jq .id`, _not_ the `#number` or `node_id`). GitHub reports `issue_dependencies_summary.blocked_by` (open blockers only — the live gate). Where dependencies aren't available, fall back to a `Blocked by: #<n>, #<n>` line at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open children (`gh issue list --repo lavallee/ergo-private --state open`, scoped to the map's sub-issues / task list), drop any with an open blocker (`issue_dependencies_summary.blocked_by > 0`, or an open issue in the `Blocked by` line) or an assignee; first in map order wins.
- **Claim**: `gh issue edit --repo lavallee/ergo-private <n> --add-assignee @me` — the session's first write.
- **Resolve**: `gh issue comment --repo lavallee/ergo-private <n> --body "<answer>"`, then `gh issue close --repo lavallee/ergo-private <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far.


## Labels are not yet created

`lavallee/ergo-private` currently carries only GitHub's default label set. Neither the triage
vocabulary (`docs/agents/triage-labels.md`) nor wayfinder's `wayfinder:map` and
`wayfinder:<type>` labels exist there yet. `gh issue create --label X` fails on an
unknown label, so create each one at first use:

```
gh label create wayfinder:map --repo lavallee/ergo-private --description "A wayfinder map" --color 0e8a16
```

## Native features are unverified

The tracker is empty, so sub-issue and issue-dependency support could not be
confirmed by probing. `gh` 2.96.0 supports both. Verify at first create rather than
assume; the fallbacks above (a task list in the map body plus `Part of #<map>`, and a
`Blocked by:` line) are what to use if either turns out to be unavailable.
