# Vision — ergo

**North star:** Nobody working with a dataset—human or agent—has to rediscover
a known trap, silently repeat a bad workaround, or misuse a number because its
caveat lived only in prose or in one person's memory.

**North-star metric:** live issue coverage — the share of known consequential
dataset issues that are stably identified, machine-scoped, typed, current,
linked to the handling code, and backed by a dated validation record where the
claim can be checked.

## Strategy bets

- **The issue is the unit.** A stable ID, effect, type, status, scope, misuse,
  and handling link make each caveat findable and actionable.
- **One human page is the canonical artifact.** Markdown narrative and embedded
  TOML serve people and machines; digests, public projections, and interop
  formats are generated renders.
- **Adoption must be cheap and safe.** A vendorable stdlib tool, progressive
  conformance, explicit internal/public projection, and agent entry points let
  real data projects adopt Ergo without a platform migration.

## Non-goals

- A data catalog service, data warehouse, or hosted validation platform.
- Replacing source ledgers, reporter notebooks, schemas, or ingestion tests.
- Making every caveat executable before the prose and scope are useful.
- Treating metadata completeness as evidence that a dataset is safe to use.

## Engine map

- The data-page specification defines manifests, issues, validations, changes,
  and the canonical/derived boundary.
- `tools/ergo.py` scaffolds, checks, exports, digests, and publishes without
  external dependencies.
- Greppable code anchors close the round trip between documented caveat and
  implemented workaround.
- Skills and AGENTS/CLAUDE pointers put the right subset of the issue registry
  into an agent's working context.
- njschooldata is the first production proving ground; served public bundles
  test the decentralized documentation path.
