# Contributing

## Ways to take part

Open an issue to **propose a test**, to **correct a citation or a sentence**, or to say a weight is wrong. Use Discussions for a question or an idea that is not yet a proposal. Send a pull request when you already know the change you want.

You do not need to ask first. A proposal that comes with its evidence is the easiest kind to accept.

## What the standard is made of

Three files, and nothing else carries the standard.

- `AI-READINESS-INDEX.md` is the standard. It is the only place the plain-language **Question**, **Why this matters**, **Fixed by**, **Evidence**, **Sources** and **Review by** for a test are written. Every page on the site reads them back out of this file.
- `tests.yaml` is the registry: each test's ID, points, applicability, verification mode and effort. It must agree with the document, and a check fails when it does not.
- `crosswalk.yaml` maps every Index 11 test ID to what it became. An old ID never stops resolving.

Change a test by changing its section in the document and, if a number changed, its row in the registry. Both go in one pull request.

## Proposing a test

A test is worth proposing when it answers a question a machine has to get right before it can use a site. A good proposal says:

1. **What a machine needs.** In plain words, the question the test asks.
2. **The signal.** What can be observed from outside that answers it.
3. **The evidence.** A source that is not you, ideally the documentation of a search engine, an AI company or a standards body, that says something uses this. Say honestly when you found none.
4. **Who would fix it.** One to three of the six roles in the standard's table.

An accepted test is added unscored. It is scored only when it has documented use, and moving a test into or out of the score is a change to the score.

## What counts as evidence

Every test carries one evidence label and every source a grade. The labels and grades are defined in the standard under *What counts as evidence*. In short, a test is scored only when an AI product or a search index is documented using it, or when it is sound practice and is labeled so. A scored test must not rest on a grade C source alone.

## Rules a change has to follow

- **A change to a weight, a gate or the scoring model is a major version.** It needs a changelog entry that says plainly that old and new scores cannot be compared. The check fails a weight change with no version change.
- **Every score is a whole number.** No test is worth half a point.
- **Reword freely, renumber never.** A pull request may propose that a test change its ID, in prose. The maintainers make that change themselves, together with anyone who implements the test, in one pass, so that no implementation is left pointing at an ID that now means something else.
- **Cite, do not assert.** A claim about what machines do needs a source. "Everyone knows" is not one.
- **American English, plain words.** Write for somebody who has never read the standard. Leave the technical terms to the **Detect** section.

## Checking your change

```bash
pip install -r requirements.txt
python -m pytest
python -m build.build   # writes ./site
```

The tests validate the registry against its schema, check that the registry and the document agree, and read every test's entry as strictly as the site does, so a missing or malformed bullet fails by test ID. Open `site/index.html` in a browser to see the result.

## How a change is decided

Maintainers review in the open. Changes that fix a typo or a citation are merged when the checks pass. A change that adds a test, or touches points, is discussed in the pull request or the issue first, and is released in a tagged version. Releases are tagged by version, for example `v12.0`, and scanners that implement the standard pin to a tag.

## License

By contributing you agree that your contribution is published under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), like the rest of the standard.
