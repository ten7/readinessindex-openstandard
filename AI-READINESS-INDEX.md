# The AI Readiness Index

**Version 12.0 — specification**
Effective 2026-10-18.
Repository: [ten7/readinessindex-openstandard](https://github.com/ten7/readinessindex-openstandard)

**License:** This document and the tests it defines are published under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Copy it, adapt
it, build your own scanner from it — for any purpose, free, forever — as long
as you credit TEN7 as the creator of the AI Readiness Index and license
what you build the same way. Scanners that compute a score from this
document are separate software and are not part of the standard. Full terms at
[openstandard.readinessindex.io/about](https://openstandard.readinessindex.io/about/#license).


## What this is

This document defines what a website has to do to score 100 on the AI Readiness Index. It is written for two readers at once: the engineer building a scanner, and the consultant explaining a score to a client.

Every test has an ID, a plain-English question, a detection method, and a scoring rubric. Every test also carries an evidence label and graded sources that say whether anything is documented using what it checks. If a test is not described here, the scanner should not score it.

We built this because "is your site ready for AI" is currently an unanswerable question. Vendors assert things. Nobody measures. Our answer is a number you can reproduce, defend line by line, and re-run in six months to show what changed.

The Index measures one thing: **can machines find, read, trust, and use this website?** It does not measure design quality, marketing effectiveness, or whether the content is any good. A beautiful site can score 12. A plain one can score 94.

Four scored categories answer that question in order. **Reach:** can they get to it? **Read:** can they find your pages and read the words? **Understand:** do they know what it is? **Act:** can an agent do something? Only what has documented use is scored. Everything else is measured and shown in three groups beside the score (Posture, Extras and Measurement) and never moves it.

## How to read a score

A result has three parts, and all three matter.

**The score (0–100).** A single weighted number across four categories: Reach, Read, Understand and Act.

**The gate status.** Two tests are gates. If a site blocks the search crawlers of AI assistants in `robots.txt` (RCH-1) or turns them away at the CDN or the firewall (RCH-2), `gated` is `true`: a separate fact reported beside the score, not a ceiling on it. The score still says how well the site is built; the gate says whether any of it is reachable today. A perfectly marked-up site that returns 403 to `Claude-SearchBot` is not badly built, it is invisible, and those are different problems with different fixes. Blending them into one capped number made a well-built gated site indistinguishable from a badly-built one; see the changelog for 4.0. Blocking a training crawler never gates: that is a rights choice, and PST-1 shows it without scoring it.

**The automated coverage.** The percentage of applicable weight the scanner verified on its own. Some tests, such as whether the date a page shows is the date its markup says, can be fooled by a heuristic, and some facts cannot be seen from outside at all. Those are scored from attestation and flagged. A score of 82 with 91% automated coverage is a much stronger claim than 82 with 64%.

Report all three together. A bare number invites arguments we don't need to have.

Beside the score, every report shows three unscored groups: **Posture** (choices that are yours to make, which never lower readiness), **Extras** (good practice with no documented reader) and **Measurement** (how you track AI traffic). A site that does them is credited in words and is never marked down for leaving them out.

### Grade bands

| Score | Grade | What it means |
|---|---|---|
| 90–100 | Exemplary | Machine-legible by design. Remaining work is optional or emerging. |
| 75–89 | Strong | Solid fundamentals with specific, addressable gaps. |
| 60–74 | Adequate | Findable and readable, but leaving significant value unclaimed. |
| 40–59 | Weak | Partially legible. Real content is not reaching answer engines. |
| 0–39 | Not ready | Structural problems. Start with retrievability before anything else. |
| Any | **Gated** | A separate fact, not a grade. RCH-1 or RCH-2 failed: the search crawlers of AI assistants cannot reach the site, so none of the score above is reaching one today. Before 4.0 this capped the total at 40, which blended two facts into a number comparable to neither. |

`grade` is always the band the real, uncapped `total` falls in — a gate failure never changes it. `gated` is the separate boolean the report checks to decide whether to lead with the access problem, so it can say "Strong at 81, and gated — none of that is reaching an assistant today" rather than either hiding the score behind the word Gated or letting it stand alone with no warning attached.

## The scoring model

### Bands

Every check scores on a 0–4 band. The check's contribution is `weight × (band ÷ 4)`.

Unless a test says otherwise, use the **default coverage rubric** against the sampled page set:

| Band | Condition |
|---|---|
| 4 | Present and correct on ≥95% of applicable sampled pages |
| 3 | Present and correct on 75–94% |
| 2 | Present on 40–74%, or present everywhere but with correctness errors |
| 1 | Present on 1–39% |
| 0 | Absent, or present but broken everywhere |

Coverage percentages are weighted, not raw page counts. Each money page (see Sampling, step 4) counts as **2** in both the numerator and the denominator; every other sampled page counts as 1. Ten money pages in a 250-URL sample therefore score as a 260-page sample. A failure on `/apply` costs twice what the same failure on a 2019 press release costs, which is the reason the client names those URLs in the first place.

Tests that are inherently site-wide and binary (a file exists, a header is set) define their own bands in the test entry.

### Points

| # | Category | Points | Tests |
|---|---|---|---|
| 1 | Reach | 25 | 4 |
| 2 | Read | 35 | 19 |
| 3 | Understand | 25 | 11 |
| 4 | Act | 15 | 4 |
| | **Total** | **100** | **38** |

Beside the hundred, and counted separately because they are not part of it: 34 unscored tests in three groups. **Posture** has 6, **Extras** has 20 and **Measurement** has 8. A report shows all 72 tests. The score is made of 38.

Weight follows three things: how badly a failure hurts, how strong the evidence is that it matters, and how many assistants it affects.

- **Reach is 25 and Read is 35, so the two together are 60.** These are the categories where the evidence comes from the companies that run the assistants, and the only failures that make a site invisible. Reach holds the four tests that decide whether an AI system can get to a site at all. Read holds the tests of whether it can find the pages and read the words, which includes the crawl housekeeping (sitemaps, redirects, dead pages, filters, pagination, file rules) that used to sit beside Reach in Index 11.
- **Understand is 25 and Act is 15.** Understand is documented for Google and Bing rather than for AI products, and it is led by dates (UND-6). Act has real but narrow evidence (browser agents read page structure and stop at CAPTCHAs), so it is four tests: ACT-1 and ACT-4, which both rest on the accessibility tree Anthropic documents its browser tool reading, carry five points each, ACT-2 carries three and ACT-3 two. Before marker Y, Reach and Read carried 75 points and Act carried five.
- **Seven tests are labeled Practice and carry one point each** (RED-13 to RED-19). They are sound practice for people, and nothing documents an AI product using them.
- **Rights are not scored.** A site's page settings decide whether a page can be quoted, so RCH-4 is scored in Reach. What a site permits AI to do with its content, and what it licenses, is a choice. PST-1 to PST-5 show it and never score it.
- **Google's AI-control setting is not scored.** A scan cannot see it, and a number should not rest on something a scan cannot check. PST-6 asks the owner to confirm it.

Posture, Extras and Measurement carry none of the 100 points — by design, not omission. Scoring a practice nobody has a documented use for subtracts the same points from every site, which moves nobody relative to anybody. They are still run and still reported.

### Applicability and N/A

Each test declares an applicability rule:

- **`always`** — scored on every site.
- **`conditional`** — scored only if a precondition holds. State the precondition in the check.
- **`vertical`** — scored only for a declared client vertical. Sixteen are published; `other` is one of them and carries no expected type set, so a client who tells us their industry is not on the list is not marked against a standard that does not exist for them.

A conditional test states its precondition in one of two forms, and never in both:

- **A named site fact** — a single named predicate over collected evidence, such as `sample_contains_tables` or `site_has_search`. Predicates are code, not expressions in a config file, so each one is unit-tested and each one names itself in the N/A reason an auditor reads.
- **A dependency on another check** — written as `requires: RED-10 ≥ 2`. A dependency is satisfied when the named check scores **band 2 or higher**. Below band 2 the foundation is broken, and measuring what sits on top of it produces a finding nobody can act on: telling a client their Markdown copy is correctly advertised when the copy itself is broken is noise. A dependency that is itself N/A cascades N/A to everything that depends on it.

Two tests carry a dependency: RED-11 → RED-10 and MSR-4 → MSR-3.

#### Facts the scanner cannot observe

Six tests are conditional on a business fact no crawler can determine: PST-3 (licensable content), EXT-3 (the site runs its own agents), EXT-8 (health, legal and financial content), EXT-9 (research and policy publishing), EXT-10 (original asset production) and MSR-1 (named critical flows). UND-2 needs a declared vertical. UND-9 needs to know whether the site has a paywall, which a crawler can often see and an owner's statement settles.

These come from an engagement profile supplied per client — never from inference. The scanner does not sniff a site for medical keywords and decide it is YMYL. A guess inside a number we ask a client to defend line by line is worse than saying we have not checked.

But not checking is not the same as not scoring, and from 1.0 to 9.x the Index treated them as the same thing.

#### Every test is scored (10.0)

**On any run a person is shown, every scored test comes back with a band.** The denominator is the full 100 points, on every site, every time. The unscored groups report a state and never enter the arithmetic.

Applicability resolution still runs, and still decides exactly what it always decided: whether this test has anything to find on this site. What changed in 10.0 is only what happens next. A verdict that used to end the test's participation in the run now resolves to a band, in one of three ways:

| What resolution found | Band | What the report says |
|---|---|---|
| The site has none of the thing the test is about — a precondition that evaluated false, a vertical the site is not in, a dependency whose parent had nothing to find | **4** | *There is none of this on the site, so there is nothing to fix.* |
| The answer is real but invisible from outside — an undeclared profile fact, a manual test with no attestation, or evidence we read and could not settle | **2**, held | *We cannot see this from outside your site. Confirm it and this scores in full.* |
| The test this one depends on is not passing | **0** | *The test this one builds on is not in place yet.* |

The middle row is a **ceiling**, not an earned band, and uses exactly the mechanism `unattested_ceiling` already used: the band is held at 2, `band_capped_at` and `cap_reason` record why, and `earnable_points` falls accordingly. A held test can never read as a pass, and confirming it can always move the number. Points above a ceiling are also excluded from the backlog: a test sitting at its ceiling has nothing on the site to fix, and a list headed *what to fix* must not open with work nobody can collect.

Every one of these carries its `unscorable_reason` in the result file and an evidence row naming what was looked for, what came back, and what it scored — the same audit trail as any other test. An auditor can still see exactly what we chose not to measure; it is now a fact about a scored row rather than a missing one.

**Why.** A test with no band was invisible to the arithmetic *and* to the reader. A self-serve visitor declares nothing, so more than half the Index left the run — a third of it purely for want of an engagement profile — and the score that came back was a percentage of a denominator that silently changed from site to site. Two sites could not be compared, and a client reading their own report found rows that gave them neither a result nor anything to do. Scoring every test costs the Index nothing it was actually measuring and gives back the property its name claims: a hundred points, all of them accounted for.

**What this is not.** It is not scoring an N/A as zero — penalizing a museum for having no `Physician` markup is the mistake this Index was built to avoid, and the first row above is what prevents it. Nor is it paying a site for our own blind spots: anything we could not see is held at 2, never granted, which is the same dishonesty pointing the other way.

**Two runs are exempt.** A **Reach scan** looks at four tests and reports points out of 25, and says so; scoring the other thirty-four would hand it points for work it never did and move its ceiling from site to site. The **census** exists to report what share of sites do a given thing, so a test it could not judge has to stay out of that tally rather than be counted as a site with nothing to fix. Both run with `score_everything` off, and neither is a report a client is handed.

```
score = (Σ earned_points ÷ Σ applicable_weight) × 100
```

### Resolving external identifiers

UND-10 asks whether a site's `sameAs` links point at real authority records. Classifying a URL as a tier-1 identifier needs no network call; confirming it still resolves does, and those hosts belong to somebody else — ORCID, Wikidata, a registry, a university directory.

Requesting them tells a third party which site is being audited. That is a real disclosure, and it is why resolution is a deliberate choice rather than a default in the reference scanner's CLI. A scan that does not resolve them still grades UND-10 on the links as published, at medium confidence and saying so, because a scored test must be able to earn full marks: the links are classified, not confirmed.

Two rules apply wherever it is turned on:

- **A third party's availability is never a fact about the client's site.** A timeout, a DNS failure or a rate limit against ORCID records that one link as unconfirmed. It must not fail the scan, and it must not score the client down.
- **Say that it happened.** The evidence records which external hosts were contacted, so a client can see what their audit disclosed and to whom.

### Rounding, and the full accounting

**Every points figure shown to a reader is a whole number. Every points figure used in the arithmetic is not.**

A test contributes `weight × band ÷ 4`. No weight in the Index divides by four, so a weight-2 test at band 3 contributes exactly 1.5 points and a weight-5 test at band 2 contributes exactly 2.5. Reports print those as 2 and 3.

This is deliberate. The Index exists to be defended out loud, line by line, in a room with the people who have to do the work. Nobody argues about three quarters of a point, and a column of figures like `2.25` reads as a spreadsheet artifact rather than a judgment somebody made. Whole numbers are the readable choice.

They are also, in aggregate, wrong — and saying so is not optional:

- **A run's printed rows do not sum to its printed score.** On a typical run roughly a third of the rows round up or down. Adding the printed column can land ten points or more away from the printed total.
- **The score is never computed from the rounded rows.** It is computed from the exact contributions, summed at full precision, divided by the total weight, and rounded exactly once, at the end.

Both numbers are correct. They answer different questions, and only one of them is the score.

**Every result therefore carries a full accounting**, reachable from the foot of the report and from the stored result file: every test, its weight, its band, the arithmetic `weight × band ÷ 4` written out, its exact contribution, the figure the report printed instead, and the final division. Nothing on that page is rounded except where it says so. It recomputes the score from weight and band rather than reprinting the stored figure, so a disagreement between the accounting and the report would be visible rather than silent.

An implementer of this specification must do the same. Print whole numbers if you like, but publish the arithmetic, and never compute a score from figures you have already rounded.

*The one real fix — re-weighting every test to a multiple of four, so a 400-point Index lands every band on a whole number — is not made here. It would be a second non-comparable version boundary bought for a cosmetic gain, and the accounting already makes the arithmetic checkable.*

### Gates

Two tests are gates: **RCH-1** and **RCH-2**.

If either scores 0 or 1, set `gated: true` and record which one in `gate_failures`. Nothing else changes: `total` is computed exactly as in *Scoring* above, from every applicable test including the gate tests themselves, and `grade` is the band that real `total` falls in.

RCH-1 gates on the search crawlers of AI assistants, and a training crawler never counts toward it. RCH-2 gates on the edge: a firewall that refuses a search crawler removes the site from that assistant whatever `robots.txt` says.

Before 4.0, a gate failure capped the final score at 40 (`total = min(ungated_score, 40)`) and forced `grade` to `Gated`. That produced one number standing for two different facts — how well the site is built, and whether any of it is reachable today — and made them impossible to tell apart: a gated site with excellent structure scored identically to a gated site with none. Reporting `gated` and `total` as two separate facts says both; capping said neither.

### Verification mode

Every test declares how its band was determined:

- **`auto`** — the scanner determined the band from evidence it collected.
- **`auto-partial`** — the scanner produced a strong signal, but a human must confirm. Heuristics that can be fooled live here.
- **`manual`** — not observable from outside. **No scored test uses this mode.** Every point in the hundred is something the scanner can see for itself; what cannot be observed is shown in Posture or Measurement instead. The mode remains defined because PST-6 and MSR-2 to MSR-6 use it.

Automated coverage counts `auto-partial` at half weight, because a strong signal awaiting human confirmation is genuinely half-verified:

```
automated_coverage = (Σ auto_weight + 0.5 × Σ auto_partial_weight) ÷ Σ applicable_weight
```

The half is not arbitrary. Counting `auto-partial` at zero puts a ceiling of 0.92 on every possible run, because the always-applicable `auto-partial` tests (RED-3, RED-18 and UND-6) are 8 points that never leave the denominator. Counting it in full reports 1.00 for a site nobody has confirmed anything about, and erases the distinction the mode exists to draw.

Never let a `manual` check silently default to 4. An unanswered attestation scores `null` and drops out of the denominator, and the result records it as unverified.

#### Attestation against an `auto-partial` check

Three `auto-partial` tests have a top band that asks something no scanner can see. This document says so in each case, and each has a different observable ceiling because their band tables differ:

| Test | Unattested ceiling | What the attestation confirms |
|---|---|---|
| EXT-12 (IndexNow) | 3 | That IndexNow submissions fire on publish, not on a schedule |
| EXT-6 (generated markup) | 3 | That JSON-LD comes from mapped fields, confirmed with the build team |
| MSR-7 (search consoles) | 3 | That sitemaps are submitted and alerts and AI reports reach a named person |

Each of these three now has a band 3 that describes exactly what a scanner can see, so the attestation lifts 3 to 4 rather than jumping a gap. A test whose band table skips a value cannot express *mostly right*, and *mostly right* is the state most real sites are in.

An attestation may **raise the ceiling** on these three. It never sets a band and never lowers one: the scanner scores what it observed, and a supplied attestation permits that observed band to rise as far as the evidence supports. The result records which points came from a claim rather than a probe, and the report prints them as attested.

Without an attestation the test scores at its observable ceiling and the report says what would be needed to go higher. A client who did the work can prove it; a client who says nothing earns nothing.

Every other `auto-partial` test is fully observable. It carries that mode because the heuristic can be fooled — EXT-3 reads a key directory against what a draft requires, EXT-4 calls a live tool — not because it needs a client to vouch for it.

#### Tests that need a previous run

Two tests are defined against change over time: RED-3 (is `lastmod` a real signal or deploy noise) and UND-6 (do dates move only when content moves).

On a first run there is nothing to compare against. Score the observable half, **cap the band at 3**, set `confidence: medium`, and record `stability_unconfirmed` in the evidence. UND-6 already words its band 3 this way; RED-3 follows the same rule.

Supplying a previous run directory as a baseline lifts the cap and permits band 4.

Every ceiling — this one, the attestation ceiling above, and a test's own declaration
that it could not see further — records the reason it applied. A client told a number
was held below the evidence is owed the sentence explaining what would lift it. This makes the re-audit a first-class input to the score rather than a report-writing exercise, and it gives the client a visible, earnable reason the number rises next quarter.

## How the audit runs

### Sampling

Most tests score against a sampled page set, not the whole site. Build the sample like this:

1. **Always include:** the homepage, `/robots.txt`, `/sitemap.xml` (and every child sitemap), `/llms.txt`, `/.well-known/` probes, and every URL in the site's primary navigation.
2. **Stratify by content type.** Use the sitemap index, URL patterns, or a declared content-type map. Take up to 10 URLs per type.
3. **Add depth.** Include at least 5 URLs three or more levels deep, to catch templates the homepage never exercises.
4. **Add the money pages.** The client names up to 10 URLs that matter most — programs, services, donate, apply, contact. These are weighted double in coverage math.
5. **Cap the crawl.** Default 250 URLs. Configurable. Record the actual count.
6. **Read only HTML as a page.** A sampled address that answers with a PDF, an image or another document that is not HTML is recorded (its status, type and headers, so RED-5 and RED-18 still see it) and is not parsed, rendered or counted as a page in any page-level test. If every sampled address is such a document, they are read as before rather than scoring nothing.

Minimum viable sample is 25 URLs. Mark the run `low_confidence` only when the sample is under 25 **and** more URLs were discovered than were sampled. A twelve-page nonprofit site that was crawled in full is a complete measurement, not a weak one.

#### The representation sub-sample

Three tests want an extra request against every sampled URL: RED-10 (the Markdown copy a page advertises, or `{path}.md`), RED-12 (`Accept: text/markdown`, and cache behavior) and RED-5 (`X-Robots-Tag` on non-HTML). At the default 250-URL cap and one request per second, that is over 600 requests and roughly ten minutes of politeness delay stacked on top of the base crawl, against infrastructure that often belongs to a hospital.

Those three tests run against a **representation sub-sample**: 25 URLs by default, drawn from the main sample, always including every money page. The size is configurable and the selected URLs are recorded in the run metadata, so the sub-sample is reproducible across audits. Twenty-five pages resolves a rubric whose finest distinction is 75% against 95%.

### Fetching

Fetch every sampled URL twice:

- **Raw** — plain HTTP GET, no JavaScript, with a declared user-agent.
- **Rendered** — a headless browser with JavaScript enabled.

The difference between those two responses is the entire evidence base for RED-1 and RED-2, which together carry 15 points. Do not skip the second fetch. The Reach scan is the exception, and says so: it uses no browser, because none of its four tests needs one.

Separately, probe a small set of URLs with each search crawler's user-agent to feed RCH-2. There is no other way to measure what the edge does: `robots.txt` states an intention, a CDN rule states a fact, and the two disagree often enough that a readiness score which skipped the question would be worth less than the awkwardness of asking it.

Say plainly what that means, because it is the part an implementer will be asked about. **The wire-level `User-Agent` on those requests carries another company's product token** — `OAI-SearchBot`, `Claude-SearchBot`, and the others in the table below. Three constraints make that measurement rather than impersonation, and an implementation that drops any of them is doing something else:

1. **The requests still identify you.** Send your own `From` header and an `X-Audit-Operator` header naming your crawler on every probe. An operator inspecting the whole request, rather than the user-agent alone, can see who it was.
2. **Probe only URLs you were already allowed to fetch.** The probe runs over the sample, and the sample is filtered by `robots.txt` first. A probe must never reach, under somebody else's name, a page you declined to reach under your own.
3. **Publish the behavior before you do it**, at the URL in your own user-agent string, alongside how to opt out. Disclosure volunteered reads differently from disclosure discovered.

#### The agent classes

The Index groups the agents it names four ways. RCH-1 evaluates the search crawlers against `robots.txt` and the gate turns on them. RCH-2 probes the ones that actually issue requests. PST-1 shows the rest and never scores them.

| Class | Agents | RCH-1 | RCH-2 probe | Shown in |
|---|---|---|---|---|
| Search and answer crawlers | `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot`, `bingbot`, `Applebot`, `MistralAI-Index`, `meta-webindexer`, `Amzn-SearchBot` | yes | yes | RCH-1, RCH-2 |
| Fetchers that act on a person's request | `ChatGPT-User`, `Claude-User`, `Perplexity-User` | no | yes, where the operator publishes a user-agent string | PST-1 |
| Training and corpus | `GPTBot`, `ClaudeBot`, `CCBot`, `Bytespider` | no | shown, never scored | PST-1 |
| Directive-only | `Google-Extended`, `Applebot-Extended` | no | **no** | PST-1 |

`Googlebot` and `bingbot` are in RCH-1 because the AI answers of Google and Microsoft are built on their indexes. `Applebot` follows the `Googlebot` group when `robots.txt` does not name it, and the verdict says which group it used. A fetcher that acts on a person's request is not held to `robots.txt` by its operator's own documentation in several cases, which is why it is listed in PST-1 and not gated on.

`Google-Extended` and `Applebot-Extended` are not crawlers. They are opt-out tokens that Google and Apple honor in `robots.txt`; no request ever arrives carrying either string. Blocking them is a rights decision with no fetch behavior attached, which is why PST-1 lists them and RCH-2 cannot probe them. A user-agent matrix that lists them is describing a crawler that does not exist.

xAI publishes no crawler documentation and no list of its addresses. The names `GrokBot`, `xAI-Grok`, `Grok-DeepSearch` and `xAI-SearchBot` are known only from third-party directories, so PST-1 reports whether `robots.txt` names them, says that, and scores nothing.

#### The Reach scan

The free scan runs RCH-1 to RCH-4: one page, `robots.txt` and the edge probe, with no browser and no sign-in. It reports points out of 25, and a site can score 25 of 25. A Reach score is not a score out of 100 and is never compared with one. The posture panel (including the prompt in PST-6), `llms.txt` and the other unscored items are shown from the same fetches, so the free scan reads nothing the full scan does not.

### Politeness

Respect `Crawl-delay`. Default to 1 request per second with 4 concurrent workers. Back off on 429 and 503, honoring `Retry-After` where it is given, and abandon a host that keeps refusing rather than retrying into a wall. Cache every response to disk so re-scoring never re-crawls.

### Consent

Two different questions, and conflating them is how a scanner ends up doing something indefensible.

**Whose site may you scan?** A client audit runs with the client's agreement, recorded before the crawl. A survey of a public population — see *Populations*, below — runs without asking each site first, on the same footing as any other published measurement of the public web. What is not acceptable in either case is scanning under a consent you did not obtain. Record which basis a run used, in the run itself.

**What may you fetch once you are there?** `robots.txt`, and specifically the group addressed to your own crawler. Name your crawler in your user-agent string, publish a page at the URL that string points to, and stop when a site names you and disallows you.

A scanner may reasonably decide that a blanket `User-agent: *` disallow does not address it — a `*` rule is aimed at the anonymous scrape, and a named crawler with a published policy, a rate limit and a working opt-out is not that. If you make that choice, **publish it on your crawler's own page** and honor `Crawl-delay` under `*` regardless, because a rate limit is not an exclusion. What is not defensible is making the choice quietly.

### Populations

A survey scores a defined population and publishes the aggregate. Two rules keep it a measurement rather than an accusation.

**Cite the population.** Record the source list, its publication date and its URL. "How did you pick these" is the first question anyone asks, and the answer has to be a citation rather than a judgment call. Use sources you may lawfully redistribute, and claim no ownership over somebody else's list.

**Publish the version and the date.** Every result records which version of this Index it was scored against and the date that version took effect. Without both, an old number silently starts meaning something new the next time the Index changes.

### Reproducibility

Store the raw evidence — headers, HTML, extracted JSON-LD, screenshots — in a run directory keyed by timestamp. A score you cannot reproduce next quarter is an opinion, not a measurement.

## Result schema

The scanner writes one `result.json` per run. Everything else (Markdown report, HTML dashboard, remediation backlog) renders from this file.

```json
{
  "schema_version": "1.0",
  "index_version": "12.0",
  "site": {
    "name": "Example University",
    "base_url": "https://example.edu",
    "vertical": "higher-ed",
    "cms": "drupal-10"
  },
  "run": {
    "id": "2026-11-03T20-14-33Z",
    "started_at": "2026-11-03T20:14:33Z",
    "finished_at": "2026-11-03T20:41:02Z",
    "scanner_version": "0.1.0",
    "urls_sampled": 187,
    "representation_sample": 25,
    "low_confidence": false,
    "baseline_run_id": null,
    "extraction_method": "readability-density",
    "extraction_version": "1"
  },
  "score": {
    "total": 61.4,
    "gated": false,
    "gate_failures": [],
    "grade": "Adequate",
    "applicable_weight": 94,
    "earned_points": 58,
    "earnable_points": 88,
    "automated_coverage": 0.87
  },
  "dimensions": [
    {
      "id": 3,
      "name": "Understand",
      "weight": 18,
      "applicable_weight": 18,
      "earned_points": 9,
      "score_pct": 50.0
    }
  ],
  "checks": [
    {
      "id": "UND-4",
      "title": "Does each article show who wrote it, with a page about the author?",
      "dimension": 3,
      "weight": 2,
      "applicability": "always",
      "applicable": true,
      "na_reason": null,
      "verification": "auto",
      "band": 2,
      "earned_points": 1,
      "confidence": "high",
      "summary": "3 of 7 distinct authors have a page or profile a machine can find.",
      "evidence": [
        {
          "url": "https://example.edu/news/new-lab",
          "author": "A. Rivera",
          "profile_found": false
        }
      ],
      "remediation": {
        "severity": "major",
        "effort": "medium",
        "summary": "Give each author a page.",
        "detail": "Four recurring authors are named in bylines with nothing behind the name..."
      }
    }
  ],
  "remediation_backlog": [
    {
      "rank": 1,
      "check": "RED-1",
      "points_available": 11,
      "severity": "critical",
      "effort": "large"
    }
  ]
}
```

#### Schema notes

- The `dimensions` array and each test's `dimension` hold the four categories: 1 Reach, 2 Read, 3 Understand, 4 Act. The names are kept so a stored result from an earlier Index still loads.
- A test that is not scored (Posture, Extras and Measurement) carries `weight` 0 and no `dimension`, and never enters `score`, `applicable_weight` or `earnable_points`.
- `site.cms` is best-effort, from the `generator` meta tag and response headers. It is nullable and nothing scores against it.
- A category with no applicable tests reports `score_pct: null`, not `0`. Zero means measured and failed.
- **Rounding happens once, at the end.** All arithmetic runs unrounded; the values written to this file are rounded to one decimal for display. The per-check `earned_points` therefore will not sum exactly to `score.earned_points`, and neither is wrong. Do not "fix" this by rounding intermediates — that reintroduces the drift the single rounding step exists to prevent.
- `extraction_method` and `extraction_version` record how main-content text was isolated. When extraction improves, old scores stay interpretable because the method that produced them is on the record.

### Remediation ranking

Sort the backlog by **points available** (`weight − earned_points`), then by effort ascending, then by check ID ascending. The last key is not cosmetic: two runs of the same evidence must produce the same backlog in the same order, or the re-audit comparison is unreadable.

A check appears in the backlog only if it is applicable, has a band, and has points available above zero. N/A checks, unattested `manual` checks, and checks already at band 4 are not remediation items.

Use three severities — `critical`, `major`, `minor` — and three effort sizes — `small`, `medium`, `large`. Effort is a property of the check, defined in this document. Severity is derived: gate failures and any check scoring **0 or 1** with weight ≥3 are `critical`; band ≤2 with weight ≥2 is `major`; everything else is `minor`.

Band 1 on a heavy check is a critical finding. A site whose program pages ship 22% of their content scores RED-1 at band 1, not 0, and calling that `major` alongside a missing caption on a table understates it to the person deciding what to fund.

The client-facing output is not the score. It is the ordered list of what to fix and what each fix is worth.

### Who fixes it

Fixing a failed test is work, and different tests need different people: a firewall rule, a template, a paragraph on an About page, a decision about what the organization permits. Each entry therefore names who typically does the work in a **Fixed by** bullet, so a reader of a result knows whose desk it lands on.

There are six roles. An entry lists one to three of them, **in order: the first is who typically does or drives the work, and the others are whose input or hands it also needs.** A decision an entry depends on, such as a licensing policy, is made by the **Site owner** and appears in that entry's Fix text as well.

| Role | Who they typically are | What they do for the Index |
|---|---|---|
| Site owner | Leadership, the communications head, counsel | Decide what the organization permits, licenses and says in public. |
| Content team | Editors, content strategists, communications and web staff | Write and maintain what pages and media say: facts, FAQs, alt text, authors, reviewers, citations. |
| Search specialist | SEO and digital marketing, analytics | Own crawl and index signals, robots.txt, redirect and sitemap strategy, the search consoles, and the measurement of AI referrals. |
| Front-end developer | Themer, UI engineer, accessibility developer | Own templates and markup: HTML structure, headings, tables, forms, and what renders without JavaScript. |
| Back-end developer | CMS developer, platform engineer, module developer | Own the data model and what the site generates: structured data, sitemaps, feeds, redirects, APIs and Markdown. |
| Operations | DevOps, infrastructure and security engineers, the CDN administrator | Own the edge and the servers: CDN and firewall rules, caching, headers, bot verification, logs and signing keys. |

This is guidance, not a requirement, and it does not touch the score. Organizations divide the work differently: at a small nonprofit one person holds three of these roles, and at a university each is a team. The roles say what kind of skill the fix needs, not how many people that takes. A report that groups the work by role uses each entry's first role, so the points in the groups add up to the points available.

## What counts as evidence

Every test carries one **evidence label**, and every source it cites carries a **grade**. Together they say how far a reader should lean on a test, and they decide whether it carries points.

### Evidence labels

| Label | Meaning |
|---|---|
| **AI product** | A named AI product or agent is documented using it. The operator's own documentation says so. |
| **Search index** | Documented for Google or Bing, not for an AI product. Google's own guide says no special markup is needed for its AI features, so this is weaker than it looks. |
| **Standard only** | A published standard or draft with no documented consumer. |
| **None found** | No source found either way. Absence of evidence is not evidence of absence, and the test says so. |
| **Practice** | Sound practice with no documented consumer. It is good for people, and no AI company documents using it. |
| **Scanner-listed** | A published scanner checks it (Cloudflare's Agent Readiness score, Lighthouse's agentic browsing category) and no AI product is documented using it. A scanner measures; it is not a reader. Shown and never scored. |

A label may carry a short parenthetical that narrows it, such as (coding agents only). The parenthetical is part of the claim: a test credited for coding agents is not credited for search crawlers.

### Source grades

| Grade | Meaning |
|---|---|
| **A** | Operator or standards-body documentation, read directly from the source. |
| **B** | An independent measurement or study, or a vendor's own data. |
| **C** | A single blog or a third-party directory. |

A scored test must not rest on a grade C source alone. A source whose address or date could not be confirmed is marked so in the test's **Sources** line.

### Policy

- **A test is scored only if it has documented use.** That means the AI product or Search index label, or the Practice label, which is scored at one point and shown as Practice. A test labeled Standard only, Scanner-listed or None found is measured and shown in Posture, Extras or Measurement, and is worth no points. A site that does it is credited in words and is never marked down for not doing it.
- **Every test carries a review date six months out.** The date is on the test's **Review by** line: 2027-04-18 for the tests as published in 12.0. A test is also re-read when a source it cites moves, changes or disappears, and it is changed if the reading changed.
- **A label that moves a test into or out of the score is a change to the score,** and follows *Versioning and change control*. A corrected citation or a reworded question is a minor change.

---

# The tests

Each entry gives: the question the test asks in plain language, its points, applicability, verification mode, effort, who typically fixes it, the evidence label, what the test measures, why it matters with a source that is not us, the full list of graded sources, how to detect it, what evidence to keep, the band rule when it differs from the default coverage rubric, how to fix it, what changed from Index 11, which Index 11 test it replaces, and when it is next reviewed.

The **Question** and **Why this matters** bullets are written for somebody who has never read this document, in plain words with the technical terms left to **Detect**. **Why this matters** is a plain description of the test, then a link to the documentation of a standards body, a search engine or an AI company that backs it, then one sentence on why that source is worth citing. A scanner or a report that explains a test to a client uses those words rather than its own, so every explanation of a test says the same thing. **Evidence** is the label defined in *What counts as evidence*, and **Sources** is every citation behind it with its date and grade. **Evidence kept** is what the scanner records for the run.

A test that replaces one or more Index 11 tests says so in **Replaces**. The full map is in *The crosswalk from Index 11*.

## #1 · Reach · 4 tests · 25 pts

**Points 25**

These four tests can each be answered from a single page and the site's front-door files, `robots.txt` and the edge, which is what makes the free Reach scan possible: it reads one page, runs exactly these four, uses no browser and reports points out of 25. Every test in the groups that follow needs more than one page, or a render, or a fetch of something beside the page, and runs only in a full scan.

### RCH-1 — Can the AI tools that search the web read your site?

- **Question:** Can the AI tools that search the web read your site?
- **Points:** 8
- **Gate**
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Search specialist, Site owner
- **Evidence:** AI product
- **Measures:** We read your robots.txt file, which tells crawlers what they may read, for the search crawlers behind ChatGPT, Claude, Perplexity, Google, Bing, Apple, Meta, Amazon and Mistral. If one is blocked, that assistant cannot cite you.
- **Why this matters:** Your robots.txt tells crawlers what they may read. If it shuts out the search crawler behind an assistant, that assistant cannot cite you. [OpenAI, crawler overview](https://developers.openai.com/api/docs/bots): OpenAI names its own crawlers there, so it is the place to confirm which names robots.txt has to address.
- **Sources:** [OpenAI, crawler overview](https://developers.openai.com/api/docs/bots), undated (A); [Anthropic Help Center, crawler controls](https://support.claude.com/en/articles/8896518), 2026-04-07 (A); [Perplexity, crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers), undated (A); [Meta, web crawlers](https://developers.facebook.com/docs/sharing/webmasters/web-crawlers), undated (A); [Apple, About Applebot](https://support.apple.com/en-us/119829), 2026-09-04 (A)
- **Detect:** Parse `robots.txt`. Evaluate each of the nine search crawlers (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot`, `bingbot`, `Applebot`, `MistralAI-Index`, `meta-webindexer`, `Amzn-SearchBot`) against the rule set, for `/` and for three sampled content URLs. Resolve `User-agent: *` fallbacks and the longest-match group rule, and let a crawler inherit the group it falls back to: Applebot follows the `Googlebot` group when `robots.txt` does not name it. Training crawlers and the fetchers that act on a person's request are evaluated as well and shown in PST-1; they never change this band.
- **Evidence kept:** Raw `robots.txt`, the parsed rule tree, a per-crawler allow/deny verdict for `/` and for three sampled content URLs, and which group each verdict came from.
- **Bands:** anchored on *which* crawlers are blocked, not how many. The five major search crawlers are `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot` and `bingbot`; the other four are `Applebot`, `MistralAI-Index`, `meta-webindexer` and `Amzn-SearchBot`.
  - **4** — every one of the nine may fetch content paths.
  - **3** — one or two of the other four blocked; all five major crawlers allowed.
  - **2** — three or four of the other four blocked; all five major crawlers allowed.
  - **1** — exactly one major search crawler blocked.
  - **0** — `Disallow: /` for `*` with no named exception, or two or more major search crawlers blocked.
- **Why the gate turns on the search crawlers:** the Index measures whether machines can find, read and *use* a site. A search or answer crawler blocked in `robots.txt` removes the site from that assistant, which is the failure the gate exists to catch. A training block is a rights choice, and this document declines to judge rights choices: PST-1 shows them and never scores them. A university that blocks `GPTBot` and welcomes `OAI-SearchBot` is reachable, and gating it would measure our approval rather than machine reach.
- **Consequence:** blocking every training crawler costs no points and does not gate. Blocking a single major search crawler gates.
- **Absent robots.txt:** a 404 scores 4. Nothing is disallowed, so nothing is blocked. A missing file is not a failure of this test.
- **Note:** A deliberate, documented block is a business decision, not a defect. Record it, score it honestly, and say in the report that the client chose it. The number reflects machine reach, not our approval.
- **Fix:** Remove inherited blocks. Keep only directives the client can explain.
- **What changed in 12.0:** Names each company's search crawler (adds Claude-SearchBot, Googlebot, bingbot, Applebot, MistralAI-Index, meta-webindexer, Amzn-SearchBot). Training crawlers no longer cost points. Points: 5 in 11.5, 8 in 12.0.
- **Replaces:** AIR-1.1
- **Review by:** 2027-04-18

### RCH-2 — Does your website let those crawlers in, or does your security turn them away?

- **Question:** Does your website let those crawlers in, or does your security turn them away?
- **Points:** 12
- **Gate**
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Operations, Back-end developer
- **Evidence:** AI product
- **Measures:** We visit the site the way each crawler would and see whether your firewall or CDN refuses it, slows it down or shows a challenge page it cannot pass.
- **Why this matters:** A firewall or bot rule can turn a crawler away even when robots.txt says yes, or put a challenge page in front of it that it cannot pass. We request pages the way each crawler does and record what comes back. [Cloudflare, new AI traffic options](https://blog.cloudflare.com/content-independence-day-ai-options/): Cloudflare sits in front of a large share of the web, and this is its own account of the crawler settings most sites actually enforce.
- **Sources:** Cloudflare, 'Perplexity is using stealth, undeclared crawlers' (address to confirm), 2025-08-04 (A); [Cloudflare, new AI traffic options](https://blog.cloudflare.com/content-independence-day-ai-options/), 2026-07-01 (A); [RESONEO, LLM crawler test](https://think.resoneo.com/sentinel/geo-llm-crawler-report.html), 2026-01 (B)
- **Detect:** Two halves, both read from the same probe. **The edge half:** request 10 sampled URLs with each search crawler's real User-Agent string (the nine named in RCH-1) and with the user-triggered fetchers whose operators publish a user-agent string (`ChatGPT-User`, `Claude-User`, `Perplexity-User`). Record status code, response size, and whether the body matches the baseline fetch. Flag 403, 429, 503 and bodies more than 40% smaller than baseline. Training crawlers are probed too, on three URLs, and shown in PST-1; a block of them is a rights choice and does not change this band. Cloudflare publishes no response header that names its Search, Agent and Training settings, so where responses come through Cloudflare the scan reports, per class, whether the crawlers were served or turned away, and says that this is read from the pattern and not from a setting. **The challenge half:** request browse, search, listing and detail pages with the scanner's own identity and look for Turnstile, reCAPTCHA, hCaptcha and JavaScript-challenge signatures, meta-refresh interstitials and challenge cookies in the raw response, on every URL that is not a form or a login.
- **Evidence kept:** A crawler × URL matrix of status codes, sizes and challenge detection, and the matching signature for every challenge found.
- **Bands:** the weakest half decides the band.
  - **4** — every crawler gets `200` with full content, and no read-only page carries a challenge.
  - **3** — one crawler rate-limited but eventually served.
  - **2** — one crawler blocked or challenged, or a challenge on a minority of read-only pages.
  - **1** — several crawlers blocked or challenged, or a challenge on most read-only pages.
  - **0** — most crawlers blocked.
- **Note:** The wire-level `User-Agent` on these requests carries another company's product token. *Fetching*, above, states the three constraints that make that measurement rather than impersonation.
- **Fix:** Audit Cloudflare bot settings, Pantheon AGCDN rules, Fastly VCL and origin WAF. Scope challenges to `POST` endpoints and authenticated routes. Verify by re-running this probe, not by reading configuration.
- **What changed in 12.0:** Absorbs the challenge-page check. Reads Cloudflare's Search, Agent and Training settings where they can be seen. Points: 6 in 11.5, 12 in 12.0.
- **Replaces:** AIR-1.2, AIR-1.3
- **Review by:** 2027-04-18

### RCH-3 — Does each page say which web address is the real one?

- **Question:** Does each page say which web address is the real one?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** Search index
- **Measures:** We look for the canonical link on the page and check that it points to a working address that agrees with itself.
- **Why this matters:** A canonical link names the true address of a page. Without one, the same content can read as several competing pages. [Google, canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization): Google explains how its index decides which address is real, and its AI answers draw on that index.
- **Sources:** [Google, canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization), 2026-08-20 (A); [Google, AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), 2025-12-10 (A)
- **Detect:** For each sampled page, extract the canonical and resolve it. Flag: missing, multiple, cross-host, pointing at a redirect, pointing at a non-200, or pointing at the homepage from a deep page.
- **Evidence kept:** Per page: the canonical found, its resolved status, and the flag raised.
- **Fix:** Emit a self-referencing canonical by default and correct the exceptions.
- **What changed in 12.0:** Detection and bands unchanged. Points: 2, unchanged from 11.5.
- **Replaces:** AIR-1.7
- **Review by:** 2027-04-18

### RCH-4 — Do your page settings let assistants quote you?

- **Question:** Do your page settings let assistants quote you?
- **Points:** 3
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Search specialist, Back-end developer
- **Evidence:** AI product
- **Measures:** We look for tags and headers that keep a page out of search or out of AI answers, such as noindex, nosnippet, noarchive and nocache, and whether they sit on pages you want cited.
- **Why this matters:** Page tags and headers that stop a search engine from showing a snippet, or from indexing a page at all, also keep that page out of the AI answers built on the search index. [Google, AI features and your website](https://developers.google.com/search/docs/appearance/ai-features): Google documents that its snippet controls apply to its AI features, so a stray tag has a consequence there.
- **Sources:** [Google, robots meta tag and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag), 2026-03-24 (A); [Google, AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), 2025-12-10 (A); [Bing Webmaster Blog, usage controls (noarchive, nocache)](https://blogs.bing.com/webmaster/september-2023/Announcing-new-options-for-webmasters-to-control-usage-of-their-content-in-Bing-Chat), 2023-09-22 (A); [Apple, About Applebot](https://support.apple.com/en-us/119829), 2026-09-04 (A)
- **Detect:** Parse `<meta name="robots">` and the bot-specific meta names (`googlebot`, `bingbot`, `applebot`) and the `X-Robots-Tag` header, including its user-agent-prefixed form, across the sample. Flag `noindex`, `nosnippet`, `max-snippet:0`, `noarchive` and `nocache`, and say which crawler each is addressed to. A directive on a page that is meant to be cited counts against it; pages that are deliberately private (login, account, cart, internal search results, confirmation pages) are left out of the sample for this test.
- **Evidence kept:** Per page: every robots directive found, where it came from (tag or header), and the crawler it addresses.
- **Bands:** Default coverage rubric, where a page passes only if no directive removes it from search or from AI answers.
  - A site-wide `noindex` or `nosnippet` is **band 0**, whatever the sample says.
- **Note:** `noarchive` is counted because Bing documents it as live. Google removed its cache, so the Index no longer reasons from `noarchive` for Google.
- **Fix:** Remove the directives from pages you want cited. They are almost always left over from a legacy SEO module or a staging template.
- **What changed in 12.0:** Rewritten around Google, Bing and Apple, and now also catches noindex and a zero snippet length. noarchive is live for Bing. Points: 1 in 11.5, 3 in 12.0.
- **Replaces:** AIR-1.6
- **Review by:** 2027-04-18

## #2 · Read · 19 tests · 35 pts

**Points 35**

Reach asks whether an AI system can get in. Read asks whether it can find the pages and read the words once it has. The tests of finding pages (sitemaps, redirects, missing pages, filters, pagination, file rules) sit here with the tests of reading them (the text in the first response, Markdown copies, page structure), because both decide whether a page is usable once somebody has the address.

### RED-1 — Is your page's text in the page itself, without needing JavaScript?

- **Question:** Is your page's text in the page itself, without needing JavaScript?
- **Points:** 10
- **Applicability:** always
- **Verification:** auto
- **Effort:** large
- **Fixed by:** Front-end developer, Back-end developer
- **Evidence:** AI product
- **Measures:** We compare the text in the first response from your server with the text a browser shows after scripts run. Most AI crawlers only ever see the first one.
- **Why this matters:** If your text only appears after JavaScript runs, a tool that does not run it sees an empty page. This is the heaviest test in the Index. [Anthropic, web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool): Anthropic documents that its fetch tool does not run JavaScript, which is exactly the behavior this test measures.
- **Sources:** [Anthropic, web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool), current (A); [Vercel and MERJ, 'The rise of the AI crawler'](https://vercel.com/blog/the-rise-of-the-ai-crawler), 2024-12-17 (B); [RESONEO, LLM crawler test](https://think.resoneo.com/sentinel/geo-llm-crawler-report.html), 2026-01 (B); [Google, JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), 2026-03-04 (A)
- **Detect:** For every sampled URL, extract main-content text from the raw fetch and from the rendered fetch. Compute `coverage = raw_chars ÷ rendered_chars` after normalizing whitespace and stripping nav, header and footer regions, and report its complement, the share of words missing from the first response, beside it. Average across the sample and report the per-template distribution.
- **Evidence kept:** Per-URL character counts, coverage ratio, and the first 500 characters of each version for spot-checking.
- **Bands:** mean coverage.
  - **4** — mean coverage ≥0.95.
  - **3** — 0.80–0.94.
  - **2** — 0.50–0.79.
  - **1** — 0.20–0.49.
  - **0** — below 0.20.
- **Edge cases:** Coverage above 1.0 happens when JavaScript *removes* content that the raw response contained. Clamp the per-URL value to 1.0 for banding and keep the unclamped ratio in the evidence. A URL whose rendered text is empty is excluded from the mean and the exclusion is recorded: it is a fetch problem, not a coverage measurement.
- **Note:** Report the worst-performing template by name. "Your program pages ship 8% of their content" lands harder than a mean. Google's and Apple's crawlers render JavaScript and several AI fetchers do not; date the claim, because it is changing.
- **Fix:** Server-render or statically render. For decoupled Drupal this is the largest line item in most remediations.
- **What changed in 12.0:** Measures the share of words missing from the first response instead of pass or fail. Points: 6 in 11.5, 10 in 12.0.
- **Replaces:** AIR-2.1
- **Review by:** 2027-04-18

### RED-2 — Is the text behind tabs and 'read more' buttons already on the page?

- **Question:** Is the text behind tabs and 'read more' buttons already on the page?
- **Points:** 5
- **Applicability:** conditional — the site uses tabs, accordions, load-more or infinite scroll
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer
- **Evidence:** AI product
- **Measures:** We check that text hidden behind tabs, accordions and 'read more' buttons is in the first response and is not removed from the page until someone clicks.
- **Why this matters:** Tabs and accordions are fine, as long as their text is already in the page before anybody clicks. [Anthropic, web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool): The same tool does not run JavaScript, so anything that only appears after a click is out of its reach.
- **Sources:** [Anthropic, web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool), current (A); [RESONEO, LLM crawler test](https://think.resoneo.com/sentinel/geo-llm-crawler-report.html), 2026-01 (B); [Google, control your snippets](https://developers.google.com/search/docs/appearance/snippet), 2026-04-20 (A)
- **Detect:** Identify disclosure widgets by ARIA roles (`tab`, `tabpanel`, `region` with `aria-expanded`), `<details>` and common class patterns. For each, check that the panel body is populated in the raw HTML **and** that the rendered page still holds it: text that a script removes from the page until someone clicks fails. Detect infinite scroll by watching for XHR content growth on scroll in the rendered fetch, and check for a paginated fallback.
- **Evidence kept:** Per widget: the pattern found, whether the panel body is in the raw HTML and in the rendered page.
- **Bands:** 4 — every panel populated in raw HTML and kept in the page; infinite scroll has crawlable pagination. 3 — one pattern incomplete. 2 — panels populated on some templates only. 1 — most content loads on interaction. 0 — all disclosure content is fetched on demand.
- **Note:** Text present in the HTML and hidden with CSS passes. One independent test reports that some tools may still drop CSS-hidden text; that result is on the evidence register's open list, and the rule tightens if it is confirmed.
- **Fix:** Render all panels and hide with CSS, never by removing the text. Give infinite scroll a paginated fallback.
- **What changed in 12.0:** Asks for visible on load, not only present. Points: 3 in 11.5, 5 in 12.0.
- **Replaces:** AIR-2.2
- **Review by:** 2027-04-18

### RED-3 — Can a crawler trust the 'last changed' dates in your sitemap?

- **Question:** Can a crawler trust the 'last changed' dates in your sitemap?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** medium
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** AI product
- **Measures:** We compare the dates in your sitemap with whether the pages actually changed.
- **Why this matters:** A last-changed date should mean the content changed, not that you deployed. Once it is noise, crawlers stop trusting it. [Bing Webmaster Blog, sitemaps in AI-powered search](https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search): Bing ties these dates to how quickly updates reach its search and AI answers.
- **Sources:** [Bing Webmaster Blog, sitemaps in AI-powered search](https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search), 2025-07-31 (A); [Google, build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), 2026-07-08 (A)
- **Detect:** Parse all `lastmod` values. Flag clustering: more than 60% of URLs sharing a single date, or timestamps identical to the minute across content types. Cross-check against on-page `dateModified` where present. Re-run across two audits to confirm.
- **Evidence kept:** The `lastmod` distribution, the clustering found and the on-page dates compared.
- **Bands:** 4 — values are distributed and match on-page dates. 3 — mostly accurate with some clustering. 2 — heavy clustering. 1 — all identical. 0 — absent.
- **First run:** cap at 3 without a baseline run. See *Tests that need a previous run*.
- **Fix:** Wire `lastmod` to the node's changed timestamp, not to cron.
- **What changed in 12.0:** Bing ties sitemap dates to how fast updates reach AI answers, which is why the test stays in the score. Points: 2, unchanged from 11.5.
- **Replaces:** AIR-4.8
- **Review by:** 2027-04-18

### RED-4 — Do your filters and calendars keep a crawler from getting lost?

- **Question:** Do your filters and calendars keep a crawler from getting lost?
- **Points:** 1
- **Applicability:** conditional — the site has search, filtering or a calendar
- **Verification:** auto-partial
- **Effort:** medium
- **Fixed by:** Search specialist, Back-end developer
- **Evidence:** Search index
- **Measures:** We look for endless combinations of links, such as filter and date pages, that waste a crawler's visit.
- **Why this matters:** Filters and calendars can generate millions of addresses. A crawler spends its visit there instead of on the pages you care about. [Google, canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization): Google explains how it groups duplicate and parameterized addresses, which is the waste filters and calendars create.
- **Sources:** [Google, canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization), 2026-08-20 (A)
- **Detect:** Crawl listing pages two levels deep with parameters followed. Measure URL growth rate and count distinct parameter combinations. Check whether those URLs are disallowed, `noindex`, or canonicalized to the unfiltered listing.
- **Evidence kept:** Growth per level, the parameter combinations counted and the control found for each.
- **Bands:** 4 — parameter space bounded by robots rules, `noindex` or canonicals. 3 — mostly controlled with gaps. 2 — partially controlled. 1 — minimal control. 0 — unbounded expansion observed.
- **Fix:** Combine disallow patterns, `noindex` on parameterized views, and canonicals back to the base listing.
- **What changed in 12.0:** Detection and bands unchanged. Points: 2 in 11.5, 1 in 12.0.
- **Replaces:** AIR-4.7
- **Review by:** 2027-04-18

### RED-5 — Do your PDFs and images have their own rules for search and quoting?

- **Question:** Do your PDFs and images have their own rules for search and quoting?
- **Points:** 1
- **Applicability:** conditional — the site serves PDFs, documents, media or JSON endpoints
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Operations
- **Evidence:** Search index
- **Measures:** We check the X-Robots-Tag header on files that are not web pages.
- **Why this matters:** PDFs, images and JSON cannot carry a meta robots tag, so the instruction has to travel in the HTTP header instead. [Google, robots meta tag and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag): Google documents the header for files that cannot hold a tag, including the snippet controls that apply to its AI features.
- **Sources:** [Google, robots meta tag and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag), 2026-03-24 (A)
- **Detect:** HEAD every sampled PDF, document, media file and API endpoint. Record `X-Robots-Tag`. Flag `noindex` on substantive content and absent directives on endpoints that should be excluded.
- **Evidence kept:** Per resource: the type, the header found and the flag raised.
- **Bands:** 4 — every non-HTML type carries a deliberate, correct value. 2 — mixed or partial. 0 — absent everywhere, or substantive PDFs marked `noindex`.
- **Fix:** Set headers by path pattern at the CDN or web server.
- **What changed in 12.0:** Detection and bands unchanged. Points: 1, unchanged from 11.5.
- **Replaces:** AIR-4.4
- **Review by:** 2027-04-18

### RED-6 — Do missing pages say they are missing?

- **Question:** Do missing pages say they are missing?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Operations
- **Evidence:** Search index
- **Measures:** We ask for pages that do not exist and check the answer is a real 404 or 410, not a normal-looking page.
- **Why this matters:** A missing page that answers 200 OK looks like a real page, and a crawler spends its visit on it. [Google, HTTP status codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes): Google lists how its crawler treats each status code, including pages that should have been errors.
- **Sources:** [Google, HTTP status codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes), 2026-02-04 (A); [Vercel and MERJ, 'The rise of the AI crawler'](https://vercel.com/blog/the-rise-of-the-ai-crawler), 2024-12-17 (B)
- **Detect:** Request 10 deliberately invalid URLs under real path prefixes. Flag `200` responses. Separately, flag sampled pages whose body matches a not-found template or falls below a minimum content threshold while returning `200`.
- **Evidence kept:** Probe URLs with status codes and body fingerprints.
- **Note:** One study found AI crawlers spent about a third of their visits on missing pages. The claim here is limited to wasted visits.
- **Fix:** Return real status codes. Use `410` for content that is permanently gone.
- **What changed in 12.0:** Citation updated; the claim is limited to wasted visits. Points: 1, unchanged from 11.5.
- **Replaces:** AIR-4.5
- **Review by:** 2027-04-18

### RED-7 — Do your redirects go straight to the right page?

- **Question:** Do your redirects go straight to the right page?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** Search index
- **Measures:** We follow your redirects and count the hops.
- **Why this matters:** Every extra redirect is another chance for a crawler to give up. One hop, straight to the destination. [Google, HTTP status codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes): Google states how many redirect hops its crawler follows, which is the limit this test works inside.
- **Sources:** [Google, HTTP status codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes), 2026-02-04 (A)
- **Detect:** Follow redirects without auto-resolution and count hops per sampled URL and per internal link target.
- **Evidence kept:** Per URL: the chain, its length and whether it loops.
- **Bands:** 4 — no chain exceeds one hop. 3 — a few two-hop chains. 2 — chains of three or more. 1 — widespread chains, meaning both more than 10% of the sample and at least three URLs. 0 — loops present.
- **Note:** Google follows up to ten hops. That is a limit, not a recommendation, and the test asks for one hop because every hop is another request.
- **Fix:** Flatten the redirect table so every source points at its final destination.
- **What changed in 12.0:** Citation updated to Google's ten-hop limit. Points: 1, unchanged from 11.5.
- **Replaces:** AIR-4.6
- **Review by:** 2027-04-18

### RED-8 — Do you have sitemaps for your images and videos?

- **Question:** Do you have sitemaps for your images and videos?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** Search index
- **Measures:** We look for image and video sitemaps.
- **Why this matters:** Image and video sitemaps tell a crawler about media it would not find in the page text. [Google, build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap): Google's own instructions for the sitemap extensions its crawler reads.
- **Sources:** [Google, build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), 2026-07-08 (A)
- **Detect:** Fetch the sitemaps named in `robots.txt` and at `/sitemap.xml`. Look for image and video sitemap entries, or child sitemaps of those types, where the sampled pages carry substantial media. Validate against the sitemap schema and the 50,000-URL and 50 MB limits.
- **Evidence kept:** The sitemaps found, the media types they cover and any limit exceeded.
- **Bands:** 4 — the sampled pages carry no substantial media, or image and video sitemaps are present and valid. 2 — present but invalid or partial. 0 — substantial media and no media sitemap.
- **Note:** The claim that splitting a sitemap by content type helps was dropped: it is a Search Console convenience, and no source ties it to AI answers.
- **Fix:** Generate image and video sitemaps from the media library and submit them to both search consoles.
- **What changed in 12.0:** The claim that splitting a sitemap by content type helps is dropped. Points: 1, unchanged from 11.5.
- **Replaces:** AIR-4.9
- **Review by:** 2027-04-18

### RED-9 — Can a crawler reach page two, three and beyond without clicking a button?

- **Question:** Can a crawler reach page two, three and beyond without clicking a button?
- **Points:** 1
- **Applicability:** conditional — the site has paginated listings or multi-page articles
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Search specialist, Back-end developer
- **Evidence:** Search index
- **Measures:** We check that lists of pages link to the next page with ordinary links, not only a 'load more' button.
- **Why this matters:** Page two and everything after it has to be reachable with an ordinary link, because a crawler does not click a button. [Google, JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics): Google explains what its crawler does and does not do with JavaScript, including content that loads on a click.
- **Sources:** [Google, JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), 2026-03-04 (A); [Vercel and MERJ, 'The rise of the AI crawler'](https://vercel.com/blog/the-rise-of-the-ai-crawler), 2024-12-17 (B)
- **Detect:** Identify paginated series by URL pattern. Check that each page links to the next with an ordinary link in the raw HTML and not only through a 'load more' button, that a view-all page carries the canonical where there is one, and that deep pages are reachable by crawl. `rel=next` and `rel=prev` are reported and not required.
- **Evidence kept:** Per series: the link found, whether it is in the raw HTML, and the depth reached.
- **Fix:** Prefer a view-all canonical where page weight allows, and give every list ordinary next-page links.
- **What changed in 12.0:** Detection and bands unchanged. Points: 1, unchanged from 11.5.
- **Replaces:** AIR-4.10
- **Review by:** 2027-04-18

### RED-10 — Do you offer a plain-text (Markdown) copy of your pages?

- **Question:** Do you offer a plain-text (Markdown) copy of your pages?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer
- **Evidence:** AI product
- **Measures:** We look for a Markdown copy of the page, at the address the page advertises or at the page's address with .md added.
- **Why this matters:** A plain-text Markdown copy of a page has none of the navigation and markup a tool has to wade through to reach your words. [Cloudflare, Markdown for Agents](https://developers.cloudflare.com/changelog/post/2026-02-12-markdown-for-agents/): Cloudflare documents serving Markdown to agents that ask for it, from the network most sites sit behind.
- **Sources:** [Cloudflare, Markdown for Agents](https://developers.cloudflare.com/changelog/post/2026-02-12-markdown-for-agents/), 2026-02-12 (A); [Dries Buytaert, a month of Cloudflare logs](https://dri.es/markdown-llms-txt-and-ai-crawlers), 2026-03-05 (B)
- **Detect:** For each URL in the representation sub-sample, find the Markdown copy the page advertises (a `<link rel="alternate" type="text/markdown">` or a `Link` header) and request it; where the page advertises none, request `{path}.md`. Require a `200` with `text/markdown` or `text/plain`, content that materially matches the page body, and no navigation chrome.
- **Evidence kept:** Per URL: the address tried, how it was found, status, type and a body comparison.
- **Fix:** Generate from the same source as the HTML. Strip nav, promos and cookie banners.
- **What changed in 12.0:** Follows the address the page advertises, not only the page address plus .md. Points: 2, unchanged from 11.5.
- **Replaces:** AIR-7.1
- **Review by:** 2027-04-18

### RED-11 — Does each page tell machines where its Markdown copy is?

- **Question:** Does each page tell machines where its Markdown copy is?
- **Points:** 1
- **Applicability:** conditional — requires RED-10 ≥ 2
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Front-end developer
- **Evidence:** AI product
- **Measures:** We look for the Markdown link in the page's head and in the response headers.
- **Why this matters:** Publishing the Markdown copy is not enough: the page has to say where it is, or nothing will find it. [llms.txt specification v2 (Link relations)](https://llmstxt.org/): The specification defines how a page points to its Markdown copy, in the page and in a response header.
- **Sources:** [llms.txt specification v2 (Link relations)](https://llmstxt.org/), 2026-08-10 (A); [RFC 8288, Web Linking](https://www.rfc-editor.org/rfc/rfc8288), 2017 (A); [Dries Buytaert, a month of Cloudflare logs](https://dri.es/markdown-llms-txt-and-ai-crawlers), 2026-03-05 (B)
- **Detect:** Parse `<link rel="alternate" type="text/markdown">` from the head and the `Link` response header (RFC 8288) for the same relation. Either form counts. Resolve the address and confirm it is the copy RED-10 found.
- **Evidence kept:** Per URL: the head link and the header link found, and where each pointed.
- **Fix:** Add the link to the head template or send it as a response header. A file nobody can find is not much use.
- **What changed in 12.0:** Reads the response headers as well as the link in the page. Points: 2 in 11.5, 1 in 12.0.
- **Replaces:** AIR-7.2
- **Review by:** 2027-04-18

### RED-12 — If a machine asks for Markdown, does your site give it?

- **Question:** If a machine asks for Markdown, does your site give it?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Operations
- **Evidence:** AI product (coding agents)
- **Measures:** We send a request that asks for Markdown, check the answer, and check that caches keep the web and Markdown versions apart.
- **Why this matters:** A machine can ask the page's own address for Markdown and get it, with caches keeping the web and Markdown versions apart. [Cloudflare, Markdown for Agents (docs)](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/): Cloudflare documents the request and its cache behavior, and reports which coding agents send it.
- **Sources:** [Cloudflare, Markdown for Agents](https://developers.cloudflare.com/changelog/post/2026-02-12-markdown-for-agents/), 2026-02-12 (A); [Cloudflare, Markdown for Agents (docs)](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/), 2026-10-09 (A); [Cloudflare, cache and Vary](https://developers.cloudflare.com/cache/concepts/vary/), 2026-08-14 (A)
- **Detect:** Two halves. **Negotiation:** request sampled URLs with `Accept: text/markdown` and confirm the response type and that `Vary: Accept` is set. **Caching:** request through the CDN twice, once for each representation, and confirm the two variants are cached separately and that a browser is never served Markdown.
- **Evidence kept:** Per URL: response type, `Vary` header, cache-status headers and the variant returned to each request.
- **Bands:** the weakest half decides the band.
  - **4** — negotiation works, `Vary: Accept` is correct and the variants are cached separately.
  - **2** — negotiation works but `Vary` is missing or the variants share a cache entry, which risks serving Markdown to browsers.
  - **0** — not supported.
- **Note:** The evidence is for coding agents only: Cloudflare reports that they send the request, and one study of crawler logs saw no AI crawler do so. Getting `Vary` wrong is worse than not doing this at all. Verify at the edge.
- **Fix:** Serve Markdown on request from the canonical address, set `Vary: Accept`, and set TTLs and invalidation to the same cache tags as the source content.
- **What changed in 12.0:** Absorbs the caching test. Points: 4 in 11.5, 2 in 12.0.
- **Replaces:** AIR-7.3, AIR-7.4
- **Review by:** 2027-04-18

### RED-13 — Is the page built from real page parts, like header, main and navigation?

- **Question:** Is the page built from real page parts, like header, main and navigation?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer
- **Evidence:** Practice
- **Measures:** We check for real page-structure elements instead of one pile of unlabeled boxes.
- **Why this matters:** Real page parts such as header, main and navigation, instead of one pile of unlabeled boxes. It is good practice for people, and research suggests structure helps a model read a page. [HtmlRAG (research paper)](https://arxiv.org/abs/2411.02959): The paper tests whether keeping HTML structure helps a model answer from a page, and it is the only evidence we found for this test.
- **Sources:** [HtmlRAG (research paper)](https://arxiv.org/abs/2411.02959), 2024-11 (B); [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** Per page, require exactly one `<main>`, at least one `<article>` or `<section>` wrapping the primary content, and a `<nav>` for primary navigation. Compute a div-to-semantic-element ratio in the content region and flag pages above 12:1.
- **Evidence kept:** Per page: the landmarks found and the ratio computed.
- **Note:** Labeled Practice: sound practice for people and for assistive technology, and no AI company documents using it. It carries one point.
- **Fix:** Replace structural divs with `article`, `section`, `nav`, `aside`, `figure` and `dl`.
- **What changed in 12.0:** Weight cut; labeled Practice. Points: 2 in 11.5, 1 in 12.0.
- **Replaces:** AIR-1.8
- **Review by:** 2027-04-18

### RED-14 — Do your headings follow in order, starting from one main heading?

- **Question:** Do your headings follow in order, starting from one main heading?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Front-end developer, Content team
- **Evidence:** Practice
- **Measures:** We check for one main heading and headings that nest without skipping a level.
- **Why this matters:** One main heading, then sub-headings in order. A study found most pages ChatGPT cited used ordered headings; that shows association, not cause. [AirOps, ChatGPT content structure](https://www.airops.com/blog/chatgpt-content-structure): It is the study behind the claim, and it reports the association without claiming the headings caused the citations.
- **Sources:** [HtmlRAG (research paper)](https://arxiv.org/abs/2411.02959), 2024-11 (B); [AirOps, ChatGPT content structure](https://www.airops.com/blog/chatgpt-content-structure), 2025-12-29 (B)
- **Detect:** Count `h1` elements. Walk the heading tree and flag skipped levels, empty headings, and headings used purely for styling (no following content).
- **Evidence kept:** Per page: the heading outline and each flag raised.
- **Bands:** Default coverage rubric, where a page passes only if it has exactly one non-empty `h1` and no skipped levels.
- **Note:** Labeled Practice: sound practice for people and for assistive technology, and no AI company documents using it. It carries one point.
- **Fix:** Move the site name out of `h1`. Fix skips in the templates, not the content.
- **What changed in 12.0:** Weight cut; the claim is softened to a correlation. Points: 2 in 11.5, 1 in 12.0.
- **Replaces:** AIR-1.9
- **Review by:** 2027-04-18

### RED-15 — Are your tables real tables, with header cells?

- **Question:** Are your tables real tables, with header cells?
- **Points:** 1
- **Applicability:** conditional — the sample contains tables
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer, Content team
- **Evidence:** Practice
- **Measures:** We check that data tables use header cells and captions.
- **Why this matters:** Tuition, hours, fees and comparisons belong in a real table with header cells, not in an image or a grid of boxes. Research suggests real tables help a model read them. [HtmlRAG (research paper)](https://arxiv.org/abs/2411.02959): The paper is the research behind the claim; no company documents how its crawler treats header cells.
- **Sources:** [HtmlRAG (research paper)](https://arxiv.org/abs/2411.02959), 2024-11 (B)
- **Detect:** For each `<table>`, require `<th>` with `scope`, a `<caption>`, and `<thead>`/`<tbody>`. Separately flag layout tables (no `th`, presentational attributes, single row or column).
- **Evidence kept:** Per table: the header cells, caption and sections found, and whether it is a layout table.
- **Bands:** 4 — every data table complete, no layout tables. 3 — minor omissions such as missing captions. 2 — header cells present without scope. 1 — tables present with no header cells. 0 — layout tables carrying data.
- **Note:** Labeled Practice: sound practice for people and for assistive technology, and no AI company documents using it. It carries one point.
- **Fix:** Fix the tables that carry facts first. Convert layout tables to CSS.
- **What changed in 12.0:** Weight cut; labeled Practice. Points: 2 in 11.5, 1 in 12.0.
- **Replaces:** AIR-2.3
- **Review by:** 2027-04-18

### RED-16 — Does every section heading have a link that will not change?

- **Question:** Does every section heading have a link that will not change?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer
- **Evidence:** Practice
- **Measures:** We check that section headings have readable IDs, taken from the heading text, that a link can point to.
- **Why this matters:** A section heading with a stable ID can be linked to directly, so a person or a tool can return to the same passage. [Google, control your snippets](https://developers.google.com/search/docs/appearance/snippet): It is the nearest primary source: it describes how Search shows part of a page, and no AI product is documented citing by anchor.
- **Sources:** [Google, control your snippets](https://developers.google.com/search/docs/appearance/snippet), 2026-04-20 (A)
- **Detect:** For headings below `h1`, check for an `id`. Classify each as slug-like (derived from heading text) or generated (`section-3`, `block-a7f2c1`, framework hashes). One scan is enough: a generated ID is the sign of one that will change, and the scanner does not compare scans.
- **Evidence kept:** Per heading: the ID found and its class.
- **Bands:** 4 — ≥95% of subheadings carry slug-like IDs. 3 — 75–94%. 2 — IDs present but a majority are generated. 1 — sparse. 0 — none.
- **Note:** Labeled Practice: sound practice for people and for assistive technology, and no AI company documents using it. It carries one point. This is the weakest evidence in the category.
- **Fix:** Derive IDs from heading text, not render order.
- **What changed in 12.0:** The check that IDs stay the same across scans is dropped; it had no evidence. Points: 2 in 11.5, 1 in 12.0. The scanner reads one scan and does not compare IDs between runs.
- **Replaces:** AIR-2.4
- **Review by:** 2027-04-18

### RED-17 — Do your images have descriptions for people who cannot see them?

- **Question:** Do your images have descriptions for people who cannot see them?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Content team, Back-end developer
- **Evidence:** Practice
- **Measures:** We check that content images have useful alt text and decorative ones have none.
- **Why this matters:** Alt text is the only text an image has. Decorative images should say so with an empty alt rather than describing themselves. [W3C WAI, alt decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/): The W3C's own decision tree for when alt text is required and when an empty alt is correct.
- **Sources:** None recorded in the evidence register beyond the primary guidance cited under Why this matters: [W3C WAI, alt decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/), undated (A)
- **Detect:** For every `<img>`, record presence of `alt`, its length, and whether the image sits inside a content region or a decorative one. Flag missing `alt`, filename-as-alt, and long alt on obviously decorative images.
- **Evidence kept:** Per image: the alt found, its length, the region it sits in and the flag raised.
- **Note:** Labeled Practice: sound practice for people and for assistive technology, and no AI company documents using it. It carries one point.
- **Fix:** Audit existing content, then make the field required in the media entity so the problem stops recurring.
- **What changed in 12.0:** Labeled Practice. Points: 1, unchanged from 11.5.
- **Replaces:** AIR-2.5
- **Review by:** 2027-04-18

### RED-18 — Are your key facts written as text, not only inside images or PDFs?

- **Question:** Are your key facts written as text, not only inside images or PDFs?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** large
- **Fixed by:** Content team, Front-end developer
- **Evidence:** Practice
- **Measures:** We check that facts that matter, such as prices and dates, also appear as page text.
- **Why this matters:** A fact that exists only in a PDF, a scan or an infographic is harder to find and quote. It is not a hard barrier: at least one AI tool reads PDFs. [Anthropic, web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool): Anthropic documents that its tool reads PDFs, which is why this test says harder and not impossible.
- **Sources:** [Anthropic, web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool), current (A)
- **Detect:** Identify pages whose visible text is thin relative to their images, or that link to a PDF as the primary content. Extract PDF text and look for numbers, dates and prices that appear nowhere in the site's HTML. Requires review before scoring.
- **Evidence kept:** Per page: the facts found only in a binary and the file they came from.
- **Bands:** 4 — no high-value facts found only in binaries. 2 — some found only in PDFs. 0 — core facts (tuition, hours, deadlines, contact) exist only in binaries.
- **Note:** Labeled Practice: sound practice for people and for assistive technology, and no AI company documents using it. It carries one point.
- **Fix:** Publish an HTML equivalent. Keep the PDF as a download, not as the source of truth.
- **What changed in 12.0:** Reworded to 'harder to find and quote'. Anthropic's tool does read PDFs. Points: 1, unchanged from 11.5.
- **Replaces:** AIR-2.6
- **Review by:** 2027-04-18

### RED-19 — Does each page give its answer near the top?

- **Question:** Does each page give its answer near the top?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Content team, Front-end developer
- **Evidence:** Practice
- **Measures:** Whether each page opens with a full sentence of its answer, and not a title, a date or a navigation prompt.
- **Why this matters:** A page that states its answer in the first sentences is easier to quote. Bing's guidelines advise it, and one study found 44% of ChatGPT citations came from the first 30% of a page. [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a): Bing publishes the guidance in its own words; the study is correlation, so the test carries one point.
- **Sources:** Bing Webmaster Guidelines (address to confirm), undated (A); a study of which part of a page ChatGPT cites, reported as 44% from the first 30% (reference to confirm) (B)
- **Detect:** For each sampled page with main text, look at the first 500 characters of the main text, paragraph by paragraph, and ask whether one paragraph holds a full sentence of eight or more words, as opposed to a title, a date, a byline or a navigation prompt. A page passes when it does. This is a proxy for "the answer is near the top", not a reading of whether the sentence answers anything.
- **Evidence kept:** Per page: the opening 200 characters and whether a full sentence was found.
- **Bands:** Default coverage rubric.
- **Note:** Provisional. The scanner reads the first paragraphs of the main text, so a title, a date and a navigation prompt never add up to a sentence, and reports medium confidence because eight words is a proxy for an answer. It is the test most likely to be reworked or dropped after the pilot. If it is dropped, its point moves to RED-1.
- **Fix:** Start each page with the answer, in a sentence or two. Put what the page is about, in plain sentences, before the navigation prompts, the long introduction and the fine print.
- **What changed in 12.0:** New in 12.0, at one point. It has no v11 predecessor.
- **Review by:** 2027-04-18

## #3 · Understand · 11 tests · 25 pts

**Points 25**

Understand asks whether a machine knows what a page and a site are: who published it, who wrote it, when, what it sells, and where it sits. Its evidence is documented for Google and Bing more often than for AI products.

### UND-1 — Does your site say clearly who you are?

- **Question:** Does your site say clearly who you are?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Content team, Site owner
- **Evidence:** Search index
- **Measures:** We look for your name, address, contact details and public identifiers, such as a company or registry number, on your About page and in your page code.
- **Why this matters:** Your name, address, contact details and public identifiers, on an About page and in your page code, so a machine can tell which organization you are. [Google, Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization): Google documents using these identifiers to tell organizations apart.
- **Sources:** [Google, Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization), 2026-09-08 (A)
- **Detect:** Locate About and Contact pages. Score presence of: organization name, founding date, leadership names, postal address, service area, `contactPoint` entries differentiated by purpose, and public legal identifiers (EIN, ROR, DUNS, company or registry number). Check both the visible page and the `Organization` node.
- **Evidence kept:** Per fact: whether it appears in the visible page, in the `Organization` node, or both.
- **Bands:** fraction of those seven facts present in both HTML and markup: 4 — ≥6. 3 — 5. 2 — 3–4. 1 — 1–2. 0 — none.
- **Note:** This release reads the `Organization` node. Whether each fact also appears in the visible page is not yet compared, so a fact counts when the markup carries it.
- **Fix:** Thin About pages are a persistent weakness for nonprofits and institutions. Do not leave the key facts in an annual-report PDF.
- **What changed in 12.0:** Cites Google's Organization documentation. Points: 2, unchanged from 11.5. The list of facts now names all seven the bands count; 11.5 listed six and banded on seven.
- **Replaces:** AIR-1.13
- **Review by:** 2027-04-18

### UND-2 — Does your site use the page labels that search engines still read for what you publish?

- **Question:** Does your site use the page labels that search engines still read for what you publish?
- **Points:** 3
- **Applicability:** vertical — scored against the client's declared vertical only
- **Verification:** auto
- **Effort:** large
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** Search index
- **Measures:** We check that you use the structured-data labels that fit your kind of site (for example local business, jobs, courses) and that Google still supports them.
- **Why this matters:** Use the markup types that match what you publish, such as local business, jobs or courses, and that search engines still read. [Google Search updates log (retirements)](https://developers.google.com/search/updates): Google's log shows which structured-data types it has retired, so each type is checked against what is still live.
- **Sources:** [Google Search updates log (retirements)](https://developers.google.com/search/updates), current (A); [Google, Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization), 2026-09-08 (A)
- **Detect:** From the declared vertical, load the expected type set and check coverage against matching content types. A type that Google has retired from Search is dropped from the expected set before the fraction is taken, and the retired types dropped are recorded in the evidence. The retired-type list is kept with the scanner, dated, and reviewed every six months. The sets are:
  - **Ecommerce:** `Product`, `Offer`, `AggregateRating`, `BreadcrumbList`
  - **Financial Services:** `FinancialService`, `BankOrCreditUnion`, `LoanOrCredit`, `InvestmentOrDeposit`
  - **Government:** `GovernmentOrganization`, `GovernmentService`, `Legislation`
  - **Healthcare:** `MedicalOrganization`, `Physician`, `MedicalCondition`, `MedicalWebPage`
  - **Higher Education:** `Course`, `EducationalOccupationalProgram`, `CollegeOrUniversity`, `EducationEvent`
  - **Hospitality:** `LodgingBusiness`, `Restaurant`, `Reservation`, `Menu`
  - **K-12 Education:** `EducationalOrganization`, `School`, `Event`, `EducationEvent`, `Course`
  - **Local Services:** `LocalBusiness`, `Service`, `OpeningHoursSpecification`, `GeoCoordinates`
  - **Manufacturing:** `Organization`, `Product`, `ProductModel`, `Brand`
  - **Media:** `NewsArticle`, `VideoObject`, `Person`, `ImageObject`
  - **Nonprofit:** `NGO`, `DonateAction`, `Grant`, `FundingScheme`
  - **Professional Services:** `ProfessionalService`, `Service`, `Person`, `Review`
  - **Real Estate:** `RealEstateListing`, `Residence`, `Place`, `GeoCoordinates`
  - **Research:** `Dataset`, `DataCatalog`, `ScholarlyArticle`
  - **SaaS:** `SoftwareApplication`, `Offer`, `Organization`
  - **Other:** no expected set. The test is **not scored** and says so on the report.
- **Evidence kept:** The declared vertical, the expected set, the retired types dropped, and the types found.
- **Bands:** fraction of expected types present and valid on the content that warrants them: 4 — ≥90%. 3 — 70–89%. 2 — 40–69%. 1 — 1–39%. 0 — none.
- **Note:** `Dataset` and `DataCatalog` are badly underused. Research organizations routinely hold cataloged data with no machine-readable description at all. The retired-type list is provisional until the register's sources are verified. `FAQPage` is no longer in any set: Google ended the FAQ result in 2026.
- **Fix:** Pick the applicable set deliberately. Do not implement types the content does not support.
- **What changed in 12.0:** Re-scoped to types Google still supports; retired types no longer count. Points: 4 in 11.5, 3 in 12.0.
- **Replaces:** AIR-3.3
- **Review by:** 2027-04-18

### UND-3 — Do the prices and availability in your page code match what the page shows?

- **Question:** Do the prices and availability in your page code match what the page shows?
- **Points:** 3
- **Applicability:** conditional — the site sells, charges or offers something
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Content team
- **Evidence:** Search index
- **Measures:** If you sell products, we compare the prices and stock in your page code with the prices and stock shown on the page. We cannot see a private merchant feed, so we check the page against itself.
- **Why this matters:** If you sell something, the price and availability in your page code should match what the page shows. A mismatch is read as an error. [Google, Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product): Google asks that product markup describe what a person can see on the page.
- **Sources:** [Google, Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product), 2025-12-10 (A); [Microsoft Ads, agentic commerce (merchant feed)](https://about.ads.microsoft.com/en/solutions/technology/agentic-commerce), undated (A); [OpenAI, product feed spec](https://developers.openai.com/commerce/specs/feed), undated (A)
- **Detect:** Validate `Offer` structure. Compare `price`, `priceCurrency` and `availability` against the visible page. Flag any mismatch and any `priceValidUntil` in the past.
- **Evidence kept:** Per page: the marked-up values, the visible values and the mismatch found.
- **Bands:** 4 — accurate and matching the page. 2 — present but drifting from visible values: a price that cannot be found on the page to compare, a missing currency, a `priceValidUntil` in the past, or a contradiction on a minority of offers. 0 — absent, or contradicting the page on more than half of the priced offers (a marked-up price the page does not show, or availability the page says the opposite of).
- **Note:** AI shopping tools take their data from merchant feeds, which a scan cannot see. The test therefore checks the page against itself and says nothing about whether a price is current or matches a feed.
- **Fix:** Source the markup value from the same field the page renders.
- **What changed in 12.0:** Compares the markup with the visible page. A private merchant feed cannot be seen from outside, so the v11 'current price' claim and any feed comparison are dropped. Points: 1 in 11.5, 3 in 12.0.
- **Replaces:** AIR-3.6
- **Review by:** 2027-04-18

### UND-4 — Does each article show who wrote it, with a page about the author?

- **Question:** Does each article show who wrote it, with a page about the author?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Content team, Back-end developer
- **Evidence:** Search index
- **Measures:** We check that articles name their author and that the name leads to a page or profile a machine can find.
- **Why this matters:** An article should show who wrote it, and the name should lead to a page or profile about that person. [Google, Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article): Google asks for a visible author with a link or profile, and it does not ask for credentials.
- **Sources:** [Google, Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article), 2026-09-08 (A); [Google, creating helpful, reliable content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), 2026-10-05 (A)
- **Detect:** On sampled article pages, check for a visible byline and an author name that leads to a page or profile a machine can find (an author `url`, a `sameAs`, or a link to an author page that returns `200`). Count each distinct author once, however many articles they signed. Record credentials (`jobTitle`, `affiliation`, `knowsAbout`, `sameAs`) as a bonus: they are shown and credited in words and never lower the band. If the sample holds no article pages, there is nothing to find and the test scores 4.
- **Evidence kept:** Per distinct author: the pages they signed, the page or profile found and any credentials.
- **Bands:** fraction of distinct authors with a findable page or profile: 4 — ≥95%. 3 — 75–94%. 2 — 40–74%. 1 — author names only, or fewer than 40%. 0 — no named authors.
- **Note:** An article page is one that carries an article type in its markup or shows a byline. A byline is recognized by the usual markup (`rel="author"`, `itemprop="author"`, a class that names a byline or author) and by a line that begins "By". An author page counts as findable when the markup or the byline links to it; this release does not fetch the linked page to confirm it returns `200`, and says so in its confidence.
- **Fix:** A byline string asserts nothing. A page about the person does.
- **What changed in 12.0:** Counts each author once. Credentials become a bonus, not a requirement. Points: 2, unchanged from 11.5.
- **Replaces:** AIR-5.1
- **Review by:** 2027-04-18

### UND-5 — Does the author label in your page code point to that person?

- **Question:** Does the author label in your page code point to that person?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Content team
- **Evidence:** Search index
- **Measures:** We check that the author in your page code is a real reference to the person, not just a repeated name.
- **Why this matters:** The author label in your page code should point to the person, not repeat their name as text on every article. [Google, Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article): Google identifies an author from a link or profile in the markup.
- **Sources:** [Google, Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article), 2026-09-08 (A)
- **Detect:** For each substantive page, read the `author` property. A page passes when a byline is visible (a recognized byline, or the author's name in the page text) and the `author` is an `@id` reference to a node, or a `Person` with a `url` or `sameAs`. A bare string fails.
- **Evidence kept:** Per page: the `author` value and whether it is a reference.
- **Bands:** 4 — visible byline plus a reference on ≥95%. 3 — 75–94%. 2 — `author` present as a bare string. 1 — sparse. 0 — unsigned.
- **Fix:** Where the author is a department, name the department and model it as an entity.
- **What changed in 12.0:** Accepts a link or profile as well as an ID. Points: 2 in 11.5, 1 in 12.0.
- **Replaces:** AIR-5.2
- **Review by:** 2027-04-18

### UND-6 — Are your published and updated dates honest and visible?

- **Question:** Are your published and updated dates honest and visible?
- **Points:** 6
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** medium
- **Fixed by:** Back-end developer, Content team
- **Evidence:** AI product
- **Measures:** We check that the dates in your page code match the dates readers see and that they change only when the content does.
- **Why this matters:** Published and updated dates should be visible to readers, match your page code, and move only when the content does. A date that changes on every deploy is noise. [Google, publication dates](https://developers.google.com/search/docs/appearance/publication-dates): Google says it uses several date signals and wants visible dates that match.
- **Sources:** [Google, publication dates](https://developers.google.com/search/docs/appearance/publication-dates), current (A); [Ahrefs, do AI assistants prefer fresh content](https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/), 2025-07-28 (B); [Bing Webmaster Blog, sitemaps in AI-powered search](https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search), 2025-07-31 (A)
- **Detect:** Extract both dates from markup and from visible text (`<time>` elements and bylines). Flag: missing dates, `dateModified` before `datePublished`, future dates, a date in the markup that differs from the date shown, and clustering that suggests a deploy stamp. Compare against sitemap `lastmod` (RED-3) and against the previous audit run to confirm dates only move when content moves.
- **Evidence kept:** Per page: the marked-up and visible dates, and each flag raised.
- **Bands:** 4 — dates present, visible, matching and consistent, and stable across a deploy with no content change. 3 — the same, stability unconfirmed. 2 — present but clustered, contradicting the sitemap, or differing from the visible date. 1 — one date only, or none visible. 0 — absent.
- **First run:** cap at 3 without a baseline run. See *Tests that need a previous run*.
- **Fix:** Wire both dates to the node's own timestamps and show them on the page. A deploy must not move them.
- **What changed in 12.0:** Citation moves to Google's publication-dates page. Points: 2 in 11.5, 6 in 12.0.
- **Replaces:** AIR-5.4
- **Review by:** 2027-04-18

### UND-7 — Does each page show where it sits in your site?

- **Question:** Does each page show where it sits in your site?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer
- **Evidence:** Search index
- **Measures:** Where your site has sections, we check for a breadcrumb trail that makes sense.
- **Why this matters:** Where your site has sections, each page should show where it sits, so a model knows a program page belongs to a department. [Google, breadcrumb structured data](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb): Google sets no depth rule and says a trail should follow how people move through the site.
- **Sources:** [Google, breadcrumb structured data](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb), 2026-09-08 (A)
- **Detect:** Decide whether the site has a hierarchy: pages below the first level of navigation. Where it does, validate `BreadcrumbList` on pages below the homepage and require at least two steps. A trail need not match the URL path. Where the site is flat, there is nothing to find and the test scores 4.
- **Evidence kept:** Per page: the trail found and its step count.
- **Bands:** Default coverage rubric over pages that sit inside a section.
- **Fix:** Generate from the menu, not by hand.
- **What changed in 12.0:** Required only where your site has sections. A trail need not match the address. Points: 2 in 11.5, 1 in 12.0.
- **Replaces:** AIR-3.2
- **Review by:** 2027-04-18

### UND-8 — Does your hidden page code say the same thing as the visible text?

- **Question:** Does your hidden page code say the same thing as the visible text?
- **Points:** 1
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Front-end developer
- **Evidence:** Search index
- **Measures:** Whether the headline and name in a page's structured data appear in the visible page.
- **Why this matters:** The headline and name in your page code should be the ones on the page. Markup that says something else is ignored at best, and misleading at worst. [Google, structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies): Google states that markup must describe content people can see.
- **Sources:** [Google, structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies), current (A)
- **Detect:** For each sampled page, take the `headline` or `name` of each non-site entity in its JSON-LD (the `Organization`, `WebSite`, `WebPage`, `Person` and similar nodes are the site's, not the page's, and are skipped). Normalize it and look for it in the visible title, the headings and the opening text. A page passes when every marked-up title is found. A site with no page carrying such a field has nothing to compare and the test scores 4.
- **Evidence kept:** Per page: the marked-up titles and whether each appears on the page.
- **Bands:** Default coverage rubric over pages that carry a headline or name in markup.
- **Note:** It compares against the page title, the headings and the first 6,000 characters of main text, so a title that appears only far down a very long page can still be missed. A title written as "Page | Site" counts when its longer part is on the page. It reports medium confidence.
- **Fix:** Generate the markup and the page from the same field.
- **What changed in 12.0:** New in 12.0, at one point. It has no v11 predecessor.
- **Review by:** 2027-04-18

### UND-9 — If a page is behind a paywall, does it say so?

- **Question:** If a page is behind a paywall, does it say so?
- **Points:** 2
- **Applicability:** conditional — the site has a paywall
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Content team
- **Evidence:** AI product
- **Measures:** If you have paywalled pages, we check that they are marked as not free, so they are not mistaken for hidden content.
- **Why this matters:** If a page is behind a paywall, say so in its markup, so it is not mistaken for hidden content shown to a crawler and kept from people. [Google, paywalled content](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content): Google documents the markup, and Apple documents it for Applebot.
- **Sources:** [Google, paywalled content](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content), 2026-09-08 (A); [Apple, About Applebot](https://support.apple.com/en-us/119829), 2026-09-04 (A)
- **Detect:** Look for signs of a paywall: known paywall scripts and class names, metered or 'subscribe to read' prompts, a body cut short with a subscription prompt, and `isAccessibleForFree` already in the markup. Accept an owner statement that the site has one. On pages that show a paywall, check that the markup says `isAccessibleForFree: false` and names the gated part with `hasPart` and a `cssSelector`. The site has a paywall when a page says so in its markup, when a page shows one, or when the owner declares one in the engagement profile; a site with none has nothing to find and the test scores 4. Where the owner declares one and no sampled page shows it, the sample cannot be judged and the test is held at 2.
- **Evidence kept:** Per page: the paywall signs found and the markup present.
- **Bands:** Default coverage rubric over pages that show a paywall.
- **Note:** Whether a paywall exists is the one fact a crawler cannot always see. The detector is provisional (a paywall vendor's script or class, or subscription wording on the page), and the owner's statement settles the doubt. Naming the gated part with `hasPart` and a `cssSelector` is advised and shown in the evidence; a page passes on `isAccessibleForFree: false` alone. The `about` and `mentions` properties are no longer checked: no consumer is documented.
- **Fix:** Add `isAccessibleForFree: false` and the gated section's selector to every paywalled page.
- **What changed in 12.0:** Apple documents it. The 'about' and 'mentions' part is dropped. Points: 1 in 11.5, 2 in 12.0.
- **Replaces:** AIR-3.5
- **Review by:** 2027-04-18

### UND-10 — Does your page code link to your official profiles elsewhere?

- **Question:** Does your page code link to your official profiles elsewhere?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Search specialist, Back-end developer
- **Evidence:** Search index
- **Measures:** We look for links to profiles such as Wikidata and LinkedIn in your organization's page code.
- **Why this matters:** Links from your organization's page code to your official profiles, such as Wikidata and LinkedIn. [Google, Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization): Google lists `sameAs` as a recommended property of Organization markup, which is a documented reader.
- **Sources:** [Google, Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization), 2026-09-08 (A)
- **Detect:** Extract `sameAs` from `Organization` and `Person` nodes. Classify each URL by authority: tier 1 (Wikidata, ROR, NPI, IRS EIN, ORCID), tier 2 (Wikipedia, Crunchbase, LinkedIn, Candid), tier 3 (social profiles). Where the links can be fetched, resolve each URL and confirm it returns `200` and references the organization back where possible, under *Resolving external identifiers*. A scan that does not fetch them grades the links as published.
- **Evidence kept:** Each link, its tier, whether it was resolved and what came back, and the external hosts contacted.
- **Bands:** 4 — a tier-1 identifier among three or more links, none known to be dead. The links need not have been fetched. 3 — a tier-1 identifier with fewer than three links, or a link known to be dead. 2 — tier-2 links and no tier-1. 1 — social profiles only. 0 — no `sameAs`.
- **Note:** Band 4 does not wait for the links to be fetched. Those hosts are often outside the client's allowlist, and a permanent ceiling at band 3 would have taken points from every site however good, which a scored test must not do. When the links were not fetched, the confidence is medium and the summary says so. A scan that did fetch them still lowers the band for a link that is dead.
- **Fix:** Claim the Wikidata item. For universities, ROR is free and takes a day.
- **What changed in 12.0:** It was unscored in the first 12.0 draft and moved into the score as an Understand test, at 2 points, because Google documents `sameAs` as a recommended Organization property. It carried 2 points in 11.5 as AIR-1.12. Band 4 no longer needs the links fetched.
- **Replaces:** AIR-1.12
- **Review by:** 2027-04-18


### UND-11 — Does your page code pass a validity check?

- **Question:** Does your page code pass a validity check?
- **Points:** 2
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** Search index
- **Measures:** We run your structured data through a validator.
- **Why this matters:** Markup that does not parse, or that leaves out what its type needs, is served to machines that cannot use it, and nothing on the page says so. [Google, structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies): Google says markup that is invalid or breaks its guidelines is not eligible to appear as a rich result.
- **Sources:** [Google, structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies), current (A)
- **Detect:** Parse every JSON-LD, microdata and RDFa block on every sampled page. A block that does not parse is a failure of the page it is on. For each node, check the properties a consumer needs for the type it declares, and check that dates are ISO 8601, that URLs are absolute, and that a price carries a currency.
- **Evidence kept:** Per block: whether it parsed and each property or value found wrong.
- **Bands:** 4 — every block parses, every node carries what its type requires, every value is well formed. 3 — everything parses and one property or value is wrong somewhere. 2 — everything parses; required properties are missing on some nodes. 0 — a block on a sampled page does not parse.
- **Note:** A site with no markup at all has nothing to validate, so the test is not judged there: it is not applicable and carries no points either way. Invalid markup is ignored by parsers, so a block that does not parse is band 0. Validate what you publish rather than trusting it was right when it was written.
- **Fix:** Validate in the build and fix what the validator reports.
- **What changed in 12.0:** It was unscored in the first 12.0 draft and moved into the score as an Understand test, at 2 points, because Google documents that invalid markup is not eligible for its features. It carried 2 points in 11.5 as AIR-3.8.
- **Replaces:** AIR-3.8
- **Review by:** 2027-04-18

## #4 · Act · 4 tests · 15 pts

**Points 15**

Act asks whether an agent can do something on the site. The evidence is real and narrow: browser agents read page structure, name what they click, and stop at CAPTCHAs.

### ACT-1 — Can an AI agent tell what each form field is for?

- **Question:** Can an AI agent tell what each form field is for?
- **Points:** 5
- **Applicability:** conditional — the site has public forms
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer, Content team
- **Evidence:** AI product
- **Measures:** We check that form fields have names and labels, which is how agents that read the page structure find them.
- **Why this matters:** An agent filling in your form has to know what each field is for. Labels and names are how it finds out. [Anthropic, browser use tool (accessibility tree)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool): Anthropic documents that its browser tool reads the page's accessibility tree, which is where field names and labels live.
- **Sources:** [Anthropic, browser use tool (accessibility tree)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool), current (A); [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** For every public form field: a `<label for>` or equivalent accessible name, and a meaningful `name` attribute (reject `field_1`, `input3`).
- **Evidence kept:** Per field: the label and name found and whether each passed.
- **Bands:** fraction of fields passing both: 4 — ≥95%. 3 — 75–94%. 2 — 40–74%. 1 — 1–39%. 0 — none.
- **Note:** `autocomplete` tokens are no longer checked: no source shows an agent reading them.
- **Fix:** The same change satisfies WCAG. Easy joint justification.
- **What changed in 12.0:** Autocomplete is dropped; no source shows agents use it. Points: 2 in 11.5, 5 in 12.0.
- **Replaces:** AIR-6.3
- **Review by:** 2027-04-18

### ACT-2 — Can an AI agent browse and search without hitting a CAPTCHA?

- **Question:** Can an AI agent browse and search without hitting a CAPTCHA?
- **Points:** 3
- **Applicability:** conditional — the site has search or filtering
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Operations, Front-end developer
- **Evidence:** AI product
- **Measures:** We check that browsing, searching and filtering do not put a CAPTCHA in front of the visitor.
- **Why this matters:** Challenge the actions that need challenging. Browsing, searching and filtering are not those actions, and a CAPTCHA there ends an agent's visit. [Open CaptchaWorld (benchmark paper)](https://arxiv.org/abs/2505.24878): The benchmark measures how often web agents fail CAPTCHAs, which is the failure this test looks for.
- **Sources:** OpenAI, Operator (hands off captchas) (address to confirm), 2025-01 (B); [Open CaptchaWorld (benchmark paper)](https://arxiv.org/abs/2505.24878), 2025 (B)
- **Detect:** Submit search and filter forms and browse listings, and check for a CAPTCHA or challenge response in the way. Complements the challenge half of RCH-2 from the application side rather than the edge.
- **Evidence kept:** Per interaction: the request made and the challenge signature found, if any.
- **Bands:** Default coverage rubric over the browse, search and filter interactions tried. A site with search or filtering in which none could be tried is not judged: the test is N/A with the reason insufficient evidence, and a client report holds it at band 2.
- **Fix:** Scope challenges to form submissions and logins. Searching and filtering do not need one.
- **What changed in 12.0:** Detection and bands unchanged. Points: 2 in 11.5, 3 in 12.0. The test now applies only where the site has search or filtering. In the Index 12 pilot 113 of 180 sites had no search or filter surface in the sample and each had been given full marks for it, which made this the cheapest three points in the Index; a client report still shows band 4, "nothing to fix", for a site with none, and the census leaves the test out of the sites it does not apply to. A site that has search or filtering that the scan could not try is held at band 2.
- **Replaces:** AIR-6.4
- **Review by:** 2027-04-18

### ACT-3 — If you have a public API, is it described in a standard file?

- **Question:** If you have a public API, is it described in a standard file?
- **Points:** 2
- **Applicability:** conditional — the site has a public or semi-public API
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer
- **Evidence:** AI product (narrow)
- **Measures:** If you offer an API, we look for an OpenAPI description of it.
- **Why this matters:** If you have a public API, describe it in a standard file an agent or a tool can read. [OpenAI, GPT Actions (OpenAPI input; being retired)](https://help.openai.com/en/articles/9442513-gpt-actions): OpenAI documents OpenAPI as the input for GPT Actions, one of the few documented consumers of the file.
- **Sources:** [OpenAI, GPT Actions (OpenAPI input; being retired)](https://help.openai.com/en/articles/9442513-gpt-actions), current (B)
- **Detect:** Look for an OpenAPI description at the conventional paths (`/openapi.json`, `/openapi.yaml`, `/swagger.json`). Read it: it is valid when it carries the version marker, `info` with a title and a version, and `paths` (or `webhooks` or `components`). It counts as linked when a `service-desc` or `service-doc` link, in the page head or a `Link` header, points to it. The site has a public API when a published description, an API catalog, an `/api` or `/developers` page, a `service-desc` link or a JSON response shows one; if none is found, there is nothing to find and the test scores 4.
- **Evidence kept:** The description found, its validity and version, and where it is linked from.
- **Bands:** 4 — valid, versioned and linked from the site. 2 — present but invalid, or not linked. 0 — a public API and no description.
- **Note:** The evidence is narrow: GPT Actions are being retired, and the other documented consumers are tools that turn the file into agent tools.
- **Fix:** Publish the OpenAPI description, version it, and link it from the developer pages.
- **What changed in 12.0:** Applies only if you have a public API. Points: 2, unchanged from 11.5.
- **Replaces:** AIR-6.1
- **Review by:** 2027-04-18

### ACT-4 — Do your buttons, links and menus have names an AI agent can read?

- **Question:** Do your buttons, links and menus have names an AI agent can read?
- **Points:** 5
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer, Content team
- **Evidence:** AI product
- **Measures:** We count the buttons, links and menu controls on each page we read and check how many have no name an agent could read, such as an icon with no label.
- **Why this matters:** An agent that clicks through your site finds each control by its name, and a control with no name is one it cannot choose. [Anthropic, browser use tool (accessibility tree)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool): Anthropic documents that its browser tool reads the page's accessibility tree, which is where the name of every button, link and menu item lives.
- **Sources:** [Anthropic, browser use tool (accessibility tree)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool), current (A); OpenAI's guidance on ARIA labels for ChatGPT Atlas, reported by Adrian Roselli (address to confirm: OpenAI's own page was not opened), undated (C)
- **Detect:** On each sampled page, collect the controls that are not hidden: `<button>`, links with an `href`, `<summary>`, elements with `role="button"`, `link`, `menuitem` or `tab`, and button inputs. A control has a name when it has an `aria-label`, an `aria-labelledby` that points to text, text of its own, an image with `alt` text or an `svg` with a title or `aria-label` inside it, a `title` attribute, a button input's `value`, or an image input's `alt`. A page passes when at most 1% of its controls have no name.
- **Evidence kept:** Per page: the number of controls, the number with no name, and the first few of them by tag and position.
- **Bands:** Default coverage rubric over the pages measured, where a page counts as present and correct when at most 1% of its controls have no name. A site where no page's controls could be measured is not judged: the test is N/A with the reason insufficient evidence.
- **Fix:** Give an icon-only button or link an `aria-label` or visible text, and give each menu control the name its heading or label already carries. The same change satisfies WCAG, which makes it an easy joint justification.
- **What changed in 12.0:** New test. Added after the first draft, because Act had three tests and carried five points, and forms and CAPTCHAs were all it measured. Points: 5 in 12.0. A page passes at 1% unnamed controls and not 5%: the Index 12 pilot (180 S&P 500 sites) gave 121 of 166 sites full marks at 5% and 74 at 1%, with the bands spread from 0 to 4.
- **Review by:** 2027-04-18

## Coverage of published scanners

Two scanners publish lists of what makes a site ready for agents: Cloudflare's Agent Readiness score and the Agentic Browsing category of Google's Lighthouse. Index 12 measures every check on both lists, as they stood on 2026-10-18, and says how completely. A scanner measures; it is not a reader, so nothing here carries points. A check that an AI product or search engine is documented using is scored on that evidence, wherever it appears, and the rest are shown with the label **Scanner-listed**.

| Scanner | Their check | Our test | Coverage |
|---|---|---|---|
| Cloudflare | robots.txt | RCH-1, PST-1 | Covered. Read as rules for nine named search crawlers, not only as a file that exists. |
| Cloudflare | sitemap.xml | EXT-19 | Covered. RED-3 judges its dates and RED-8 its media sitemaps. |
| Cloudflare | Link response headers | RED-11, EXT-2, ACT-3 | Covered. One test per relation the headers carry. |
| Cloudflare | DNS for AI Discovery (DNS-AID) | EXT-17 | Covered. An SVCB lookup at _index._agents; an IETF draft that had expired at its last revision. |
| Cloudflare | Markdown content negotiation | RED-12, RED-10, RED-11 | Covered. Also checks Vary and CDN caching. |
| Cloudflare | llms.txt | EXT-1 | Covered. Cloudflare leaves it off by default. |
| Cloudflare | AI bot rules in robots.txt | RCH-1, PST-1 | Covered |
| Cloudflare | Content Signals | PST-2 | Covered |
| Cloudflare | Web Bot Auth | EXT-3 | Covered |
| Cloudflare | API Catalog (RFC 9727) | EXT-2, ACT-3 | Covered |
| Cloudflare | OAuth server discovery (RFC 8414) | EXT-15 | Covered |
| Cloudflare | OAuth Protected Resource (RFC 9728) | EXT-15 | Covered |
| Cloudflare | Auth.md | EXT-15 | Covered. Its publisher and a second source disagree on the address, so both are probed. |
| Cloudflare | MCP Server Card | EXT-4 | Covered. Also calls a live tool. |
| Cloudflare | A2A Agent Card | EXT-16 | Covered. Both /.well-known/agent-card.json and the older agent.json. |
| Cloudflare | Agent Skills index | EXT-16 | Covered |
| Cloudflare | WebMCP | EXT-14 | Covered |
| Cloudflare | ARD manifest | EXT-2 | Covered. Agentic Resource Discovery's manifest is the AI Catalog at /.well-known/ai-catalog.json. |
| Cloudflare | Personal Agent Protocol | none | Not covered. One vendor's protocol, and no published specification could be found to write a check from. |
| Cloudflare | Universal Commerce Protocol | EXT-18 | Covered |
| Cloudflare | x402 | EXT-18 | Partly covered. Shows only on a page that answers HTTP 402, so a shop that has it behind a paid address we did not sample is not seen. |
| Cloudflare | Machine Payments Protocol (MPP) | EXT-18 | Partly covered. The same limit as x402. |
| Cloudflare | Agentic Commerce Protocol | EXT-18 | Not observable from outside. No merchant discovery address could be confirmed, so there is nothing to probe. |
| Lighthouse | Registered WebMCP tools | EXT-14 | Covered |
| Lighthouse | Forms missing declarative WebMCP | EXT-14 | Partly covered. Counts the forms that declare themselves; does not flag one that has not. |
| Lighthouse | WebMCP schema validity | EXT-14 | Partly covered. Records whether a tool has an input schema; does not validate it. |
| Lighthouse | llms.txt | EXT-1 | Covered. Lighthouse treats a missing file as not applicable, as the Index leaves it unscored. |
| Lighthouse | Agentic Resource Discovery (13.5) | EXT-2 | Covered. The same AI Catalog as the ARD manifest above. |
| Lighthouse | Accessibility for agents: names and labels | ACT-4, ACT-1 | Covered |
| Lighthouse | Accessibility for agents: tree integrity and visibility | EXT-20 | Covered |
| Lighthouse | Layout stability (CLS) | MSR-8 | Covered. A lab reading from one load, shown and never scored. |

Counts: 25 covered, 1 not covered, 4 partly covered, 1 not observable from outside. The table is maintained by the scanner's authors and is dated. A scanner that adds a check is a reason to add a row.

## Posture · 6 items · not scored

Posture is your choices. Which training crawlers you allow, whether you declare a position, what you license and whether you have reserved your rights are yours to decide, and a choice is not a defect. Each item is shown in every report and never lowers a score. Where the items can contradict each other, PST-5 says so.

### PST-1 — Which AI training crawlers have you allowed or blocked?

- **Question:** Which AI training crawlers have you allowed or blocked?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Site owner, Search specialist
- **Evidence:** AI product
- **Measures:** We read your robots.txt for the crawlers that collect data to train AI models and show your choices. A choice is not a defect, so it never lowers your score. For xAI's Grok we show whether your robots.txt names GrokBot, xAI-Grok, Grok-DeepSearch or xAI-SearchBot. xAI publishes no crawler documentation and no list of its addresses, so we cannot say whether these names are honored or whether a visitor using them is really xAI. We show the names, say that, and never score it.
- **Why this matters:** Which AI training crawlers you allow or block is your choice, so it is shown and never scored. [OpenAI, crawler overview](https://developers.openai.com/api/docs/bots): OpenAI names its training crawler separately from its search crawler there.
- **Sources:** [OpenAI, crawler overview](https://developers.openai.com/api/docs/bots), undated (A); [Anthropic Help Center, crawler controls](https://support.claude.com/en/articles/8896518), 2026-04-07 (A); [Google, common crawlers (Google-Extended)](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers), 2026-07-14 (A); [Apple, About Applebot](https://support.apple.com/en-us/119829), 2026-09-04 (A); [Google, user-triggered fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers), 2026-08-19 (A); [Known Agents and Botcrawl directories (xAI crawler names; third-party, xAI publishes none)](https://botcrawl.com/bots/grokbot), 2026 (C); [StackFox, test of Grok's user agent (single blog, unverified)](https://stackfox.co/research/grok-user-agent), 2026-02 (C)
- **Detect:** Parse `robots.txt` and evaluate the training crawlers (`GPTBot`, `ClaudeBot`, `CCBot`, `Bytespider`) and the directive-only tokens (`Google-Extended`, `Applebot-Extended`). List which are allowed and which are blocked. Name the tools that act on a person's request and may ignore `robots.txt` (`ChatGPT-User`, `Claude-User`, `Perplexity-User`). Report whether `robots.txt` names xAI's `GrokBot`, `xAI-Grok`, `Grok-DeepSearch` or `xAI-SearchBot`, and state that xAI publishes no crawler documentation and no list of its addresses, so whether the names are honored, or whether a visitor using one is really xAI, cannot be said.
- **Evidence kept:** The raw `robots.txt`, the allowed and blocked lists, and the xAI names found.
- **Bands:** always reported as a choice. The band is 4 and exists only so the row renders; it never enters a total.
- **Note:** A choice is not a defect. Blocking every training crawler costs nothing and says nothing about readiness. The xAI names are observed in third-party directories and are listed as undocumented.
- **Fix:** Nothing to fix. If the choice was never made on purpose, make it now, and say the same thing everywhere (PST-5).
- **What changed in 12.0:** Training crawlers are reported as your choice. The report also says which tools acting on a person's request may ignore robots.txt, and lists xAI's Grok crawlers as observed but undocumented.
- **Replaces:** AIR-1.1
- **Review by:** 2027-04-18

### PST-2 — Have you posted a Content Signals statement about what AI may do with your content?

- **Question:** Have you posted a Content Signals statement about what AI may do with your content?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Search specialist, Site owner
- **Evidence:** None found
- **Measures:** We look for a Content-Signal line in robots.txt or in response headers.
- **Why this matters:** A line in robots.txt or in a response header that states whether AI may search, quote or train on your content. Having a stated position is the point. [Cloudflare, Content Signals Policy](https://blog.cloudflare.com/content-signals-policy/): Cloudflare defines the Content-Signal line this test looks for.
- **Sources:** [Cloudflare, Content Signals Policy](https://blog.cloudflare.com/content-signals-policy/), 2025-09-24 (A); [Search Engine Roundtable, Mueller on Content-Signal](https://www.seroundtable.com/google-cloudflare-content-signals-41631.html), 2026-07-06 (C)
- **Detect:** Parse `Content-Signal:` lines in `robots.txt` and in response headers. Validate syntax (`key=yes|no`, comma-delimited) for `search`, `ai-input` and `ai-train`, and check for contradiction with `Disallow` rules.
- **Evidence kept:** The signal lines found, where they were found and the contradictions noted.
- **Bands:** describe the state in the report; none moves the score. 4 — all three signals declared, valid and consistent with `robots.txt`. 3 — declared but one signal omitted. 2 — declared with a syntax error or a contradiction. 1 — a partial or malformed attempt. 0 — absent.
- **Note:** Any combination of `yes` and `no` reads as 4. We are noting that a deliberate position exists, not which position it is. No company is documented honoring the line, and Cloudflare says some will ignore it.
- **Fix:** Run the policy conversation with the site owner, then add the line.
- **What changed in 12.0:** Moved out of the score: no company is documented honoring it. It carried 3 points in 11.5 and carries none now.
- **Replaces:** AIR-1.4
- **Review by:** 2027-04-18

### PST-3 — Have you published a license for AI use of your content?

- **Question:** Have you published a license for AI use of your content?
- **Not scored**
- **Applicability:** conditional — the client holds licensable archives (journals, museums, associations, research bodies) or has opted into a licensing posture
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Site owner, Back-end developer
- **Evidence:** Standard only
- **Measures:** We look for an RSL licensing file and whether your feeds and page code point to it.
- **Why this matters:** A machine-readable license for AI use of your content, so a company can find out what you allow without writing to you first. [RSL Collective, standard announcement](https://rslstandard.org/press/rsl-standard): The RSL Collective's own announcement defines the licensing format this test looks for.
- **Sources:** [RSL Collective, standard announcement](https://rslstandard.org/press/rsl-standard), 2025-09-10 (A)
- **Detect:** Two halves. **The document:** fetch `/license.xml` and any path referenced from `robots.txt`, validate it against the RSL 1.0 schema, and check for an HTTP `Link:` header on content responses. **Propagation:** where the document exists, check RSS and Atom feeds for licensing elements and sampled JSON-LD for a `license` property on licensable types.
- **Evidence kept:** The document found and its validity, where it is referenced, and the feeds and pages that carry it.
- **Bands:** the weakest half decides, and the propagation half is read only where the document exists.
  - **Document:** 4 — valid, referenced from both `robots.txt` and headers. 3 — valid, referenced from one. 2 — present but invalid. 1 — referenced but missing. 0 — absent.
  - **Propagation:** 4 — feeds and markup both carry it. 2 — one channel. 0 — neither.
- **Note:** Shown for sites that hold licensable content and never scored: no AI company is documented honoring RSL.
- **Fix:** Decide terms with the site owner first. The XML is the easy half. Then add the license reference to feed generation and to the markup field mapping.
- **What changed in 12.0:** Two tests merge into one. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-4.1, AIR-4.2
- **Review by:** 2027-04-18

### PST-4 — Have you reserved your text and data mining rights in a form machines can read?

- **Question:** Have you reserved your text and data mining rights in a form machines can read?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Site owner, Back-end developer
- **Evidence:** Standard only
- **Measures:** Whether the site reserves its text and data mining rights with a TDMRep file or header.
- **Why this matters:** A reservation of your text and data mining rights, in a form machines can read. TDMRep is a W3C community standard tied to EU copyright law. [W3C, TDM Reservation Protocol community group](https://www.w3.org/community/tdmrep/): The community group publishes the protocol this test looks for.
- **Sources:** [W3C, TDM Reservation Protocol community group](https://www.w3.org/community/tdmrep/), undated (A)
- **Detect:** Fetch `/.well-known/tdmrep.json`, read the `tdm-reservation` response header on sampled pages and read the `tdm-reservation` meta tag on them. The file speaks for the site and the header and the tag speak for a page.
- **Evidence kept:** The file found and its status, and the pages whose headers or meta tags carry the reservation.
- **Bands:** describe the state in the report; none moves the score. 4 — the file and at least one page-level signal (header or meta tag). 3 — the file alone, or a page-level signal alone. 0 — none.
- **Note:** Provisional. The first release reads that the file, the header and the tag are there, and does not validate the file's contents against the protocol. It is shown as the site's choice and never scored: no consumer is documented.
- **Fix:** Declare your text and data mining position in TDMRep, in the file and in the header, and make it match PST-2.
- **What changed in 12.0:** New in 12.0, shown and never scored. It has no v11 predecessor.
- **Review by:** 2027-04-18

### PST-5 — Do your statements about AI use agree with each other?

- **Question:** Do your statements about AI use agree with each other?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Site owner, Search specialist
- **Evidence:** None found
- **Measures:** Whether the site's statements about AI use, in `robots.txt`, Content Signals, headers and licenses, agree with each other.
- **Why this matters:** Your statements about AI use should say the same thing. A Markdown copy that allows AI training while robots.txt forbids it tells a crawler two things. [Cloudflare, Content Signals Policy](https://blog.cloudflare.com/content-signals-policy/): Cloudflare defines the Content-Signal line that this test compares with the other statements.
- **Sources:** [Cloudflare, Content Signals Policy](https://blog.cloudflare.com/content-signals-policy/), 2025-09-24 (A)
- **Detect:** Collect every statement the site makes about AI use: Content Signals, the `Disallow` rules in `robots.txt`, a TDMRep reservation, an RSL license and a published `llms-full.txt`. Compare them and list each contradiction, such as Content Signals saying `ai-train=no` beside an `llms-full.txt` that publishes the full text. If the site makes no such statement, there is nothing to compare and the test is not applicable.
- **Evidence kept:** Each statement found, where it was found, and each contradiction.
- **Bands:** describe the state in the report; none moves the score. 4 — the statements agree. 1 — at least one contradiction.
- **Note:** The comparison covers `robots.txt`, Content Signals, TDMRep (the `tdm-reservation` header and meta tag, which carry its value), the RSL file and `llms-full.txt`. It does not read the value inside `tdmrep.json`. The contradictions it names are Content Signals against `Disallow` rules, against a reservation and against a published `llms-full.txt`, and a reservation against a published `llms-full.txt`.
- **Fix:** Decide the position once, then express it the same way in `robots.txt`, response headers and page tags.
- **What changed in 12.0:** New in 12.0, shown and never scored. It has no v11 predecessor.
- **Review by:** 2027-04-18

### PST-6 — Is your site switched on for Google's AI answers?

- **Question:** Is your site switched on for Google's AI answers?
- **Not scored**
- **Applicability:** always
- **Verification:** manual
- **Effort:** small
- **Fixed by:** Search specialist, Site owner
- **Evidence:** AI product
- **Measures:** Whether the owner has confirmed the Search Console setting that switches the site on or out of Google's AI answers.
- **Why this matters:** Google lets site owners switch their site out of its AI answers. A scan cannot see the setting, so we ask you to confirm it. [Google, AI features and your website](https://developers.google.com/search/docs/appearance/ai-features): Google's own page describes the controls a site owner has over how content appears in its AI features.
- **Sources:** [Google, AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), 2025-12-10 (A)
- **Detect:** None from outside. The report shows a prompt asking the owner to confirm the setting in Search Console. The owner's answer is the evidence, and it is recorded with the date it was given.
- **Evidence kept:** The owner's confirmation and its date. Nothing else.
- **Note:** It is never scored, because a number should not rest on something a scan cannot check.
- **Fix:** Open Search Console, find the control for generative AI, and confirm it matches the site owner's decision.
- **What changed in 12.0:** New in 12.0, shown and never scored. It has no v11 predecessor.
- **Review by:** 2027-04-18

## Extras · 20 items · not scored

Extras are good practice with no documented reader: some for coding agents and agent tools, some markup nothing is documented reading, and a few early signals with essentially no adoption. Each is measured and reported like any other test and contributes nothing to the hundred, because scoring a practice nobody is documented using subtracts the same points from every site and moves nobody relative to anybody.

They are numbered within this section rather than inside a category. A global number would imply a place in the score, and they have none.

**For coding agents and agent tools (EXT-1 to EXT-4)**

### EXT-1 — Do you publish an llms.txt file for coding assistants?

- **Question:** Do you publish an llms.txt file for coding assistants?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** AI product (coding agents only)
- **Measures:** We look for /llms.txt and /llms-full.txt and whether the links work.
- **Why this matters:** A file at /llms.txt listing your most important pages, for coding assistants and documentation tools. Search crawlers do not read it. [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide): Google says its Search does not use the file, which is why it is credited for coding agents only.
- **Sources:** [Ahrefs, llms.txt study (137,210 domains)](https://ahrefs.com/blog/llmstxt-study/), 2026-06-15 (B); [Dries Buytaert, a month of Cloudflare logs](https://dri.es/markdown-llms-txt-and-ai-crawlers), 2026-03-05 (B); [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** Two halves. **`/llms.txt`:** fetch it and validate against the llmstxt.org structure: an `# H1` title, an optional blockquote summary, and `##` sections of Markdown links. Resolve a sample of the linked URLs. Compare listed URLs against the sitemap to measure coverage; tracking the sitemap means listing at least 75% of it. Detect the Drupal `llms_txt` module by response headers or known output patterns and report it as evidence; it does not change the band. **`/llms-full.txt`:** fetch it only to see whether it inlines content, and cross-check it against Content Signals.
- **Evidence kept:** The files found, their structure, link results, sitemap coverage and any contradiction with Content Signals.
- **Bands:** the weakest half decides, and `/llms-full.txt` is read only where it exists.
  - **4** — valid, links resolve, coverage tracks the sitemap.
  - **3** — valid, links resolve, coverage lags the sitemap.
  - **2** — present with broken links, or `/llms-full.txt` contradicts declared signals.
  - **1** — present but malformed.
  - **0** — absent.
- **Note:** Shown and never scored. An absent `/llms-full.txt` never lowers the band. In one measurement 97% of valid files drew no requests from search crawlers, and the file is read by coding agents and documentation tools.
- **Fix:** On Drupal, use the `llms_txt` module with token-driven menus. A hand-written file is stale within a quarter. Publish `/llms-full.txt` only where the licensing position allows it.
- **What changed in 12.0:** Credited for coding agents only. Merges the full-text version. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-1.10, LI-7
- **Review by:** 2027-04-18

### EXT-2 — Do you list your APIs and agent tools where agents look for them?

- **Question:** Do you list your APIs and agent tools where agents look for them?
- **Not scored**
- **Applicability:** conditional — the site exposes an API or an agent capability
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Operations
- **Evidence:** Standard only
- **Measures:** We look for an API catalog and an AI catalog, and for headers that point to them.
- **Why this matters:** A list of your APIs and agent tools at the address agents check, rather than at a URL somebody has to be told about. [RFC 9727, api-catalog](https://www.rfc-editor.org/rfc/rfc9727): The RFC defines the well-known API catalog and the link relation that points to it.
- **Sources:** [RFC 9727, api-catalog](https://www.rfc-editor.org/rfc/rfc9727), 2025 (A); [AI Catalog specification (draft)](https://ai-catalog.io/spec/), draft (A); [MCP SEP-2127, server cards (final)](https://modelcontextprotocol.io/seps/2127-mcp-server-cards), 2026 (A)
- **Detect:** Read the `Link` response headers for the `api-catalog` and `ai-catalog` relations, and probe `/.well-known/api-catalog` and the AI Catalog file at its well-known address. Parse what is found. Any one valid entry counts.
- **Evidence kept:** The headers and files found and the entries each lists.
- **Bands:** 4 — at least one valid catalog entry, found by header or by file. 2 — a catalog present but invalid or empty. 0 — absent.
- **Note:** Shown and never scored. RFC 9727 is a Proposed Standard and the MCP server card proposal is final, but no consumer is documented, and in one survey fewer than 15 of the top 200,000 sites published both.
- **Fix:** Publish the catalog at the well-known address and point to it from a `Link` header.
- **What changed in 12.0:** Reads response headers and the api-catalog and ai-catalog files; any one valid entry counts. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-6.2
- **Review by:** 2027-04-18

### EXT-3 — If you run your own crawler or agent, do you publish its signing keys?

- **Question:** If you run your own crawler or agent, do you publish its signing keys?
- **Not scored**
- **Applicability:** conditional — the site runs its own crawler or agent
- **Verification:** auto-partial
- **Effort:** large
- **Fixed by:** Operations, Back-end developer
- **Evidence:** Standard only
- **Measures:** If you operate a crawler or agent, we look for the key directory that proves its requests are yours.
- **Why this matters:** If you run your own crawler or agent, publish the keys that prove its requests are yours, so the sites it visits can verify it. [IETF draft, Web Bot Auth key directory](https://www.ietf.org/archive/id/draft-meunier-webbotauth-httpsig-directory-00.html): The working-group draft defines the key directory a signing agent publishes.
- **Sources:** [IETF draft, Web Bot Auth key directory](https://www.ietf.org/archive/id/draft-meunier-webbotauth-httpsig-directory-00.html), 2026-06-26 (A)
- **Detect:** Probe `/.well-known/http-message-signatures-directory`. The draft requires it to answer `200` at that address itself (a verifier does not follow a redirect), as `application/http-message-signatures-directory+json`, with a JSON Web Key Set that has at least one key. A signed request carries `Signature`, `Signature-Input` (covering `@authority` or `@target-uri` and the `signature-agent` member, with `created`, `expires` and `tag="web-bot-auth"`) and `Signature-Agent`, a dictionary of HTTPS URLs that name the signer's directory.
- **Evidence kept:** The response at the directory address: status, redirect, media type and key count.
- **Bands:** 4 — a key directory that meets the draft. 3 — a key set is published but served in a way a verifier refuses: through a redirect, or as another media type. 0 — nothing there, or something that is not a key set.
- **Note:** Applies only to sites that run their own agents. A receiving site only verifies; the signing agent publishes the directory. Shown and never scored: no consumer is documented.
- **Fix:** If you operate agents, publish the directory at the well-known address as `application/http-message-signatures-directory+json`, with no redirect, and sign requests with `Signature-Agent`.
- **What changed in 12.0:** Applies only to sites that run their own agents. It carried 1 point in 11.5 and carries none now. The 11.4 comparison of a signed request with an unsigned one is dropped, because a receiving site only verifies and the signing agent publishes the directory.
- **Replaces:** AIR-4.3
- **Review by:** 2027-04-18

### EXT-4 — Can an AI assistant connect to your site as a tool?

- **Question:** Can an AI assistant connect to your site as a tool?
- **Not scored**
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** large
- **Fixed by:** Back-end developer, Operations
- **Evidence:** AI product (you add it)
- **Measures:** We look for a public MCP server that assistants can be pointed at.
- **Why this matters:** A public MCP server over your catalog or directory, so an assistant can be pointed at it and call it as a tool rather than scraping a results page. [MCP SEP-2127, server cards (final)](https://modelcontextprotocol.io/seps/2127-mcp-server-cards): The protocol's final proposal defines how a server describes itself so it can be found.
- **Sources:** [MCP SEP-2127, server cards (final)](https://modelcontextprotocol.io/seps/2127-mcp-server-cards), 2026 (A)
- **Detect:** Discover a public MCP server from `/.well-known/` and from the AI catalog. Enumerate tools, check each has a description and typed parameters, and call one read-only tool against live data.
- **Evidence kept:** The server found, its tools and their descriptions, and the result of one read-only call.
- **Bands:** 4 — documented, typed tools returning live data, with auth and rate limiting. 3 — tools present but thinly documented. 2 — a generic query endpoint rather than narrow tools. 0 — none.
- **Note:** Shown and never scored. MCP clients connect to a server a person adds; there is no discovery by an assistant today, which is why the label says you add it. A well-described tool with three parameters beats a generic endpoint.
- **Fix:** Expose the catalog as a few narrow, typed tools. Document each.
- **What changed in 12.0:** Moved from Leading Indicators.
- **Replaces:** LI-6
- **Review by:** 2027-04-18

**Markup with no documented reader (EXT-5 to EXT-10)**

### EXT-5 — Is your page code one connected description of your organization?

- **Question:** Is your page code one connected description of your organization?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** Standard only
- **Measures:** We check that your structured data links your organization, site and pages together with stable IDs.
- **Why this matters:** Structured data that links together, your organization, your site and this page, instead of a scattering of disconnected labels. [Ahrefs, 1,885 pages that added schema](https://ahrefs.com/blog/schema-ai-citations/): It is a measurement of whether adding schema changed AI citations, and the best evidence we found. It is not documentation from an AI company.
- **Sources:** [Ahrefs, 1,885 pages that added schema](https://ahrefs.com/blog/schema-ai-citations/), 2026-05-11 (B); [searchVIU, schema markup and AI](https://www.searchviu.com/en/schema-markup-and-ai-in-2025-what-chatgpt-claude-perplexity-gemini-really-see/), 2025-12-02 (B)
- **Detect:** Extract all JSON-LD across the sample. Build a graph of nodes and `@id` references. Measure: what fraction of **entity** nodes carry an `@id` (value objects such as `ListItem`, `PostalAddress`, `ContactPoint`, `EntryPoint` and `BreadcrumbList` are excluded, because they have no identity and nothing should reference them); whether `Organization` and `WebSite` have stable canonical `@id` URIs reused site-wide; whether `WebPage` nodes reference `WebSite` and `WebSite` references `Organization`; and how many duplicate definitions of the same entity exist. The index counts every distinct `Person` `@id` as a duplicate entity.
- **Evidence kept:** The resolved graph, orphan node count and duplicate entity count.
- **Bands:** 4 — canonical `@id`s reused, chain intact, no duplicates. 3 — chain intact with minor duplication. 2 — `@id`s present but inconsistently reused. 1 — `@id`s rare. 0 — isolated blobs with no references.
- **Note:** Shown and never scored: schema parsers read JSON-LD, but nothing documents anyone using an `@id` graph.
- **Fix:** Define canonical `@id` URIs once and reference them everywhere.
- **What changed in 12.0:** Moved out of the score: no documented consumer. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-1.11
- **Review by:** 2027-04-18

### EXT-6 — Is your page code generated from your content rather than typed by hand?

- **Question:** Is your page code generated from your content rather than typed by hand?
- **Not scored**
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** medium
- **Fixed by:** Back-end developer
- **Evidence:** None found
- **Measures:** We check whether structured data is built from your content fields or hard-coded.
- **Why this matters:** Structured data generated from your content model survives the next content change. Hardcoded markup rots quietly. [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide): Google says no special markup is needed for its AI features, which is why this is maintenance advice and not a score.
- **Sources:** [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** Heuristics only. Compare JSON-LD values against visible field values on the same page; a mapped implementation matches. Flag identical literal values repeated across pages of the same type where the visible content differs. Detect Schema.org Metatag output patterns on Drupal. Confirm with the build team.
- **Evidence kept:** Per template: the values compared and the literals repeated.
- **Bands:** 4 — values track content across every sampled page of a type, and the build team confirms the mapping. 3 — values track content on every sampled page, generation unconfirmed. 2 — mixed, with some literals. 0 — clear hardcoding, or values contradict the visible page.
- **Note:** Shown and never scored. An attestation lifts the observable ceiling of 3 to 4.
- **Fix:** Map Drupal fields to schema properties through configuration so editors maintain it.
- **What changed in 12.0:** Moved out of the score. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-3.1
- **Review by:** 2027-04-18

### EXT-7 — If you run real question-and-answer pages, are they marked as such?

- **Question:** If you run real question-and-answer pages, are they marked as such?
- **Not scored**
- **Applicability:** conditional — the site has real question-and-answer content
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Content team, Back-end developer
- **Evidence:** Search index
- **Measures:** We look for QAPage markup on pages where visitors really ask and answer questions.
- **Why this matters:** If you run pages where visitors really ask and answer questions, mark them up as such. Do not invent a question-and-answer block that is not on the page. [Google Search updates log (retirements)](https://developers.google.com/search/updates): Google's log records the end of the FAQ result, and QAPage is still documented.
- **Sources:** [Google Search updates log (retirements)](https://developers.google.com/search/updates), current (A)
- **Detect:** Validate `QAPage` structure. Cross-check that every marked-up question and answer appears in the visible page text, and that the page is a real exchange between visitors. Flag pages where the markup exists with no corresponding visible content. `FAQPage` is no longer evaluated.
- **Evidence kept:** Per page: the questions marked up and whether each is visible.
- **Bands:** 4 — real Q&A marked up, nothing fabricated. 2 — partial coverage. 0 — absent where warranted. **Cap at 1 if markup is found with no visible content**, regardless of coverage.
- **Fix:** Mark up what exists. Do not invent questions to earn the markup.
- **What changed in 12.0:** FAQ markup is retired; QAPage is kept. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-3.4
- **Review by:** 2027-04-18

### EXT-8 — Does sensitive content, like health, legal or money advice, name who reviewed it?

- **Question:** Does sensitive content, like health, legal or money advice, name who reviewed it?
- **Not scored**
- **Applicability:** conditional — the site publishes medical, legal or financial content
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Content team, Back-end developer
- **Evidence:** None found
- **Measures:** We look for a named reviewer on health, legal and financial pages.
- **Why this matters:** Health, legal and financial pages should name the person who reviewed them, in the page and in the markup, not only in a design a machine cannot read. [Schema.org, reviewedBy](https://schema.org/reviewedBy): Schema.org's own property for naming a reviewer in markup.
- **Sources:** None recorded in the evidence register beyond the property definition cited under Why this matters: [Schema.org, reviewedBy](https://schema.org/reviewedBy), undated (A)
- **Detect:** On sensitive pages, check for `reviewedBy` referencing a credentialed `Person`, plus `lastReviewed` where the type supports it, plus a visible reviewer statement.
- **Evidence kept:** Per page: the reviewer found in the markup and on the page.
- **Note:** Shown and never scored. A visible reviewer credential is sound practice with no documented machine reader.
- **Fix:** Most healthcare and legal clients already run review workflows. The reviewer's identity simply never reaches the page.
- **What changed in 12.0:** Moved out of the score. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-5.3
- **Review by:** 2027-04-18

### EXT-9 — Does your page code point to the sources you cite?

- **Question:** Does your page code point to the sources you cite?
- **Not scored**
- **Applicability:** conditional — the site publishes research or policy content
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Content team
- **Evidence:** None found
- **Measures:** We look for citation markup on pages that quote research or policy.
- **Why this matters:** Where you cite a primary source, make the citation machine-readable so the chain from claim to evidence survives. [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide): Google's guide is the primary description of what its AI features use; we found no mention of citation markup in it.
- **Sources:** [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** Check for `citation` on research and policy pages. Resolve DOIs where present. Compare against the count of outbound links to primary sources in the body.
- **Evidence kept:** Per page: the citations marked up and the links found in the body.
- **Note:** Shown and never scored. Visible, linked citations are what answer engines show.
- **Fix:** Credibility that a parser cannot see does not count.
- **What changed in 12.0:** Moved out of the score. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-5.5
- **Review by:** 2027-04-18

### EXT-10 — Do your images carry proof of where they came from?

- **Question:** Do your images carry proof of where they came from?
- **Not scored**
- **Applicability:** conditional — the client produces original photography, primary research or documents where authenticity matters
- **Verification:** auto
- **Effort:** large
- **Fixed by:** Operations, Site owner
- **Evidence:** Search index (narrow)
- **Measures:** We look for C2PA content credentials on original images.
- **Why this matters:** Content credentials travel with an image, so it can show where it came from after somebody else reposts it. [Google, image license metadata (C2PA)](https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata): Google documents showing C2PA data in its 'About this image' panel.
- **Sources:** [Google, image license metadata (C2PA)](https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata), 2025-12-10 (A)
- **Detect:** Download sampled original images and PDFs and read C2PA manifests. Confirm the manifest survives the image derivative pipeline; this is where it usually breaks.
- **Evidence kept:** Per file: the manifest found and whether it survived each derivative.
- **Bands:** 4 — valid manifests on originals and derivatives. 2 — present on originals, stripped by the pipeline. 0 — absent.
- **Note:** Shown and never scored. Google shows the data, but no answer engine is documented reading it, so it is not how AI answers choose or cite sources.
- **Fix:** Scope this deliberately. It needs signing infrastructure.
- **What changed in 12.0:** Moved out of the score. It carried 2 points in 11.5 and carries none now.
- **Replaces:** AIR-5.6
- **Review by:** 2027-04-18

**Early signals (EXT-11 to EXT-13)**

### EXT-11 — Have you marked the part of a page that answers a spoken question?

- **Question:** Have you marked the part of a page that answers a spoken question?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Back-end developer, Content team
- **Evidence:** Standard only
- **Measures:** We look for speakable markup on summaries.
- **Why this matters:** Flag the part of a page that answers a spoken question, the lede or the summary, so an assistant reads that rather than guessing at a paragraph. [Google Search updates log (retirements)](https://developers.google.com/search/updates): Google's log is where changes to supported markup are announced.
- **Sources:** [Google Search updates log (retirements)](https://developers.google.com/search/updates), current (A)
- **Detect:** Extract `speakable` with `cssSelector` or `xpath`. Resolve the selector against the DOM and confirm it matches 1–3 elements containing 40–400 characters. Flag selectors that match the whole body or nothing.
- **Evidence kept:** Per page: the selector and what it matched.
- **Bands:** 4 — resolves to a genuine summary passage. 2 — present but resolves too broadly. 0 — absent.
- **Note:** Shown and never scored: speakable is in beta for English news on Google Home only.
- **Fix:** Point it at the lede, not the article.
- **What changed in 12.0:** Detection and bands unchanged.
- **Replaces:** LI-2
- **Review by:** 2027-04-18

### EXT-12 — Do you tell search engines the moment a page changes?

- **Question:** Do you tell search engines the moment a page changes?
- **Not scored**
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** small
- **Fixed by:** Back-end developer, Search specialist
- **Evidence:** Search index
- **Measures:** We look for IndexNow pings when you publish or update.
- **Why this matters:** Tell search engines the moment a page changes, rather than waiting to be crawled again. [IndexNow documentation](https://www.indexnow.org/documentation): The protocol's own docs, backed by Microsoft Bing and Yandex as the search engines that consume it.
- **Sources:** [Bing Webmaster Blog, sitemaps in AI-powered search](https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search), 2025-07-31 (A)
- **Detect:** Look for an IndexNow key file at the site root (a 32–128 character hex filename returning its own key). Confirm the key resolves. Whether submissions actually fire on publish requires attestation.
- **Evidence kept:** The key file found, whether it resolves, and the attestation if one was given.
- **Bands:** 4 — key file present, valid, and submission confirmed. 3 — key file present and valid, submission unconfirmed. 2 — a key file is referenced but does not resolve or does not contain its own key. 0 — absent or not discoverable.
- **Limitation:** the key file's name *is* the key, and the key is not published. A scanner can only find it where `robots.txt` or a conventional path advertises it, so a zero here means *not discoverable* rather than *absent*. Score it honestly and say which.
- **Note:** Shown and never scored. Google does not use IndexNow, and no AI vendor is documented using it.
- **Fix:** Hook submission into the publish workflow rather than a schedule.
- **What changed in 12.0:** Detection and bands unchanged.
- **Replaces:** LI-3
- **Review by:** 2027-04-18

### EXT-13 — Can an assistant ask your site a question directly?

- **Question:** Can an assistant ask your site a question directly?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** large
- **Fixed by:** Back-end developer, Operations
- **Evidence:** Standard only
- **Measures:** We look for an NLWeb endpoint.
- **Why this matters:** A natural-language endpoint over your own structured data, so an assistant can ask your site a question instead of scraping around it. [NLWeb](https://github.com/nlweb-ai/NLWeb): The NLWeb project's own repository defines the endpoint this test looks for.
- **Sources:** None recorded in the evidence register beyond the project's own repository cited under Why this matters: [NLWeb](https://github.com/nlweb-ai/NLWeb), undated (A)
- **Detect:** Probe known NLWeb paths and `/.well-known/` entries. If found, send a representative question and check for a schema.org-formatted JSON response.
- **Evidence kept:** The endpoint found and the response to one representative question.
- **Bands:** 4 — endpoint answers correctly and is grounded in site content. 2 — endpoint responds but answers poorly. 0 — absent.
- **Note:** Shown and never scored: an open-source toolkit with no AI-product consumer documented.
- **Fix:** Stand up the endpoint over structured data you already publish.
- **What changed in 12.0:** Detection and bands unchanged.
- **Replaces:** LI-5
- **Review by:** 2027-04-18

### EXT-14 — Does your site offer its actions to AI browsers as tools?

- **Question:** Does your site offer its actions to AI browsers as tools?
- **Not scored**
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** medium
- **Fixed by:** Front-end developer, Back-end developer
- **Evidence:** Scanner-listed (Lighthouse and Cloudflare)
- **Measures:** We look for WebMCP tools: a form that declares itself as a tool, and tools a page registers while it loads.
- **Why this matters:** A page can hand a browser agent its actions by name instead of leaving the agent to work out its buttons. [Chrome for Developers, WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp): Chrome describes two interfaces, one declared on a form and one registered from script, that let a browser agent act on a visitor's behalf.
- **Sources:** [Chrome for Developers, WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp), 2026-10-18 (A); [Chrome for Developers, Lighthouse agentic browsing](https://developer.chrome.com/docs/lighthouse/agentic-browsing), 2026-10-18 (A); [Cloudflare, Agent Readiness score](https://blog.cloudflare.com/agent-readiness/), 2026-04-17 (A)
- **Detect:** On each sampled page read forms that carry a `toolname` attribute and whether each has a `tooldescription`, and scripts that mention `modelContext`. While rendering, a stand-in for `navigator.modelContext` records every tool the page registers, with its name, description and whether it has an input schema. The attribute names are the explainer's and the specification is in early preview: confirm them against it before relying on this test. Lighthouse needs Chrome 150 and an origin trial to read the same things.
- **Evidence kept:** Per page: forms declared as tools and how many are described, scripts that mention the API, and each tool registered while rendering.
- **Bands:** 4 — every tool and declared form describes itself. 3 — tools exist and some have no description. 2 — a script refers to the API but no tool was registered while the page loaded. 0 — nothing.
- **Note:** Shown and never scored: it is a preview, no AI product is documented reading it, and a scanner listing it is not a reader. Lighthouse also flags a form that has not been declared and validates a tool's schema; this test counts what is declared and records whether a schema is present.
- **Fix:** Declare the actions an agent would want, such as search and contact forms, with `toolname` and `tooldescription`, or register them from script, each with a description and an input schema.
- **What changed in 12.0:** New test, added so that Index 12 measures every check that Cloudflare's Agent Readiness score and Lighthouse's agentic browsing category list. No points.
- **Review by:** 2027-04-18

### EXT-15 — Can an AI agent find out how to sign in to your site?

- **Question:** Can an AI agent find out how to sign in to your site?
- **Not scored**
- **Applicability:** conditional — the site has a public API
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Operations
- **Evidence:** Scanner-listed (Cloudflare)
- **Measures:** We look for the documents that tell an agent where your sign-in is: protected-resource metadata, authorization-server metadata and auth.md.
- **Why this matters:** An agent that meets a protected API needs to learn where to sign in without a person pointing it there. [IETF, RFC 9728 (OAuth Protected Resource Metadata)](https://www.rfc-editor.org/rfc/rfc9728): The standard defines the document at a well-known address in which a protected resource names its authorization servers.
- **Sources:** [IETF, RFC 9728 (OAuth Protected Resource Metadata)](https://www.rfc-editor.org/rfc/rfc9728), 2025 (A); [IETF, RFC 8414 (OAuth Authorization Server Metadata)](https://www.rfc-editor.org/rfc/rfc8414), 2018 (A); [Cloudflare, Agent Readiness score](https://blog.cloudflare.com/agent-readiness/), 2026-04-17 (A)
- **Detect:** Probe `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`, `/.well-known/openid-configuration`, `/auth.md` and `/.well-known/auth.md`. Protected-resource metadata is valid when it is a JSON object whose `resource` is an https address. Authorization-server metadata is valid when it has an https `issuer` and an endpoint. auth.md counts when it is Markdown with a heading; its publisher and a second source disagree on its address, and its fields are not settled, so none are checked.
- **Evidence kept:** Per document: the address, status, and whether it is the document its address promises.
- **Bands:** 4 — valid protected-resource metadata. 3 — valid authorization-server metadata or auth.md. 2 — a JSON or Markdown document is served at one of the addresses and is not that document; a page that answers every address with HTML is not an attempt. 0 — nothing.
- **Note:** Applies to sites with a public API. Shown and never scored: no AI product is documented reading it from a site.
- **Fix:** Publish `/.well-known/oauth-protected-resource` with the resource and its authorization servers, and the server's own metadata at its issuer.
- **What changed in 12.0:** New test. No points.
- **Review by:** 2027-04-18

### EXT-16 — Do you publish a card or a skills list for the agents you run?

- **Question:** Do you publish a card or a skills list for the agents you run?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Back-end developer, Operations
- **Evidence:** Scanner-listed (Cloudflare)
- **Measures:** We look for an agent card and a skills index at their well-known addresses.
- **Why this matters:** If your site runs an agent, a card tells other agents what it can do and where to reach it. [Cloudflare, Agent Skills discovery RFC](https://github.com/cloudflare/agent-skills-discovery-rfc): The proposal fixes the index's address and shape, with a name, type, description, address and digest for every skill.
- **Sources:** [Cloudflare, Agent Skills discovery RFC](https://github.com/cloudflare/agent-skills-discovery-rfc), 2026 (A); [specification.website, A2A agent cards](https://specification.website/spec/agent-readiness/a2a-agent-cards.md), 2026 (C); [Cloudflare, Agent Readiness score](https://blog.cloudflare.com/agent-readiness/), 2026-04-17 (A)
- **Detect:** Probe `/.well-known/agent-card.json` (and `/.well-known/agent.json`, its name before A2A 0.3) and `/.well-known/agent-skills/index.json`. A card is valid when it is JSON with a `name` and either skills or an endpoint. A skills index is valid when it has `$schema` and a `skills` list in which every entry has a lowercase `name`, a `type` of `skill-md` or `archive`, a `description`, a `url` and a `sha256:` digest. The A2A address and fields are from secondary summaries, so confirm them against the A2A specification.
- **Evidence kept:** Per document: the address, status, and whether it is valid.
- **Bands:** 4 — a valid card or skills index at the current address. 3 — a valid card only at the older address. 2 — a JSON document is served and is not that document; a page that answers every address with HTML is not an attempt. 0 — nothing. The AI Catalog is read by EXT-2.
- **Note:** Shown and never scored: no AI product is documented reading either file from a site. Most sites run no agent and have nothing to publish.
- **Fix:** If you run an agent, publish its card as JSON at the well-known address; if you offer skills, publish the index with a digest for each.
- **What changed in 12.0:** New test. No points.
- **Review by:** 2027-04-18

### EXT-17 — Do you list your agents in your domain's DNS records?

- **Question:** Do you list your agents in your domain's DNS records?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Operations
- **Evidence:** Scanner-listed (Cloudflare)
- **Measures:** We look up the SVCB record where DNS-AID says a domain lists its agents.
- **Why this matters:** A domain can announce its agents in DNS, where an agent looks before it fetches anything. [IETF, DNS-AID draft](https://datatracker.ietf.org/doc/html/draft-mozleywilliams-dnsop-dnsaid-01): The draft describes a leaf zone under `_agents` whose SVCB records say how to reach each agent.
- **Sources:** [IETF, DNS-AID draft](https://datatracker.ietf.org/doc/html/draft-mozleywilliams-dnsop-dnsaid-01), 2026-03 (A)
- **Detect:** Ask the machine's own resolver for the SVCB record at `_index._agents.<your host>`. An answer with no such name means none; a resolver that does not answer is not judged, because it says nothing about the zone. The draft had expired at its last revision, so the label and the record may change.
- **Evidence kept:** The name asked and the number of records answered, or the reason no answer came.
- **Bands:** 4 — at least one SVCB record. 0 — the name has none.
- **Note:** Shown and never scored: an expired draft with no documented reader.
- **Fix:** Publish an SVCB record for each agent under `_agents` in your domain, signed with DNSSEC, once the draft settles.
- **What changed in 12.0:** New test. No points.
- **Review by:** 2027-04-18

### EXT-18 — Do you tell AI shoppers how they can pay?

- **Question:** Do you tell AI shoppers how they can pay?
- **Not scored**
- **Applicability:** conditional — the site sells something
- **Verification:** auto-partial
- **Effort:** large
- **Fixed by:** Back-end developer, Site owner
- **Evidence:** Scanner-listed (Cloudflare)
- **Measures:** We look for a Universal Commerce Protocol profile, and for an HTTP 402 answer that names x402 or MPP.
- **Why this matters:** A shop can tell an agent which payment methods it accepts before the agent tries to buy. [Google for Developers, Universal Commerce Protocol](https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/): Google's write-up describes the merchant profile at a well-known address in which a shop lists its services and payment handlers.
- **Sources:** [Google for Developers, Universal Commerce Protocol](https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/), 2026 (A); [Cloudflare, Agentic payments](https://developers.cloudflare.com/agents/agentic-payments), 2026 (A); [Cloudflare, Agent Readiness score](https://blog.cloudflare.com/agent-readiness/), 2026-04-17 (A)
- **Detect:** Probe `/.well-known/ucp` and accept JSON that declares a version, services or capabilities. On any sampled page that answers HTTP 402, look for a `PAYMENT-REQUIRED` header (x402) or a `WWW-Authenticate` scheme of `Payment` (MPP). The Agentic Commerce Protocol has no merchant discovery address that could be confirmed, so it is not detected, and x402 and MPP show only on a page that asks for payment.
- **Evidence kept:** The profile document, and each page that answered 402 with a payment header.
- **Bands:** 4 — a profile or a payment challenge was found. 0 — none was seen.
- **Note:** Applies to sites that sell something. Shown and never scored, and its confidence is low: three of the four protocols are not discoverable from a page that does not ask for payment.
- **Fix:** If agents may buy from you, publish a Universal Commerce Protocol profile that lists your payment handlers.
- **What changed in 12.0:** New test. No points.
- **Review by:** 2027-04-18

### EXT-19 — Does robots.txt say where your sitemap is?

- **Question:** Does robots.txt say where your sitemap is?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** small
- **Fixed by:** Search specialist, Back-end developer
- **Evidence:** Scanner-listed (Cloudflare)
- **Measures:** We check that a sitemap exists and that robots.txt names it, which is how a crawler is meant to find it.
- **Why this matters:** A sitemap that robots.txt names is found by every crawler without guessing an address. [Sitemaps.org, the sitemap protocol](https://www.sitemaps.org/protocol.html): The protocol lets a robots.txt file name a sitemap with a `Sitemap:` line.
- **Sources:** [Sitemaps.org, the sitemap protocol](https://www.sitemaps.org/protocol.html), undated (A); [Cloudflare, Agent Readiness score](https://blog.cloudflare.com/agent-readiness/), 2026-04-17 (A)
- **Detect:** Read the `Sitemap:` lines of robots.txt and the sitemaps the scan loaded, from those lines or from `/sitemap.xml`.
- **Evidence kept:** The sitemap addresses robots.txt names, and how many URLs were read.
- **Bands:** 4 — robots.txt names a sitemap and URLs were read from it. 3 — a sitemap loads but robots.txt does not name it. 2 — robots.txt names a sitemap that could not be read. 0 — none.
- **Note:** Shown and never scored: Google documents sitemaps, but this test asks only whether one is declared, which RED-3 and RED-8 do not.
- **Fix:** Add a `Sitemap:` line with the full address to robots.txt.
- **What changed in 12.0:** New test. No points.
- **Review by:** 2027-04-18

### EXT-20 — Can an AI browser see the controls on your page?

- **Question:** Can an AI browser see the controls on your page?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer
- **Evidence:** Scanner-listed (Lighthouse)
- **Measures:** We look for what would break the accessibility tree an agent reads: a control hidden from it, a role that does not exist, and a role without the parent it needs.
- **Why this matters:** A browser agent finds what it can press through the accessibility tree, and a broken tree hides or mislabels controls from it. [Chrome for Developers, Lighthouse accessibility for agents](https://developer.chrome.com/docs/lighthouse/agentic-browsing/accessibility-for-agents): Lighthouse runs a subset of its accessibility audits for agents and names tree integrity and visibility as two of its three areas.
- **Sources:** [Chrome for Developers, Lighthouse accessibility for agents](https://developer.chrome.com/docs/lighthouse/agentic-browsing/accessibility-for-agents), 2026-10-18 (A); [W3C, WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/), 2023 (A)
- **Detect:** On each sampled page count the controls that can take focus but sit inside `aria-hidden="true"`, the `role` values that are not a WAI-ARIA role, and the roles that need a parent (a `tab` in a `tablist`, a `menuitem` in a `menu`, a `row` in a table) and have none. Names and labels are read by ACT-1 and ACT-4.
- **Evidence kept:** Per page: the three counts and the first few examples by tag and position.
- **Bands:** Default coverage rubric over the pages measured, where a page counts as present and correct when it has none of the three problems.
- **Note:** Shown and never scored: Lighthouse reads this, but no AI product is documented measuring it, and the rules are the accessibility ones people already follow.
- **Fix:** Remove `aria-hidden` from anything a visitor can press or take it out of the tab order, use only roles ARIA defines, and give each role its parent.
- **What changed in 12.0:** New test. No points.
- **Review by:** 2027-04-18

## Measurement · 8 items · not scored

Measurement is how you track AI traffic. Whether a channel group exists in somebody's analytics, whether access logs are retained, whether a prompt panel runs monthly: most of it cannot be observed from outside the organization, so the owner's attestation is the evidence.

They were scored until 11.0, and scoring them was a mistake worth naming. Across 69 scans of 39 sites every one of them returned the identical result, because an unverifiable check awarded the same mark to everybody. They are reported as guidance and left out of the arithmetic.

Numbered within this section, for the same reason the extras are.

### MSR-1 — Can people finish key tasks without relying on JavaScript-only clicks?

- **Question:** Can people finish key tasks without relying on JavaScript-only clicks?
- **Not scored**
- **Applicability:** conditional — the client names critical flows
- **Verification:** auto-partial
- **Effort:** large
- **Fixed by:** Front-end developer, Back-end developer
- **Evidence:** AI product
- **Measures:** You name your key tasks, such as applying or donating, and we check they work for agents that read the page structure.
- **Why this matters:** Register, donate, apply or find a clinician should complete through ordinary form submissions and real URLs, not only through clicks. [Anthropic, browser use tool (accessibility tree)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool): Anthropic documents that its browser tool reads the page's accessibility tree, the structure that a flow built from real controls exposes.
- **Sources:** [Anthropic, browser use tool (accessibility tree)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool), current (A); [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** For each named flow, walk it with JavaScript disabled. Flag `div`-based controls with click handlers, wizards with no addressable step URLs, and modal-only paths.
- **Evidence kept:** Per flow: each step, its URL and where the flow stopped.
- **Bands:** 4 — every flow completes with real URLs at each step. 2 — flows start but cannot complete. 0 — flows are JavaScript-only.
- **Fix:** Run this as a joint engineering and UX audit.
- **What changed in 12.0:** Detection and bands unchanged.
- **Replaces:** BP-1
- **Review by:** 2027-04-18

### MSR-2 — Can you count visits that come from AI assistants?

- **Question:** Can you count visits that come from AI assistants?
- **Not scored**
- **Applicability:** always
- **Verification:** manual
- **Effort:** small
- **Fixed by:** Search specialist
- **Evidence:** AI product
- **Measures:** You tell us whether your analytics separates AI assistant traffic.
- **Why this matters:** Visits from ChatGPT, Perplexity, Claude and the rest land in Direct by default, where they disappear. A channel group makes them countable. [Google Analytics, default channel groups](https://support.google.com/analytics/answer/9756891): Google's documentation on channel groups, from the analytics platform that files this traffic under Direct.
- **Sources:** [Google Analytics, default channel groups](https://support.google.com/analytics/answer/9756891), undated (A); Google Analytics AI Assistant channel, 2026-05-13 (read through a summary; address to confirm) (B)
- **Detect:** Analytics presence is detectable from the page. The channel group is not: attest it, ideally with a screenshot.
- **Evidence kept:** Whether analytics was found, and the attestation with its date.
- **Bands:** 4 — a group for AI assistant referrers live with a saved report. 2 — analytics present, no grouping. 0 — no analytics.
- **Note:** Google Analytics added a native AI Assistant channel on 2026-05-13, and it counts as a group.
- **Fix:** Turn on the AI Assistant channel or build a group for the assistants' referrers, and save a report on it.
- **What changed in 12.0:** Updated: Google Analytics added an AI Assistant channel on 2026-05-13.
- **Replaces:** BP-3
- **Review by:** 2027-04-18

### MSR-3 — Do you keep your crawler logs long enough to use them?

- **Question:** Do you keep your crawler logs long enough to use them?
- **Not scored**
- **Applicability:** always
- **Verification:** manual
- **Effort:** medium
- **Fixed by:** Operations
- **Evidence:** Practice
- **Measures:** You tell us how long access logs are kept.
- **Why this matters:** Crawler logs have to survive long enough to show a before and an after. Many hosts discard them in days. [Cloudflare, Logs](https://developers.cloudflare.com/logs/): Cloudflare's own documentation on log retention, from the edge many crawler requests pass through first.
- **Sources:** None recorded in the evidence register beyond the primary documentation cited under Why this matters: [Cloudflare, Logs](https://developers.cloudflare.com/logs/), undated (A)
- **Detect:** Not observable from outside. Attest the retention period and whether the store is queryable.
- **Evidence kept:** The attestation, its date and the retention period stated.
- **Bands:** 4 — ≥12 months retained and queryable by user-agent, path, status and date. 2 — retained but not queryable. 0 — discarded.
- **Fix:** Keep at least a year of access logs in a store you can query.
- **What changed in 12.0:** Detection and bands unchanged.
- **Replaces:** BP-5
- **Review by:** 2027-04-18

### MSR-4 — Do you get a regular report on AI crawler visits?

- **Question:** Do you get a regular report on AI crawler visits?
- **Not scored**
- **Applicability:** conditional — requires MSR-3 ≥ 2
- **Verification:** manual
- **Effort:** medium
- **Fixed by:** Search specialist, Operations
- **Evidence:** Practice
- **Measures:** You tell us whether you get a report on AI crawlers.
- **Why this matters:** Watch crawler behavior continuously rather than auditing it once. A crawler that stops appearing usually means somebody reintroduced a block. [Google Search Console, Crawl stats report](https://support.google.com/webmasters/answer/9679690): Google's own crawl-stats report, the tool built to show whether a crawler stopped showing up.
- **Sources:** [Google Search Console, Crawl stats report](https://support.google.com/webmasters/answer/9679690), undated (A); the register notes that Crawl Stats covers Googlebot only
- **Detect:** Not observable from outside. Attest whether a scheduled report on AI crawler activity exists and who reads it.
- **Evidence kept:** The attestation, its date and the report named.
- **Bands:** 4 — a scheduled report, read by a named person. 2 — an ad-hoc look. 0 — none.
- **Note:** Google's Crawl Stats covers only Googlebot, so a report on AI crawlers has to come from your own logs.
- **Fix:** Schedule a report on AI crawler requests, and send it to a person.
- **What changed in 12.0:** Reframed: Google's Crawl Stats covers only Googlebot.
- **Replaces:** BP-6
- **Review by:** 2027-04-18

### MSR-5 — Do you ask AI assistants the same questions every month and keep the answers?

- **Question:** Do you ask AI assistants the same questions every month and keep the answers?
- **Not scored**
- **Applicability:** always
- **Verification:** manual
- **Effort:** medium
- **Fixed by:** Search specialist
- **Evidence:** None found
- **Measures:** You tell us whether you track what assistants say about you.
- **Why this matters:** Ask the same questions of the same assistants every month and keep the answers, so you can see whether what they say about you is changing. [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide): Google cautions about third-party AI measurements, which is why the Index asks for a method and not a vendor.
- **Sources:** [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** Not observable from outside. Attest the panel and its history.
- **Evidence kept:** The attestation, its date and the panel described.
- **Bands:** 4 — fixed panel, baseline stored, monthly runs comparable. 2 — ad-hoc tests. 0 — none.
- **Note:** The panel has to stay fixed. Tuning prompts between runs destroys the trend line.
- **Fix:** Write the panel down, run it monthly and keep every answer.
- **What changed in 12.0:** Reframed: Google cautions about third-party AI measurements.
- **Replaces:** BP-7
- **Review by:** 2027-04-18

### MSR-6 — Have you measured how accurately an AI reads your page?

- **Question:** Have you measured how accurately an AI reads your page?
- **Not scored**
- **Applicability:** always
- **Verification:** manual
- **Effort:** medium
- **Fixed by:** Search specialist, Content team
- **Evidence:** None found
- **Measures:** You tell us whether you have a baseline for how assistants read your key pages.
- **Why this matters:** Feed a page to an assistant, ask it your key questions, and score the answers. Do it again after the fixes and compare. [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide): Google's guide is the primary description of how its AI features use a site, and it frames repeat testing as how to see change.
- **Sources:** [Google, AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10 (A)
- **Detect:** Not observable from outside. Attest the baseline and the method.
- **Evidence kept:** The attestation, its date and the baseline described.
- **Bands:** 4 — a before-and-after baseline exists for the key pages. 2 — one-off checks. 0 — none.
- **Note:** The before-and-after change is the clearest single demonstration of what a fix was worth.
- **Fix:** Pick the key pages and questions, score the answers now, and again after each round of fixes.
- **What changed in 12.0:** Reframed.
- **Replaces:** BP-8
- **Review by:** 2027-04-18

### MSR-7 — Are you set up in Google Search Console and Bing Webmaster Tools, and do you read their AI reports?

- **Question:** Are you set up in Google Search Console and Bing Webmaster Tools, and do you read their AI reports?
- **Not scored**
- **Applicability:** always
- **Verification:** auto-partial
- **Effort:** small
- **Fixed by:** Search specialist, Operations
- **Evidence:** AI product
- **Measures:** You tell us whether both tools are verified and whether you use the AI reports.
- **Why this matters:** Verify your site in both Google Search Console and Bing Webmaster Tools, and read their AI reports. Bing's index feeds several AI products. [Bing Webmaster Tools](https://www.bing.com/webmasters/about): Bing's own webmaster tools page, worth verifying because its index feeds several AI products.
- **Sources:** [Bing Webmaster Tools](https://www.bing.com/webmasters/about), undated (A); Bing AI Performance report, 2026-02-10 (address to confirm; grade to confirm); Google generative AI performance report, 2026-06 (address to confirm; grade to confirm)
- **Detect:** Look for `google-site-verification` and `msvalidate.01` meta tags, or DNS TXT verification records. Whether anyone reads the alerts and the AI reports must be attested.
- **Evidence kept:** The verification found for each tool, and the attestation if one was given.
- **Bands:** 4 — both verified, sitemaps submitted, AI reports read by a named person. 3 — both verified; submission and reading unconfirmed. 2 — one verified. 0 — neither.
- **Note:** Bing's AI Performance report (2026-02-10) and Google's generative AI performance report (2026-06) now exist. Clients frequently have Search Console and no Bing property at all.
- **Fix:** Verify both, submit the sitemaps, and route the alerts and AI reports to a person.
- **What changed in 12.0:** Adds Bing's AI Performance report and Google's generative AI report.
- **Replaces:** BP-9
- **Review by:** 2027-04-18

### MSR-8 — Does your page hold still while it loads?

- **Question:** Does your page hold still while it loads?
- **Not scored**
- **Applicability:** always
- **Verification:** auto
- **Effort:** medium
- **Fixed by:** Front-end developer
- **Evidence:** Scanner-listed (Lighthouse)
- **Measures:** We measure how much the page shifts while it loads.
- **Why this matters:** An agent that acts from a screenshot clicks where a button was, so a page that moves under it makes it miss. [Chrome for Developers, Lighthouse layout stability](https://developer.chrome.com/docs/lighthouse/agentic-browsing/layout-stability): Lighthouse reports layout shift in its agentic browsing category because agents work from screenshots and coordinates.
- **Sources:** [Chrome for Developers, Lighthouse layout stability](https://developer.chrome.com/docs/lighthouse/agentic-browsing/layout-stability), 2026-10-18 (A); [web.dev, Cumulative Layout Shift](https://web.dev/articles/cls), 2024 (A)
- **Detect:** While rendering each page, record the worst burst of layout shifts that no click caused, as Lighthouse does (shifts within a second of each other, in a window of at most five seconds), before any scrolling. A page is good at 0.1 or less.
- **Evidence kept:** Per page: the layout shift measured and whether it is good.
- **Bands:** Default coverage rubric over the pages rendered, where a page counts as present and correct at a layout shift of 0.1 or less.
- **Note:** Shown and never scored: it is one lab reading from one load, which varies between loads, and no AI product is documented reading it.
- **Fix:** Give images and embeds a width and height, reserve room for banners and late content, and do not insert content above what a visitor is looking at.
- **What changed in 12.0:** New test. No points.
- **Review by:** 2027-04-18

## Retired tests

Six Index 11 tests have no Index 12 section. Each keeps its row in the crosswalk, so an old ID still answers the question of what happened to it. Their IDs are never reused.

| Index 11 ID | The question it asked | Why it retired |
|---|---|---|
| AIR-1.5 | Can a person read your AI policy? | Crawlers ignore comments by design. A plain-language note in `robots.txt` is documentation for people, and nothing documents anyone reading it. |
| AIR-3.7 | Can an agent search your site without a search box? | Google removed the sitelinks search box in November 2024 and its documentation with it, and no other consumer of `SearchAction` was found. |
| LI-1 | Are your step-by-step pages marked up as steps? | Google removed `HowTo` rich results in 2023. |
| LI-4 | Do you document how your content is made and corrected? | No consumer of `publishingPrinciples` was found. |
| BP-2 | Can an agent find your key buttons again after a rebuild? | Nothing documents agents using `data-*` attributes to find an element again. |
| BP-4 | Do you capture visits whose referrer was stripped? | No evidence was found for the claim that server-side tagging recovers a stripped referrer. |

## What 100 means

A site scoring 100 has, at minimum:

- **Reach:** the search crawlers of every major assistant reaching real content, in `robots.txt` and at the edge, with page settings that let an assistant quote it.
- **Read:** every substantive fact present in the first server response, a clean and finite URL space, honest sitemap dates, Markdown copies that are advertised and served on request, and pages built from real structure with the answer near the top.
- **Understand:** a site that says who it is, markup that matches the page, authors with pages of their own, honest and visible dates, a trail that shows where each page sits, and any paywall declared.
- **Act:** forms an agent can read, no CAPTCHA in the way of browsing, and a described API where one exists.

Beside the hundred, a thorough site also has a deliberate and consistent position on what AI may do with its content (Posture), and the measurement to see what assistants do with it (Measurement). Neither moves the number.

Almost no site will score 100, and that is the point. The Index is a target to move toward, not a bar to clear. A client who moves from 41 to 72 in one engagement has a number they can take to their board — which is worth considerably more to them than a perfect score they will never reach.

We hold ourselves to the standard with a reference site. [reference.readinessindex.io](https://reference.readinessindex.io) is a hand-built implementation of the Index, and we do our best to keep it a working example of what a high score looks like: when a test asks for something, you can open the reference site and see it done. We scan it every night with the same scanner we run for everyone else, and we publish the result. The latest score, and the points it is still missing, are on [the reference scan](https://readinessindex.io/reference-scan).

## What the Index deliberately does not measure

We keep this list public because leaving it out would be dishonest.

- **Whether the content is any good.** Structure, not substance.
- **Whether the models actually cite the site.** That is answer-share monitoring, a different instrument on a different cadence. MSR-5 asks whether you run it.
- **Traditional SEO performance.** Rankings, backlinks, and Core Web Vitals are real, and they are not this.
- **Accessibility conformance.** Several tests overlap with WCAG, happily. This is not a WCAG audit and must not be sold as one.
- **Security posture.** We probe bot handling at the edge. We do not test the site's defenses.
- **Your rights choices.** Which training crawlers you allow, what you license and how you reserve your rights are shown under Posture and never scored. The Index measures machine reach, not approval.
- **Anything with no documented reader.** Markup and files that nothing is documented using are shown under Extras with no points, and a site that has them is credited in words.

## The crosswalk from Index 11

Index 11 named its tests `AIR-n.m`, `LI-n` and `BP-n`, after dimensions that no longer exist: `AIR-4.8` sat in *Crawl, index and licensing hygiene*, which Index 12 does not have. Index 12 names a test for the category it belongs to: `RCH`, `RED`, `UND`, `ACT`, `PST`, `EXT` and `MSR`.

**The crosswalk is permanent.** An Index 11 ID never stops resolving: a stored result, a bookmarked report, an exported `backlog.csv` or a ticket that quotes `AIR-4.8` can always be traced to the test it became. A retired test keeps its row, with the reason. **A new ID is never reused** for a different test. The machine-readable form of this table is `crosswalk.yaml`, published as `crosswalk.json`, and exports carry both IDs.

| Index 11 ID | Question it asked | Index 12 |
|---|---|---|
| AIR-1.1 | Can AI crawlers reach your site? | RCH-1 (scored) and PST-1 (training crawlers, not scored) |
| AIR-1.2 | Does your CDN let AI crawlers through? | RCH-2 (absorbs AIR-1.3) |
| AIR-1.3 | Is your page readable without a security challenge? | RCH-2 (merged into RCH-2 with AIR-1.2) |
| AIR-1.4 | Have you stated what AI may do with your content? | PST-2 |
| AIR-1.5 | Can a person read your AI policy? | Retired. Crawlers ignore comments by design. A plain-language note in `robots.txt` is documentation for people, and nothing documents anyone reading it. |
| AIR-1.6 | Are you allowing assistants to quote you? | RCH-4 |
| AIR-1.7 | Does this page declare its real address? | RCH-3 |
| AIR-1.8 | Is your page structured so a machine can follow it? | RED-13 |
| AIR-1.9 | Do your headings tell a clear story? | RED-14 |
| AIR-1.10 | Do you publish a guide for AI assistants? | EXT-1 (absorbs LI-7) |
| AIR-1.11 | Can a machine tell what your organization is? | EXT-5 |
| AIR-1.12 | Can a machine be certain it is you? | UND-10 |
| AIR-1.13 | Can a machine find out who you are? | UND-1 |
| AIR-2.1 | Does your content show up without JavaScript? | RED-1 |
| AIR-2.2 | Is content behind tabs and accordions already in the page? | RED-2 |
| AIR-2.3 | Are your tables real tables? | RED-15 |
| AIR-2.4 | Can a model link straight to a section of your page? | RED-16 |
| AIR-2.5 | Do your images say what they show? | RED-17 |
| AIR-2.6 | Are your key facts written as text? | RED-18 |
| AIR-3.1 | Is your structured data built from your content, not typed in by hand? | EXT-6 |
| AIR-3.2 | Does each page say where it sits in your site? | UND-7 |
| AIR-3.3 | Does your markup describe what you actually publish? | UND-2 |
| AIR-3.4 | Is your FAQ markup made of real questions and answers? | EXT-7 |
| AIR-3.5 | Do you say what a page is about and whether it is free to read? | UND-9 |
| AIR-3.6 | Are your prices and offers in your markup, and current? | UND-3 |
| AIR-3.7 | Can an agent search your site without a search box? | Retired. Google removed the sitelinks search box in November 2024 and its documentation with it, and no other consumer of `SearchAction` was found. |
| AIR-3.8 | Does your structured data actually validate? | UND-11 |
| AIR-4.1 | Have you published your licensing terms in a form machines can read? | PST-3 (absorbs AIR-4.2) |
| AIR-4.2 | Do your licensing terms travel with your content? | PST-3 (merged into PST-3 with AIR-4.1) |
| AIR-4.3 | Can you prove a visiting bot is who it says it is? | EXT-3 |
| AIR-4.4 | Do your PDFs and images carry their own crawl rules? | RED-5 |
| AIR-4.5 | Do your missing pages say they are missing? | RED-6 |
| AIR-4.6 | Do your redirects go straight to the destination? | RED-7 |
| AIR-4.7 | Are your filters and calendars kept from swallowing a crawl? | RED-4 |
| AIR-4.8 | Can a crawler trust the dates in your sitemap? | RED-3 |
| AIR-4.9 | Is your sitemap organized by type of content? | RED-8 |
| AIR-4.10 | Can a crawler reach page two and beyond? | RED-9 |
| AIR-5.1 | Do your authors have real pages with real credentials? | UND-4 |
| AIR-5.2 | Do your bylines point at a person, not just a name? | UND-5 |
| AIR-5.3 | Does health, legal and financial content name its reviewer? | EXT-8 |
| AIR-5.4 | Are your published and modified dates honest? | UND-6 |
| AIR-5.5 | Can a machine follow your citations back to their sources? | EXT-9 |
| AIR-5.6 | Can your images prove where they came from? | EXT-10 |
| AIR-6.1 | Do you describe your public API in a spec an agent can read? | ACT-3 |
| AIR-6.2 | Do you publish agent capabilities where agents look for them? | EXT-2 |
| AIR-6.3 | Can an agent tell what each form field is for? | ACT-1 |
| AIR-6.4 | Can an agent search and filter without meeting a captcha? | ACT-2 |
| AIR-7.1 | Do you offer a clean Markdown version of your pages? | RED-10 |
| AIR-7.2 | Does each page point to its Markdown version? | RED-11 |
| AIR-7.3 | Can a machine ask your URL for Markdown? | RED-12 (absorbs AIR-7.4) |
| AIR-7.4 | Are your alternate versions served from the cache? | RED-12 (merged into RED-12 with AIR-7.3) |
| LI-1 | Are your step-by-step pages marked up as steps? | Retired. Google removed `HowTo` rich results in 2023. |
| LI-2 | Have you flagged the part of each page that answers the question? | EXT-11 |
| LI-3 | Do you tell search engines the moment something changes? | EXT-12 |
| LI-4 | Do you document how your content is made and corrected? | Retired. No consumer of `publishingPrinciples` was found. |
| LI-5 | Can an assistant ask your site a question directly? | EXT-13 |
| LI-6 | Can an assistant call your catalog as a tool? | EXT-4 |
| LI-7 | Do you offer your full text in one file? | EXT-1 (merged into EXT-1 with AIR-1.10) |
| BP-1 | Can a task like applying or donating be finished without JavaScript-only clicks? | MSR-1 |
| BP-2 | Can an agent find your key buttons again after a rebuild? | Retired. Nothing documents agents using `data-*` attributes to find an element again. |
| BP-3 | Can you count visits that come from AI assistants? | MSR-2 |
| BP-4 | Do you capture visits whose referrer was stripped? | Retired. No evidence was found for the claim that server-side tagging recovers a stripped referrer. |
| BP-5 | Do you keep your crawler logs long enough to use them? | MSR-3 |
| BP-6 | Do you get a regular report on AI crawler activity? | MSR-4 |
| BP-7 | Do you ask the same questions of AI models every month? | MSR-5 |
| BP-8 | Have you measured how accurately a model reads your page? | MSR-6 |
| BP-9 | Are you verified in Google Search Console and Bing Webmaster Tools? | MSR-7 |

## Versioning and change control

The Index version is independent of the scanner version. Both appear in every result file.

Bump the **minor** version for new tests, clarified detection, or corrected band anchors. Bump the **major** version for any weight change, gate change, or scoring-model change — anything that makes two scores non-comparable.

A test ID is never reused for another test, and the crosswalk is permanent.

Never silently re-weight. A client's trend line is the most valuable thing the Index produces, and one quiet weight change destroys it. When a major bump lands, re-score the last run under both versions and show the difference.

### Changelog

#### 12.0 — 2026-10-18

**A MAJOR bump. Scores computed under Index 12 cannot be compared with scores computed under Index 11, in either direction.** Every weight moved, the structure of the score changed, 38 tests carry the hundred points where 51 did, and every test has a new ID. A site that scored 70 under 11.5 and scores 70 under 12.0 has not stayed the same: the two numbers answer different questions. Every site's trend line carries one marker, *Index changed from 11.5 to 12.0*, and benchmarks compare only sites within a major version.

1. **Four categories replace seven dimensions.** **Reach** (4 tests, 25 points), **Read** (19 tests, 35 points), **Understand** (11 tests, 25 points) and **Act** (4 tests, 15 points). Primary Indicators is now Reach. The seven crawl-housekeeping tests that sat beside it (sitemaps, redirects, missing pages, filters, pagination, file rules, media sitemaps) moved to Read, where they are about finding pages and not about being let in, which is why Read carries more tests than Reach and no test lost weight on that account.
2. **Seventy-two tests, 38 of them scored.** Index 11 had 67: 51 scored, 7 leading indicators and 9 best practices. Index 12 has the 38 scored tests and three unscored groups: **Posture** (6), **Extras** (20) and **Measurement** (8). Six tests retire. Fourteen are new.
3. **Every test carries an evidence label and graded sources.** The labels are AI product, Search index, Standard only, None found and Practice, and the grades are A, B and C. A test is scored only if it has documented use, or is labeled Practice. Each test names its sources and a review date six months out. See *What counts as evidence*.
4. **The free scan is the Reach scan.** It runs RCH-1 to RCH-4 from one page and the site's front-door files, with no browser, and reports points out of 25. The Primary Indicators scan ran thirteen tests. The posture panel, `llms.txt` and the other unscored items are shown from the same fetches.
5. **Gates are RCH-1 and RCH-2.** RCH-1 reads the search crawlers of OpenAI, Anthropic, Perplexity, Google, Bing, Apple, Meta, Amazon and Mistral by name, where AIR-1.1 read ten agents, six of them training or opt-out agents. RCH-2 merges AIR-1.2 and AIR-1.3 into one edge test that also catches a challenge page. A training block never gates and never costs a point.
6. **Training crawlers and Content Signals leave the score.** Which training crawlers a site allows is shown in PST-1, a statement about AI use in PST-2, a license in PST-3, a text and data mining reservation in PST-4 and whether the statements agree in PST-5. A choice is not a defect. No company is documented honoring Content Signals or RSL, which is why they carry no points. PST-1 also names the tools that act on a person's request and may ignore `robots.txt`, and lists xAI's Grok crawler names as observed and undocumented: xAI publishes no crawler documentation and no list of its addresses.
7. **Google's AI control becomes a prompt.** Google lets owners switch a site out of its AI answers. A scan cannot see the setting, so PST-6 asks the owner to confirm it and never scores it. Its two points went to RCH-1 and RCH-4 in the first 12.0 draft, and the weights have since moved again; see decision (10).
8. **Six tests retire.** AIR-1.5 (crawlers ignore comments by design), AIR-3.7 (Google removed the sitelinks search box in November 2024), LI-1 (Google removed `HowTo` rich results in 2023), LI-4 (no consumer found), BP-2 (nothing documents agents using data attributes) and BP-4 (no evidence for the claim).
9. **Six new tests.** RED-19 (does each page give its answer near the top), UND-8 (does the hidden page code say the same as the visible text), ACT-4 (do your buttons, links and menus have names an AI agent can read), PST-4 (TDMRep), PST-5 (do the statements about AI use agree) and PST-6 (Google's AI control, as a confirm prompt).
10. **Twelve scored tests moved out of the score, 22 points between them, because no consumer is documented.** AIR-1.4 (now PST-2), AIR-4.1 and AIR-4.2 (PST-3), AIR-1.10 (EXT-1), AIR-6.2 (EXT-2), AIR-4.3 (EXT-3), AIR-1.11 (EXT-5), AIR-3.1 (EXT-6), AIR-3.4 (EXT-7) and AIR-5.3, AIR-5.5 and AIR-5.6 (EXT-8 to EXT-10) are shown without points. A site that has them is credited in words. The points went to tests with documented use: RCH-1, RCH-2, RCH-4, RED-1, RED-2, UND-3, UND-6, UND-9, ACT-1 and ACT-2 each weigh more than in 11.5, and ACT-4 is new. AIR-1.12 and AIR-3.8 stay in the score at two points each as UND-10 and UND-11, because Google documents a reader for each: `sameAs` as a recommended Organization property, and the rule that invalid markup is not eligible for its features.
11. **Practice tests are one point each, seven in all.** RED-13 to RED-19 are sound practice with no documented consumer. Index 11 gave several of them two points.
12. **Detection changed in thirteen tests.** Per-crawler robots verdicts with group inheritance and Applebot's fall-back to the Googlebot rules (RCH-1); edge probes with the new crawler names (RCH-2); `noindex` and bot-specific page tags (RCH-4); the share of words missing from the first response (RED-1); text visible on load and not removed until a click (RED-2); the advertised Markdown address and the response headers (RED-10, RED-11, RED-12); price markup compared with the visible page (UND-3); distinct authors counted once (UND-4, UND-5); visible dates matched against the markup (UND-6); breadcrumbs required only where the site has a hierarchy (UND-7). Types Google has retired no longer count toward UND-2.
13. **New IDs, and a permanent crosswalk.** `AIR-n.m`, `LI-n` and `BP-n` give way to `RCH`, `RED`, `UND`, `ACT`, `PST`, `EXT` and `MSR`. Every Index 11 ID maps to what it became, in *The crosswalk from Index 11*. An old ID never stops resolving and a new ID is never reused. Exports carry both IDs.
14. **Decisions made before release.** (1) Google's AI-control setting leaves the score and is shown as a confirm prompt. (2) Practice tests are one point each. (3) Understand was set at 20 and Act at 5; it was 18 and 7 before decision (9), and decision (10) moved both again. (4) The free scan is the Reach scan. (5) Test IDs are new category IDs with a permanent crosswalk. (6) There are three unscored groups. (7) The 20,000-property census scan is discarded and the census is re-run from the start under Index 12. (8) Points moved off the tests that almost every site passes and onto the tests that tell sites apart, with every category total unchanged: RCH-1 from 15 to 10 and RED-1 from 15 to 13, RCH-2 from 8 to 13 and RED-2 from 5 to 7. Re-weighting the published Index 11.0 results of 921 sites showed RCH-1, RCH-4 and ACT-2 giving the average site about 22 of their 23 points, which lifted every score without separating anyone; the edge test, which the average site passes 40 percent of, tells sites apart far better and carries the same evidence. (9) Understand is 20 and Act is 5: sameAs and validation, which have a documented reader (Google's Organization and structured-data documentation), moved into the score as UND-10 and UND-11, paid for by ACT-2 3 to 1, UND-2 3 to 2 and UND-1 2 to 1; Reach stayed 30 and Read stayed 45 at that point. (10) Marker Y, 2026-10-18: Reach 25, Read 35, Understand 25, Act 15. Four categories stay; the proportions moved because Reach and Read carried 75 points while Act carried five. ACT-4 was added so Act has a substantive test beyond forms and CAPTCHAs, and the points moved off the tests nearly every site passes (RCH-4 5 to 3, RCH-1 10 to 8) and off Read's heaviest tests (RED-1 13 to 10, RED-2 7 to 5), with Understand led by dates (UND-6 4 to 6). The previous set, marker X (30/45/20/5), is tagged weights-x-30-45-20-5 and written in docs/WEIGHT-MARKERS.md. The free Reach scan runs RCH-1 to RCH-4 and reports out of 25. (12) Eight unscored tests (EXT-14 to EXT-20 and MSR-8) were added, 2026-10-18, so that Index 12 measures every check listed by Cloudflare's Agent Readiness score and Lighthouse's agentic browsing category: WebMCP, sign-in discovery, agent cards and skills, DNS-AID, agent payment protocols, a declared sitemap, accessibility-tree integrity and layout stability. They carry the new evidence label Scanner-listed and no points, because a scanner listing a check is not an AI product reading it; no score moves. The table in Coverage of published scanners shows which of their checks each answers and which are only partly covered or not covered. (11) Act was nearly free in the pilot (2026-10-18, 180 S&P 500 sites): the median site earned 90 percent of its 15 points. ACT-4 now passes a page at 1 percent unnamed controls, not 5, which takes full marks from 121 of 166 sites to 74 and spreads the bands from 0 to 4; and ACT-2 now applies only where the site has search or filtering, so the census no longer counts the 113 of 180 sites with none as passing it. Weights are unchanged. Together the two moved the pilot's median Act share from 90 to 65 percent and its median score from 59 to 56.5. (13) A sampled address that answers with a PDF or another non-HTML document is no longer read as an HTML page: it nested almost a thousand levels, failed three pilot scans and fed millions of characters of noise to the text checks. Applied to the pilot's stored evidence it set aside 18 pages on 10 of 195 sites and moved those scores by 0 to 3 points, 1 at the median.

Re-score a site's last run under both versions and show the two numbers side by side before anyone compares them; neither is wrong.

#### 11.5 — 2026-10-11

**A minor bump: one more vertical for AIR-3.3. No weight, band or scoring-model change,
and no score computed under 11.4 moves.**

AIR-3.3 is scored against the client's declared vertical, and school districts had no
honest one. Higher Education's set (`Course`, `EducationalOccupationalProgram`,
`CollegeOrUniversity`, `EducationEvent`) describes a college, and marking a district
against it would score it for not being one. **K-12 Education** is added with its own
expected set: `EducationalOrganization`, `School`, `Event`, `EducationEvent` and `Course`.

The fifteen existing verticals are **byte-for-byte unchanged**, in their stored values and
their type sets, so a site scored under 11.4 scores identically under 11.5. A site with no
vertical is unchanged in every respect: still *not declared*, still out of the denominator.

#### 11.4 — 2026-10-09

**A minor bump: clarified detection. No weight, gate or scoring model changed, and a
site's score under 11.4 is within one point of its score under 11.3, only through AIR-4.3.**
The scores are comparable, not identical.

1. **AIR-4.3 cites the draft that is current.** The standard pointed at
   `draft-meunier-web-bot-auth-architecture`, which was renamed and folded into
   `draft-ietf-webbotauth-httpsig-protocol` (revision -00, September 2026, a working group
   draft that expires 2027-03-05). `Detect` and `Fix` now use its terms: `Signature-Agent`
   is a dictionary of HTTPS URLs, a signed request covers `@authority` and the
   `signature-agent` member with `created`, `expires` and `tag="web-bot-auth"`, and the key
   directory is a JSON Web Key Set at `/.well-known/http-message-signatures-directory`.
2. **What counts as a key directory is stricter, and a new band says so.** Any `200` at that
   address used to score 4, an HTML page included. Now band 4 is a directory that answers
   `200` at the address itself, with no redirect, as
   `application/http-message-signatures-directory+json`, with a key set that has at least one
   key. A key set served through a redirect or as another media type, which a verifier
   following the draft refuses, scores 3. Something at the address that is not a key set
   scores as no directory: 2 when the edge tells AI agents apart by user-agent, otherwise 0.
3. **What moves.** Only a site that publishes a key directory: from 4 to 3 (a quarter of a
   point) when it is served the wrong way, and from 4 to 2 or 0 (up to one point) when what
   is at the address is not a key set. Nothing else changes.

#### 11.3 — 2026-10-08

**A minor bump: no weight, gate, band or detection rule changed, and a score under
11.3 is identical to the same site's score under 11.2.** Like 11.2 it changes how the
Index explains itself.

1. **Every entry now says who typically fixes it.** A `Fixed by` bullet follows
   `Effort` on all 51 scored tests and on the tests beside them that are run but never
   scored: one to three of six roles, the first being who typically does or drives the work. A new
   section, *Who fixes it*, defines the roles. They are guidance for the reader of a result, so a failed firewall rule and a thin
   About page do not land on the same desk, and they carry no points.
2. **The roles are written here and nowhere else**, as the questions are: a scanner
   or a report that names who fixes a test reads it from this document.

#### 11.2 — 2026-10-03

**A minor bump: no weight, gate, band or detection rule changed, and a score
under 11.2 is identical to the same site's score under 11.1.** The revision is to
how the Index explains itself.

1. **Every test now carries a plain-language `Question` and a `Why this matters`.**
   The question is the first bullet of each entry. `Why this matters` follows
   `Measures` and has a description, a link to a source that is not us, and one
   sentence on why that source is worth citing. Until now only the thirteen
   Primary Indicators had a question, and the rest of this was kept outside the
   document, so what a report said about a test and what this document said could
   differ. They cannot now: a scanner reads those words from here.
2. **Every test has them**, the Leading Indicators and Best Practices that never
   count toward the score included. Fifty-four questions are new.
3. **The Primary Indicators section says why those thirteen are the quick scan.**

#### 11.1 — 2026-09-30

**A minor bump: no weight, gate or model changed, and scores from 11.0 and 11.1
remain comparable. They are not identical.** Two tests that a quick scan held
below their top band now reach it, so a Primary Indicators score can rise by up
to one point against 11.0 with nothing changed on the site. A full scan can
move by at most the same amount, and only through AIR-1.10.

1. **AIR-1.10 no longer asks whether `llms.txt` is generated.** The question
   could not be answered from outside, so the test was capped at band 3 until a
   client attested to it, and a valid, current file that nobody could vouch for
   lost half a point. It is `auto` now. The bands measure what a scanner can
   see: valid and covering at least 75% of the sitemap is band 4; valid but
   below that is band 3; the old floor at 25% (band 2, "clear staleness") is
   gone, so a valid file with working links scores 3 however little it lists.
   The Drupal module is reported as evidence only. AIR-1.10 leaves the list of
   tests an attestation can lift.
2. **The Primary Indicators scan resolves `sameAs` links**, up to five,
   tier-1 identifiers first. AIR-1.12 used to be held at band 3 in a quick scan
   because those hosts belong to somebody else and requesting them tells them
   which site is being audited. That is accepted, and bounded by the limit. With
   both held-back tests released, the thirteen can earn their full 30 points.

#### 11.0 — 2026-09-24

**Scores computed under 10.x cannot be compared with scores computed under
11.0.** Seventeen tests left the hundred, one dimension was removed, every
remaining test was renumbered, and eleven points moved. Every number moved.

1. **Seventeen tests were returning the same answer for every site.** Measured,
   not guessed: across every production scan on record, seventeen tests in
   dimensions 2 through 8 had never once produced a different result. A test
   that cannot separate two sites is not measuring anything; it is a constant
   added to every score, and sixteen points of the hundred were being handed out
   for nothing. They are all still run and still reported — as **Leading
   Indicators** (LI-1 through LI-7) and **Best Practices** (BP-1 through BP-9),
   beside the hundred rather than inside it.

2. **The hundred is 51 tests, and every one of them is observable.** The Index
   no longer has a single scored test in `manual` mode. What the scanner cannot
   see for itself is reported as a best practice; what carries points is
   something the crawl establishes. `auto-partial` remains for the fifteen
   points held below band 4 pending a confirmation only the client can give.

3. **Dimension 8, Measurement and instrumentation, was removed.** Whether a
   channel group exists in somebody's analytics, whether their access logs are
   queryable, whether a prompt panel runs monthly — none of it is visible from
   outside, and all of it was scoring the same everywhere. It is now the Best
   Practices family, which is where advice that a scan cannot verify belongs.

4. **Seven dimensions, reweighted.** Primary Indicators 28 → **30**; Rendering
   and Extraction **15**; Structured Data and the Entity Graph 14 → **15**;
   Crawl, Index and Licensing Hygiene 14 → **12**; Authorship, Provenance,
   Freshness 8 → **12**; Agent Interfaces 7 → **8**; Alternate Representations 7
   → **8**. The eleven points freed by the removals went to tests that already
   separate sites rather than into a new one.

5. **AIR-3.8 measures the markup instead of asking about the build.** It used to
   ask whether schema validation ran in CI — unobservable, and so worth two free
   points to everybody. It now parses every structured-data block on every
   sampled page, holds each node against the properties its declared type needs,
   and checks that dates are ISO 8601, that URLs are absolute and that a price
   carries a currency. Worth 2 points now rather than 1, and AIR-3.3 gave up
   the point to pay for it.

6. **Everything is renumbered, with no gaps.** Removing a dimension and moving
   seventeen tests out of the hundred left holes across every family, and an id
   that means nothing is worse than an id that changed. There is no mapping
   table on purpose: the numbers are not comparable across this bump, and a
   table would invite somebody to pretend they are.

#### 10.4 — 2026-09-24

**Two dimensions renamed. No weight, band, gate or scoring-model change, and no
score computed under 10.3 moves.**

Dimension 1 is now **Primary Indicators**, and dimension 9 is now **Leading
Indicators**.

1. **"First contact" named a moment; the dimension measures a condition.** It
   holds the thirteen highest-signal tests, pulled from six other dimensions
   because each can be answered from a single page — which is also what makes
   them the free scan's thirteen. "Primary" says what they are to the reader:
   the first things to get right, and the ones that decide whether anything
   below them can be read at all. The free scan takes the same name, so the
   page somebody lands on and the dimension it reports are no longer two
   products with one set of tests.

2. **"Unscored leading indicators" said the same thing twice.** Leading
   indicators are unscored by definition — that is what the tier means, and the
   dimension's own section has said so since 10.0. The word was carried in the
   name to prevent a misreading that the zero in the weight column already
   prevents.

**Scores are comparable across this bump.** Both dimensions keep their ids,
their weights, their tests and their band anchors. A result scored under 10.3
and the same evidence scored under 10.4 produce the same number; only the two
labels differ. Earlier changelog entries keep the names in use at the time,
because they are a record of what happened rather than a description of the
Index today.

#### 10.3 — 2026-09-21

**Ten more verticals for AIR-3.3, and an explicit "other". No weight, band or
scoring-model change, and no score computed under 10.2 moves.**

AIR-3.3 is scored against the client's declared vertical, and five were
published: higher education, healthcare, nonprofit, government and research.
Every other kind of organization had nothing to declare, so the test left their
denominator as *not declared* — correct, but it meant an ecommerce site or a
manufacturer could never be measured on the one test about modelling what they
actually contain.

Nine are added — ecommerce, financial services, hospitality, local services,
manufacturing, media, professional services, real estate and SaaS — each with
its expected type set above. The five that existed are **byte-for-byte
unchanged**, in both their stored values and their type sets, so a site scored
under 10.2 scores identically under 10.3.

`other` is the tenth, and it is deliberately different: it carries no expected
type set. A client who tells us their industry is not on the list has told us
something true, and marking them against types the Index never defined for them
would be scoring them for our own gap. AIR-3.3 is therefore **not scored** for
`other` and the report says why, with an invitation to tell us the industry so
a set can be added.

A client with no vertical at all is unchanged in every respect: still *not
declared*, still out of the denominator, still the same score.

#### 10.2 — 2026-09-17

**Corrected detection for AIR-1.2. No weight, band or scoring-model change, but a
site's AIR-1.2 result can move, because the old one was measuring the wrong thing.**

The edge probe sent each agent's bare token as its entire User-Agent header — a
literal `User-Agent: GPTBot`. No crawler sends that. Edge protection keys on the
real signature: a browser-shaped prefix, `compatible; <Token>/<version>`, and the
vendor's contact URL. So the probe walked straight past the rules it exists to
find, and a site whose CDN was turning GPTBot away scored as though it were
letting GPTBot in.

Measured on readinessindex.io on 2026-09-17, against an edge running Cloudflare's
AI-crawler blocking: probing as `GPTBot` and `CCBot` was served 200, while the
real strings for the same two agents were served 403 by the same edge on the same
request path. The Index reported 2 of 8 agents blocked. Four were.

AIR-1.2 is a gate. Under-detecting here does not shade a number slightly — it
hands a site the one verdict the Index exists to raise, *AI assistants can reach
you*, when they cannot.

1. **The probe now sends each agent's real User-Agent string**, listed in
   `PROBE_USER_AGENTS` with its provenance: OpenAI and Perplexity publish theirs
   verbatim, and Anthropic, Common Crawl and ByteDance do not, so those three are
   the canonical observed forms and are marked as such.
2. **Findings still name the bare token.** It is what a reader recognises and what
   they would write into robots.txt; the full string belongs on the wire, not in
   the report.
3. **Version drift is expected and harmless.** OpenAI moved GPTBot from 1.2 to 1.4
   without announcement. Edge rules match the shape and the token rather than the
   digits, so a stale version still probes honestly — a bare token does not.

A site that passed AIR-1.2 under 10.1 and fails it under 10.2 was failing all
along. Re-scan before concluding anything from a comparison across this boundary.

#### 10.1 — 2026-09-17

**Clarifications and two scanner switches. No weight, band or scoring change — a
site scored under 10.0 and the same site scored under 10.1 report the same number
from the same evidence.**

1. **Rounding is now stated in the specification**, in *Rounding, and the full
   accounting*. It always happened; it was never written down. Every points figure
   shown to a reader is a whole number, roughly a third of a run's rows round to get
   there, and the score is computed from the exact contributions and rounded exactly
   once at the end — so a report's printed rows do not sum to its printed score.
   Implementers must publish the arithmetic and must never compute a score from
   figures they have already rounded.
2. **Every result carries a full accounting**, reachable from the foot of the report:
   every test, its weight, its band, `weight × band ÷ 4` written out, its exact
   contribution, the figure printed instead, and the final division. It recomputes
   the score from weight and band rather than reprinting the stored figure, so a
   disagreement between the accounting and the report is visible rather than silent.
3. **Resolving external identifiers has a rule of its own**, in *Resolving external
   identifiers*. A third party's availability is never a fact about the client's
   site: a timeout against ORCID records one link unconfirmed, and must neither fail
   the scan nor score the client down. What the audit disclosed, and to whom, is
   recorded in the evidence.

#### 10.0 — 2026-09-17

**Every test is scored.** Nothing outside dimension 9 leaves the denominator any
more, on any run a person is shown. A test the engine cannot band from evidence
resolves to a band by rule instead of dropping out — full marks where the site has
none of the thing, a held band 2 where the answer is invisible from outside, zero
where the test it builds on is not passing. The full model is in *Applicability and
N/A* above.

**Scores are not comparable across this boundary, in either direction.** Both halves
of the fraction moved: the denominator is now the full 100 on every site, and tests
that contributed nothing now contribute a band. The reference fixtures show the size
of it — the clean site reads 84 of 100 where it read 93 of 69, and the weak site 50
where it read 38 of 55. A site that scored under 9.x and re-scores under 10.0 must
have both numbers shown side by side, per the versioning rule, and neither number is
wrong: they are answers to two different questions.

1. **The rule.** Applicability resolution is unchanged — it still decides whether a
   test has anything to find. What changed is what happens to its verdict:
   `precondition_not_met`, `vertical_mismatch` and `dependency_not_applicable` score
   4; `not_declared_in_engagement_profile`, `no_attestation` and
   `insufficient_evidence` are held at 2; `dependency_not_met` scores 0. Two reasons
   are deliberately not in that table — `check_not_implemented` and `scanner_error`
   both mean *we* failed, not the site, and inventing a band for our own defect would
   hide it.
2. **Held is not earned.** A held test carries `band_capped_at: 2` and the cap reason
   *awaiting confirmation from your team*, exactly as an `unattested_ceiling` always
   has, so `earnable_points` falls and confirming it can still move the score. A
   report that showed 100 points available where only 87 could be reached would be
   selling points nobody can buy.
3. **The backlog now ranks by what is reachable, not by raw weight.**
   `points_available` is `earnable − earned` rather than `weight − earned`. This
   fixes an older bug in passing: a test held by a first-run cap or an attestation
   ceiling used to promise its full remaining weight at the top of the backlog, and
   no amount of work on the site could collect it.
4. **Every scored row carries evidence.** A test banded by this rule records what was
   looked for, what came back, and what it scored — so *we found none of this* is
   checkable in the same place as any other finding, rather than being an assertion.
5. **Two exemptions, both for runs nobody is handed.** The quick scan (thirteen
   tests, a fixed published ceiling) and the census (population statistics, where our
   blind spot must not be reported as an industry result) keep the 9.x behavior via
   `score_everything: false`.

**Why now.** The self-serve full scan made the old model's cost impossible to ignore.
Nobody filling in a URL box declares an engagement profile, so a real report came
back with 52 of its 100 points unassessed, 19 of them for want of business facts
alone — and the rows that carried them told the reader neither a result nor anything
to do. The Index is named for a hundred points. It should score them.

#### 9.0 — 2026-09-16

**A new dimension, not a new score.** Every `leading`-tier test — measured
and reported since 4.0, never scored — moves out of the dimension it
happened to be filed under and into its own: **#9 · Unscored Leading
Indicators**, declared at 0 of the 100 points, last in dimension order.
Nothing about *why* a leading test doesn't count changes; what changes is
that it no longer sits inside a dimension whose own heading implies every
one of its tests carries weight. A reader adding up a dimension's own rows
now gets that dimension's own declared total, every time — before this,
seven of those rows didn't, because they were leading tests hiding in
plain sight in dimensions 3, 4, 5, and 6.

1. **Six tests move, ten more renumber to close the gaps they leave.**
   `tests.yaml` (then `checks.yaml`) stays grouped and numbered by dimension (6.0's own rule),
   so a check moving dimension is a check getting a new id:
   - AIR-3.5 (HowTo) → AIR-9.1, AIR-3.6 (speakable) → AIR-9.2. The four that
     followed them close the gap: AIR-3.7 → AIR-3.5, AIR-3.8 → AIR-3.6,
     AIR-3.9 → AIR-3.7, AIR-3.10 → AIR-3.8.
   - AIR-4.11 (IndexNow) → AIR-9.3. Last in its dimension; nothing behind it
     to renumber.
   - AIR-5.7 (editorial policy) → AIR-9.4. Also last; same reason.
   - AIR-6.1 (NLWeb endpoint) → AIR-9.5, AIR-6.3 (domain MCP server) →
     AIR-9.6. The seven that followed close the gap: AIR-6.2 → AIR-6.1,
     AIR-6.4 → AIR-6.2, AIR-6.5 → AIR-6.3, AIR-6.6 → AIR-6.4, AIR-6.7 →
     AIR-6.5, AIR-6.8 → AIR-6.6, AIR-6.9 → AIR-6.7.
   - The one dependency naming an id that moved is updated to match: the
     test now numbered AIR-6.1 (formerly AIR-6.2) required AIR-6.1 before
     this change; it requires AIR-9.5 now, the new number for the same
     test it always depended on.
2. **No weight, band, or score changes.** Every test kept its own weight;
   every dimension holding only core tests kept its own declared total,
   because removing a test that never contributed to it changes nothing
   about the sum. A site scored under 8.0 and the same site scored under
   9.0 report identical numbers everywhere except which id and dimension
   two handfuls of findings print under — the same guarantee 6.0 made for
   the same reason.
3. **A related bug, caught while building this: a dimension's own
   applicable/earned points included any leading test inside it.** Scoring
   itself was never affected — `score_run`'s own total already excluded
   leading tests — but `_dimension_results` didn't apply the same
   exclusion, so a dimension holding one could show a share-earned number
   diluted by a test that was never part of its denominator. Dimension 9
   would have inherited this as a dimension that could show nonzero earned
   points against a declared weight of zero — negative points "left,"
   on the one dimension where that number most needs to read as exactly
   zero. Fixed in the same change: leading tests are now excluded from a
   dimension's own applicable and earned totals, everywhere they're
   computed, not only in the overall score.

#### 8.0 — 2026-09-16

**A convention change, not a scoring one, bumped major because it touches
the one canonical dimension label everywhere it's used.** A dimension
heading now reads `#1 · First Contact · 13 tests · 28 pts` rather than
`13 checks · 28% weight` — the dimension's own weight, shown as points,
not re-expressed as a percent of the total (every other number on the
site already reads as points, and the percent was the odd one out). The
site's own word for what it audits is "test" now, not "check" — the nav,
the footer, the scan pages. Nothing is re-scored: a check's id, weight,
and band are exactly what they were; only what the page calls it changed.

#### 7.0 — 2026-09-15

**A major bump on both the letter and the spirit of the rule.** Seventeen
checks change weight, and for the nine that were at zero this is not
accounting — a check worth zero points cannot move a score, and now every
one of them can. Re-score before comparing a 7.0 result to anything earlier.

1. **No core check weighs zero.** The nine checks 5.0 rounded to zero on the
   100-point scale — `AIR-5.5`, `AIR-5.6`, `AIR-6.4`, `AIR-6.5`, `AIR-7.4`,
   `AIR-8.1`, `AIR-8.2`, `AIR-8.6`, `AIR-8.7` — each now carry at least 1
   point, funded by moving weight rather than by widening the scale. A check
   in the Index is a claim that something is worth measuring; a check worth
   nothing was a claim the number itself contradicted.
2. **Three dimensions could not fund their own floor.** *Agent interfaces*
   (9 checks) and *Measurement and instrumentation* (7 checks) each totaled
   fewer points than they have checks — mathematically, some of them had to
   be zero. Both dimensions' declared weight rises to match their own check
   count (5 → 7, and 3 → 7), every check in each now weighing exactly 1.
   *Alternate representations* funds its own zero-weight check from within
   its existing 5, plus 2 more for the same reason (5 → 7), landing at
   1/2/1/2/1 across its five checks rather than the flat 1 the other two
   dimensions reach.
3. **First contact funds the difference: 36 → 28.** The 8 points the other
   three dimensions needed come from here, not from *Structured data* or
   *Crawl, index and licensing hygiene* — First contact is still by far the
   heaviest dimension, and the two checks it gates on (`AIR-1.1`, `AIR-1.2`)
   keep their weight of 5 each unchanged; the reduction is absorbed by the
   other eleven, heaviest first, none dropping below 1.
4. **Dimensions are still declared in descending weight order** — see
   *Weights* — which is why *Alternate representations* lands at 7 rather
   than the 5 its own checks would otherwise need: dimension 7 must weigh at
   least as much as dimension 8, and dimension 8's own floor is 7.

#### 6.0 — 2026-09-11

**A major bump, on the letter of the versioning rule rather than its spirit,
same as 5.0.** No check's detection, band anchor, gate, or weight moved.
What changed is how a check is named.

1. **Every check is renumbered so its id prefix names its own dimension.**
   `AIR-1.1` through `AIR-1.13` are Dimension 1, `AIR-2.1` through `AIR-2.6`
   are Dimension 2, and so on through `AIR-8.7` — this reverses 5.0's
   decoupling (above), which let a check's id and its `dimension` field
   disagree. The registry (then `checks.yaml`, now `tests.yaml`) is now grouped and ordered by dimension, and
   `_validate_ids` enforces the ascending order that follows from it.
2. **The id prefix itself changes, from `AR-` to `AIR-`.** Every check id,
   every anchor (`#air-1.1`, not `#ar-1.1`), and every mention of a check
   anywhere the site or this document names one, uses the new prefix.
3. **A dimension has one canonical label, used everywhere one is named:**
   `#N · Title Case Name · N checks · W% weight` — for example,
   `#1 · First Contact · 13 checks · 36% weight`. The methodology page's own
   dimension headings and the checks list both follow it now.
4. **Nothing is re-scored.** A site scored under 5.0 and the same site scored
   under 6.0 differ only in which id and dimension label each finding is
   printed under, not in any check's verdict, weight, or band.

#### 5.0 — 2026-09-10

**A major bump, on the letter of the versioning rule rather than its spirit.**
Nothing here changes what a check detects or how a band is assigned — no
detection logic moved, no band anchor moved, no gate moved. What changed is
the accounting underneath the checklist, which is exactly the kind of change
the rule says must never happen silently.

1. **Weights are integers, on the same 100-point scale.** Every dimension
   total and every check weight is now a whole number, and the eight
   dimension totals still sum to exactly 100. That forces nine checks —
   `AIR-7.4`, `AIR-5.5`, `AIR-5.6`, `AIR-6.4`, `AIR-6.5`, and four of the five
   checks in *Measurement and instrumentation* — to round to zero: each was
   already worth less than half a point, and a 100-point scale has no
   smaller unit to give them. A check worth zero points cannot move a score.
   That is a known, accepted cost of staying on 100 rather than moving to a
   finer-grained scale, not an oversight — recorded here rather than left
   for someone to discover. The leading tier's own weights (measured, still
   never scored) round the same way, with a floor of 1 rather than 0: they
   describe a real practice worth naming even at the bottom of the scale.
   (Fixed in 7.0, below — every core check now floors at 1 too, by moving
   weight rather than by widening the scale.)
2. **A dimension is a field, not a naming convention.** The registry used to
   validate that a check's id prefix matched its `dimension` — `AR-2.3` (now
   `AIR-1.7`) had to live in dimension 2. That coupling is gone. A check's id
   is permanent from the day it is written; which dimension it is grouped
   under can move, and now does. (Reversed in 6.0, below — the id prefix is
   coupled to the dimension again, this time by renumbering the check rather
   than by validating against it.)
3. **First contact is a new dimension: exactly the 13 checks the free quick
   scan runs**, pulled out of six different dimensions they used to sit in.
   The quick scan's own weight and the number this document states for
   Dimension 1 are now the same claim — they used to be two different sums
   that happened to disagree. `AIR-4.1`–`AIR-4.4` (RSL, Web Bot Auth,
   `X-Robots-Tag`) — what was left of the old Dimension 1 once its
   quick-scan checks moved out — folded into the old Dimension 2, renamed
   *Crawl, index and licensing hygiene*, so the Index still has 8 dimensions,
   not 9.
4. **Dimensions are ordered by weight, descending; checks within a dimension
   the same way, gates pinned first.** Both orders are computed from the
   registry, never a hand-maintained list — see *Weights*, and every
   `### AIR-x.y` section in this document, for the result.
5. **Nothing is re-scored.** Every scan already on record keeps its `4.0`
   stamp and renders exactly as it did the day it ran; the Census stays on
   4.0 until it is next run. `AI-READINESS-INDEX.md`'s own rule above —
   re-score before comparing across a major bump — still applies to anyone
   who wants to line up a 4.0 result next to a 5.0 one; nothing here does
   that automatically, because nothing here changed what a re-score would
   find. A site scored under 4.0 and the same site scored under 5.0 differ
   only by integer rounding, not by any check's verdict.

#### 4.0 — 2026-09-08

**A major bump, and the versioning rule applies in full.** Any site scored under
3.x must be re-scored under 4.0 before its number is compared to anything.

1. **A gate failure no longer caps the score.** `total` is the site's real, uncapped
   score, computed exactly as in *Scoring*; `gated` and `gate_failures` are reported
   beside it as a separate fact, never blended into it. The old model produced one
   number standing for two facts and comparable to neither — a gated site with
   excellent structure scored identically to a gated site with none. `ungated_score`,
   `ungated_grade`, and the `Gated` grade are gone rather than kept as duplicates of
   what `total` and `gated` already say between them. See *Gates*.
2. **A leading tier exists for checks with essentially no 2026 adoption.** Six checks
   move out of the hundred points entirely — scoring them would subtract the same
   points from every site, which moves nobody relative to anybody. They are still run
   and still reported, as `leading_adopted` of `leading_total` (adopted meaning band 2
   or better), so a site gets credit for being early without it changing anyone's
   score.

#### 3.0 — 2026-09-07

**A major bump, and the versioning rule applies in full.** Any site scored under
2.x must be re-scored under 3.0 before its number is compared to anything.

1. **The crawler obeys the `robots.txt` group addressed to it.** Until now the
   scanner read `robots.txt` only to score it, and crawled regardless of what it
   said about the scanner itself. It now honors a `Disallow` addressed to its own
   product token, and a site that turns it away is recorded as exactly that —
   `robots.txt` is still fetched, so AIR-1.1 still resolves and the gate still
   answers, while every other check reports insufficient evidence. **This changes
   which URLs are sampled, and therefore what a site can score, which is why the
   version is 3.0.**
2. **A blanket `User-agent: *` disallow does not stop the crawler**, and the
   reasoning is now published rather than implied. `Crawl-delay` under `*` is
   honored regardless. See *Consent*.
3. **The AIR-1.2 probe is documented rather than glossed.** The behavior has not
   changed — the probe has always carried other crawlers' product tokens — but
   the specification previously said we "do not pretend to be somebody else's
   bot", which was not an accurate description of the wire. It now states what
   the requests carry and the three constraints that make it measurement rather
   than impersonation. No score moves; the honesty of the document does.
4. **A survey population is a first-class concept**, with the sourcing and
   citation rules a published measurement needs. See *Populations*.
5. **Every result carries the Index's effective date** alongside its version, so
   an old report cannot silently start meaning something new.

#### 2.0 — 2026-09-01

**A major bump, and the versioning rule applies in full.** The one-time exemption
taken at 1.1 is spent. Any site scored under 1.x must be re-scored under 2.0 before
its number is compared to anything.

1. **AIR-1.1's bands are anchored on agent class rather than agent count**, and the
   gate now turns on the answer-serving class. Blocking every training crawler costs 2
   of 5 points and does not gate; blocking one answer-serving agent does. Under 1.x the
   table could not tell `PerplexityBot` from `CCBot` — both scored band 3 — which meant
   a site invisible to an answer engine and a site excluded from a corpus were graded
   identically. **This changes which sites are gated, which is why the version is 2.0.**
2. **`critical` severity widens to band 0 or 1** on checks weighing 3.0 or more. A
   6-point check at band 1 is not a `major` finding sitting alongside a missing table
   caption. Ordering and points are unchanged; only the label moves.
3. **AIR-4.11, AIR-3.1 and AIR-8.7 gain a band 3**, and their unattested ceilings rise from
   2 to 3 to match. Their tables previously skipped 3, so with a ceiling at 2 the whole
   observable range was `{0, 2}` and there was no way to say *mostly right*.

#### 1.2 — 2026-09-01

Refinements found while implementing all 68 checks. None changes a weight or a gate.
Two change how a band is reached and are recorded here so a re-score is explicable.

1. **`@id` coverage in AIR-1.11 counts entity nodes only.** A `ListItem` inside a
   `BreadcrumbList`, a `PostalAddress` on an `Organization` and a `SearchAction`'s
   `EntryPoint` are value objects: they have no identity and nothing should reference
   them. Counting them penalized a site for marking breadcrumbs up correctly.
2. **AIR-1.12 resolution is opt-in.** Band 4 requires `sameAs` links to resolve, which
   means requesting Wikidata, ROR and LinkedIn — hosts the client never allowlisted,
   and hosts that learn which site is being audited. The scanner classifies by
   authority tier from the markup alone and declares an observed ceiling of band 3
   until told to fetch.
3. **AIR-6.6 expects an `autocomplete` token only where the field type implies one**
   (`email`, `tel`, `url`, `password`). A search box has no sensible token and must
   not be marked down for lacking one.
4. **"Widespread" in AIR-4.6 needs a count as well as a share.** One three-hop chain on
   a two-page site is a finding, not a systemic failure.
5. **Every band ceiling now states its reason** in the result and in the report:
   awaiting a baseline run, awaiting confirmation from the client, limited by the band
   attested, or needing review by a person. A client told a number was held down is
   owed the reason.
6. **AIR-4.11's detection method is weaker than this document implied.** The IndexNow key
   file is named after the key, and the key is not published, so a third party can only
   find it where the site advertises it. A negative result is *not discoverable*, which
   is weaker than *absent*, and the check says so.
7. **AIR-5.6 is not implemented.** Reading C2PA manifests means parsing image and PDF
   bytes. The check reports that it had no evidence and leaves the denominator rather
   than scoring a site zero for a measurement nobody took.

#### 1.1 — 2026-09-01

Twelve gaps found while building the first scanner against 1.0. Several of these would ordinarily force a major bump, because they change how a score is computed. They are landing as a minor bump because **no site has ever been scored under 1.0** — the scanner did not exist yet, so there is no trend line to break. This exemption applies once. Every change after this one follows the rule above.

1. **Automated coverage** now counts `auto-partial` at half weight. Under the previous wording the metric could not exceed 0.83, while this document's own example result showed 0.87 — arithmetically unreachable.
2. **Attestations may lift an `auto-partial` band ceiling**, never set or lower a band. Four checks (AIR-4.11, AIR-1.10, AIR-3.1, AIR-8.7) had a top band this document itself says requires attestation, and no mechanism to supply one.
3. **Cross-run checks cap at band 3 on a first run** (AIR-6.9 at 2) and lift with a supplied baseline. AIR-4.8, AIR-2.4 and AIR-6.9 previously required a second audit with no definition of what run one does.
4. **The ten AI agents are sorted into three classes.** AIR-1.1's bands referenced categories the document never defined, and AIR-1.2 asked us to probe two user-agents that no crawler ever sends.
5. **Money-page double weighting is defined** as counting 2 in both sides of the coverage rubric. Previously asserted and never operationalized.
6. **A gated run grades as `Gated`** and gains an `ungated_grade` field. The bands table offered two labels for the same run.
7. **"Requires AIR-X.Y to pass" means band ≥ 2**, with N/A cascading to dependents. Previously undefined against a 0–4 scale.
8. **Business-fact applicability comes from a declared engagement profile**, never inference. Undeclared scores N/A with a reason.
9. **A 25-URL representation sub-sample** bounds AIR-4.4, AIR-7.2, AIR-7.4 and AIR-7.5, which together would otherwise triple the request count against a client's origin.
10. `confidence` is an enum: `high`, `medium`, `low`.
11. AIR-2.1 coverage clamps to 1.0 and excludes empty renders; a missing `robots.txt` scores AIR-1.1 band 4; `score_pct` is `null` where nothing applies; backlog ties break on check ID; `site.cms` is best-effort and nullable.
12. **Rounding happens once**, and the file records that per-check points will not sum exactly to the total.

## Appendix — Test index

| Test | Points |
|---|---|
| RCH-1 | 8 |
| RCH-2 | 12 |
| RCH-3 | 2 |
| RCH-4 | 3 |
| RED-1 | 10 |
| RED-2 | 5 |
| RED-3 | 2 |
| RED-4 | 1 |
| RED-5 | 1 |
| RED-6 | 1 |
| RED-7 | 1 |
| RED-8 | 1 |
| RED-9 | 1 |
| RED-10 | 2 |
| RED-11 | 1 |
| RED-12 | 2 |
| RED-13 | 1 |
| RED-14 | 1 |
| RED-15 | 1 |
| RED-16 | 1 |
| RED-17 | 1 |
| RED-18 | 1 |
| RED-19 | 1 |
| UND-1 | 2 |
| UND-2 | 3 |
| UND-3 | 3 |
| UND-4 | 2 |
| UND-5 | 1 |
| UND-6 | 6 |
| UND-7 | 1 |
| UND-8 | 1 |
| UND-9 | 2 |
| UND-10 | 2 |
| UND-11 | 2 |
| ACT-1 | 5 |
| ACT-2 | 3 |
| ACT-3 | 2 |
| ACT-4 | 5 |

**38 tests · 100 points**

### Unscored tests

These 34 tests are shown in every report and carry no points.

| ID | Group |
|---|---|
| PST-1 | Posture |
| PST-2 | Posture |
| PST-3 | Posture |
| PST-4 | Posture |
| PST-5 | Posture |
| PST-6 | Posture |
| EXT-1 | Extras |
| EXT-2 | Extras |
| EXT-3 | Extras |
| EXT-4 | Extras |
| EXT-5 | Extras |
| EXT-6 | Extras |
| EXT-7 | Extras |
| EXT-8 | Extras |
| EXT-9 | Extras |
| EXT-10 | Extras |
| EXT-11 | Extras |
| EXT-12 | Extras |
| EXT-13 | Extras |
| EXT-14 | Extras |
| EXT-15 | Extras |
| EXT-16 | Extras |
| EXT-17 | Extras |
| EXT-18 | Extras |
| EXT-19 | Extras |
| EXT-20 | Extras |
| MSR-1 | Measurement |
| MSR-2 | Measurement |
| MSR-3 | Measurement |
| MSR-4 | Measurement |
| MSR-5 | Measurement |
| MSR-6 | Measurement |
| MSR-7 | Measurement |
| MSR-8 | Measurement |

**34 unscored tests · 0 points**
