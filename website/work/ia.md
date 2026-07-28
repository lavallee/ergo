# Information architecture — the ergo site

Private working document. Not deployed.

## 1. The customers, and the job each one arrives with

Three reader populations. Only the first sets the IA; the other two are served
without being allowed to dilute the front door.

| Reader | Arrives from | The job in their words | What convinces them | What loses them |
|---|---|---|---|---|
| **Pipeline maintainer** (primary) | The repo, a data-journalism list, a colleague's page | "I keep rediscovering the same traps in this agency's files. Is this where the list goes?" | Seeing the enforcement, and seeing how small the commitment is. That it is one file and markdown. | Ceremony with no teeth. A schema standard in disguise. Anything implying a service. |
| **Agent author** (secondary) | Agent-tooling chatter, AGENTS.md/skills discussion | "What actually lands in the model's context, and what does it cost me to load?" | The three disclosure tiers, the `core` flag, the scope filter, the two-line memory pointer. | Being shown only a CLI, or a format that assumes a human reads everything. |
| **Format evaluator** (tertiary) | Metadata-standards work, DCAT/Croissant circles | "Is this a credible new thing, or a fork of documentation practice with opinions?" | The survey, the honest interop table, the stated non-goals. | Overclaiming standardization. Vagueness about what catalogs supply and what ergo adds. |

**Where the three converge:** all three are deciding about an *artifact at
rest* — a markdown file in somebody's repository — not about a product
experience. That is the centre of gravity, and it is why the load-bearing
interactive shows a file being written and a validator refusing, not an app
being used.

**Where they diverge:** the maintainer wants to know what it costs; the agent
author wants to know what it loads; the evaluator wants to know exactly what is
being claimed against existing standards. Three questions, three routes, one
spine.

## 2. The decision stack, marked

Bottom-up, before touching a surface:

| Layer | State | Note |
|---|---|---|
| Observed user behaviour and constraints | **weak** | Two adopting projects, one of them the author's. No interviews, no analytics, no support log. This is the honest floor and it constrains everything above it. |
| Domain facts and rules | **strong** | SPEC.md v0.4 is current and mechanically checkable against `tools/ergo.py`; the survey behind it is written down. |
| User need and authority | **partial** | The need is inferred from the author's own multi-project practice and from the survey's finding that no format makes an issue scoped, typed, versioned and code-linked at once. Stated as a bet, not a finding. |
| Product strategy and scope | **strong** | VISION.md names the north star, three strategy bets, four non-goals. |
| Concept model and vocabulary | **strong** | Dataset / issue / practice / validation / change, plus scope, effect, anchor. Stable, and enforced by the validator. |
| Interaction flow | **partial** | The authoring flow is proven by tests and by two adoptions; the *site's* flow is new work. |
| Rendered surface | **absent** | No site existed before this. |

**Lowest weak layer is the bottom one, and this project cannot repair it** — no
amount of design produces adoption evidence. The correct response is not to
fake it but to argue from the format itself and label the absence explicitly.
That decision propagates into every route: the proof on this site is
*mechanical* (real commands, real refusals, real conformance) because the
*empirical* proof does not exist yet.

## 3. Routes

Five routes, flat files so the site renders from `file://` (an artoo
requirement, and the reason there are no directory-index URLs).

### `index.html` — the argument

- **Mode:** marketing, with editorial passages for the argument body.
- **Task anatomy:** proof-led product argument. Position → the problem in the
  reader's own terms → what is enforced → what a page is at rest → the issue /
  practice distinction → adjacent comparison → the honest limits → coordinates.
- **Structural fingerprint:** *the widening spiral.* One claim stated flat,
  then re-entered at increasing resolution — headline, then four enforcement
  rules each backed by real validator output, then the block itself. A reader
  can leave at any depth with a correct, if coarser, understanding.
- **Deliberately absent:** feature cards, logo strip, testimonials, metrics the
  project does not have, animated terminal.

### `walkthrough.html` — how a page comes together

- **Mode:** public-data, in an editorial wrapper.
- **Task anatomy:** a linear narrative the reader scrolls, not a stepper. The
  unit of meaning is an *exchange*, and exchanges have a natural order.
- **Structural fingerprint:** *the conversation, with the machine's answer
  attached.* Human turn right, agent turn left, the command underneath the
  reply, and a closed `<details>` holding the full record — output, entry,
  tree, spec link. The reader learns one layout and then only the content
  changes.
- **Why a conversation and not a command list:** nobody adopting this types
  these commands in sequence. They ask an agent for something and the
  documentation happens along the way; showing it as a chat is the honest
  depiction, and it puts the refusals where they belong — between what the
  human asked for and what the format allowed.
- **Deliberately absent:** autoplay, typing animation, fake latency, and any
  edited output.

### `format.html` — the format, visually

- **Mode:** public-data.
- **Task anatomy:** a map with drill-down. A navigation surface into SPEC.md,
  not a diagram to admire.
- **Structural fingerprint:** *the page, opened.* The block list as the
  organizing spine (because that is how a reader meets a page on disk), each
  block expanding into its required and optional keys and a real example from
  the walkthrough's page.
- **Second and third views on the same page:** the vocabularies (closed vs
  recommended, which is the distinction that makes filtering worth doing) and
  the issue lifecycle, because the single most important thing to understand is
  that registering, scoping, mitigating, anchoring and validating are
  *separate acts* and a static list cannot show sequence.
- **Deliberately absent:** a node graph. Five block types have no topology
  worth drawing.

### `page.html` — a real page, browsable

- **Mode:** public-data.
- **Task anatomy:** overview-to-detail over one real artifact.
- **Structural fingerprint:** *the registry, filtered.* Manifest facts, the
  pitfall pulled out, then one card per entry with its scope, misuse, and the
  prose that sits under it in the source file. Filters are the effect
  vocabulary itself, so using the page teaches the vocabulary.
- **Why the repository's own example and not a synthetic one:** the walkthrough
  is already synthetic, and a reader who has watched a fictional page being
  built needs to see the format carrying real NJ DOE material before believing
  it. Labelled as a render of `examples/spr.md` throughout.

### `start.html` — first page in ten minutes

- **Mode:** operator.
- **Task anatomy:** a linear task with copyable exact state. Vendor → scaffold
  → manifest → first issue → anchor → validate → digest → agent pointer → CI.
- **Structural fingerprint:** *the numbered path with a visible finish line.*
- **Deliberately absent:** decorative anything, and any invented command
  output. The one record on the page is generated; everything else is a command
  you can paste.

## 4. Navigation model

A persistent six-item nav: `ergo` (home), Walkthrough, Format, Example page,
Start, GitHub. Flat, no dropdowns — five routes do not need hierarchy, and
inventing some would misrepresent the site's size.

Ordering is the reader's likely path, not alphabetical: understand → see it
happen → check the details → see it carrying real data → do it.

Cross-route links are one-directional and specific:

- Home → walkthrough at the enforcement claim ("watch this happen").
- Home → format at the moment the vocabulary is introduced.
- Walkthrough → spec section per step, so a step's concept has a definition.
- Format → SPEC.md anchors, always; the visual never becomes the source of
  truth.
- Everything → start, once.

## 5. Content inventory and its provenance

| Surface content | Source | Fails how |
|---|---|---|
| Format version, tool version, revision | `tools/ergo.py` banner, `git rev-parse` at build | Build error |
| Spec status, section titles and anchors | Parsed from `SPEC.md` at build | Build error |
| Passing checks | `python3 tests/run.py` at build, counted from its output | Build error |
| Command list and usage lines | `ergo.py --help` and each subcommand's `--help` | Build error on drift |
| Vocabularies and required keys | Imported from the validator's constants, cross-checked against SPEC.md and against the demo page's real output | Build error on drift |
| Walkthrough frames | Real validator runs in a temp project at build | Build error, including if a refusal stops refusing |
| Block examples | Sliced out of the demo page the walkthrough built | Build error |
| Example page fields and prose | `ergo.py export examples/spr.md` plus prose sliced from the same file | Build error |
| Everything else (prose) | Written, and answerable to the design brief | Review |

The rule: if a fact can be derived, it is derived. Prose is for argument, not
for facts that will drift.

## 6. What this site does not have, on purpose

- No blog, no news, no changelog page — CHANGELOG.md is the record and the
  footer links to it rather than mirroring it.
- No docs tree. `docs/survey.md` and SPEC.md are the reference; duplicating
  them here would create two sources of truth, which is the exact failure
  ergo's own "canonical page, derived renders" principle warns about.
- No search. Five routes.
- No newsletter, no waitlist, no analytics, no third-party anything.
- No provenance panel. flip's site has one because it keeps a flip notebook;
  ergo's site would need a notebook it does not have, and an empty panel is
  worse than no panel.
