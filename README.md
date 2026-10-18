# The AI Readiness Index: an open standard

A public standard for whether machines can find, read, trust and use a website. It defines 72 tests, the 38 of them worth points and how those points add up to a score out of 100, and the evidence behind each one.

Read it at **[openstandard.readinessindex.io](https://openstandard.readinessindex.io)**.

- **Version 12.0**, effective 2026-11-02.
- Licensed **[CC BY-SA 4.0](LICENSE)** (see also [NOTICE.md](NOTICE.md)): copy it, adapt it, build a scanner from it, for any purpose, as long as you credit TEN7 as the creator of the AI Readiness Index and license what you build the same way.
- Created by [TEN7](https://ten7.com). This repository is the standard, not a product. Scanners that implement it, including TEN7's own product, [readinessindex.io](https://readinessindex.io), are separate software and are not part of it.

## What is here

| File | What it is |
|---|---|
| [`AI-READINESS-INDEX.md`](AI-READINESS-INDEX.md) | The standard. The only place a test's question, explanation, evidence and sources are written. |
| [`tests.yaml`](tests.yaml) | The registry: each test's ID, points, applicability, verification mode and effort. |
| [`crosswalk.yaml`](crosswalk.yaml) | Every Index 11 test ID and what it became. An old ID never stops resolving. |
| [`schema/tests.schema.json`](schema/tests.schema.json) | A JSON Schema for the registry. |
| [`build/`](build) | The script that builds the site from the three files above. |

The site and its machine-readable files (`tests.json`, `evidence.csv`, `crosswalk.json`, `standard.md`, `llms.txt`) are generated, never edited, and published to GitHub Pages on every merge to `main`.

## Take part

- **Propose a test, or say a weight is wrong:** [open an issue](../../issues/new/choose).
- **Ask a question or float an idea:** [Discussions](../../discussions).
- **Send a change:** read [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests are checked automatically.

A change to a weight, a gate or the scoring model is a new major version, and scores from different major versions cannot be compared.

## Build it

```bash
pip install -r requirements.txt
python -m pytest        # registry, document and site checks
python -m build.build   # writes ./site
python -m http.server --directory site
```
