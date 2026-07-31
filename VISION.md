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
- **One page in the repository is the canonical artifact.** Not because people
  read it top to bottom — they don't, and they don't write it by hand either —
  but because it sits next to the code it describes, diffs legibly in a pull
  request, and an agent reads it with nothing in between. Digests, public
  projections, and interop formats are generated renders.
- **Adoption must be cheap and safe.** A vendorable stdlib tool, progressive
  conformance, explicit internal/public projection, and agent entry points let
  real data projects adopt Ergo without a platform migration.
- **Capture happens at the moment of learning.** Every prior documentation
  tradition failed because writing it down was a separate act, done later, by
  someone who had stopped being confused. An agent working alongside you is
  present at that moment and holds what the record needs — so the skill, not
  the format, is what people adopt.

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
  into an agent's working context, and carry the procedures — consuming a page,
  registering an issue, reading a page out of an existing implementation.
- `scan` plus the reading procedure open a dataset that has no documentation
  anywhere, which is nearly all of them.
- njschooldata is the first production proving ground; served public bundles
  test the decentralized documentation path.
