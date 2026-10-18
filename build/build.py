"""Builds the site into ./site from the three files at the repository root.

    python -m build.build            # writes ./site
    python -m build.build --out DIR  # somewhere else

Every page, and every machine-readable file beside them, is generated from
`tests.yaml`, `AI-READINESS-INDEX.md` and `crosswalk.yaml`. Nothing is written by hand
twice, so a corrected citation in the document is a corrected row everywhere.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from . import data, spec, specdata

ROOT = spec.ROOT
HERE = Path(__file__).resolve().parent
BASE = "https://openstandard.readinessindex.io"
REPO = "https://github.com/ten7/readinessindex-openstandard"

NAV = [
    {"id": "standard", "href": "/standard/", "label": "Standard"},
    {"id": "tests", "href": "/tests/", "label": "Tests"},
    {"id": "evidence", "href": "/evidence/", "label": "Evidence"},
    {"id": "changelog", "href": "/changelog/", "label": "Changelog"},
    {"id": "contribute", "href": "/contribute/", "label": "Contribute"},
    {"id": "about", "href": "/about/", "label": "About"},
]

#: What each scored category asks. The document says the same in "What this is"; a test
#: fails if it stops.
PROMPTS = {
    "Reach": "Can they get to it?",
    "Read": "Can they find your pages and read the words?",
    "Understand": "Do they know what it is?",
    "Act": "Can an agent do something?",
}

DATA_FILES = [
    ("standard.md", "The standard as Markdown: the same document the pages are made from."),
    ("tests.yaml", "The registry: every test with its points, applicability, verification mode and effort."),
    ("tests.json", "The registry joined to the document: each test's question, evidence, sources and fixers."),
    ("tests.schema.json", "A JSON Schema for tests.yaml."),
    ("evidence.csv", "The evidence register, one row per test."),
    ("evidence.json", "The same register as JSON."),
    ("crosswalk.json", "Every Index 11 test ID and what it became in Index 12."),
    ("crosswalk.yaml", "The crosswalk as it is maintained."),
    ("llms.txt", "A short map of the site for language models."),
    ("sitemap.xml", "Every page."),
]

SECTION_END = re.compile(r"^## ", re.MULTILINE)


def human_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def short_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


# ------------------------------------------------------------------ rendering


def _wrap_tables(html: str) -> str:
    return re.sub(r"(<table>.*?</table>)", r'<div class="table-wrap">\1</div>', html, flags=re.S)


def _anchors(html: str) -> str:
    def add(match: re.Match[str]) -> str:
        level, slug, text = match.group(1), match.group(2), match.group(3)
        return (f'<h{level} id="{slug}"><a class="anchor" href="#{slug}" '
                f'aria-label="Link to this section">#</a>{text}</h{level}>')
    return re.sub(r'<h([2-5]) id="([^"]+)">(.*?)</h\1>', add, html, flags=re.S)


def _drop_title(html: str) -> str:
    return re.sub(r"<h1 id=\"[^\"]+\">.*?</h1>\s*", "", html, count=1, flags=re.S)


def render_doc(markdown: str) -> tuple[Markup, list[spec.Heading]]:
    html, headings = spec.render(markdown)
    return Markup(_anchors(_wrap_tables(_drop_title(html)))), headings


DIMENSION_HEADING = re.compile(r"^#(?P<n>\d+)\s*·\s*(?P<name>.+?)\s*·\s*\d+\s*tests?\s*·\s*(?P<pts>\d+)\s*pts$")
GROUP_HEADING = re.compile(r"^(?P<name>Posture|Extras|Measurement)\s*·\s*\d+\s*items?\s*·\s*not scored$")


def standard_rail(headings: list[spec.Heading]) -> list[tuple[str, str, str, bool]]:
    """The document's own sections, with the categories and groups nested under the tests."""
    items = []
    in_tests = False
    for h in headings:
        if h.level == 1:
            continue
        if h.level == 2:
            in_tests = h.text.strip().lower() == "the tests"
            items.append((h.slug, h.text.replace(" — ", ": "), "", False))
        elif h.level == 3 and in_tests:
            m = DIMENSION_HEADING.match(h.text.strip())
            g = GROUP_HEADING.match(h.text.strip())
            if m:
                items.append((h.slug, f"{m['n']} · {m['name']}", m["pts"], True))
            elif g:
                items.append((h.slug, g["name"], "·", True))
    return items


def changelog_markdown(text: str) -> str:
    start = text.index("## Versioning and change control")
    end = text.index("## Appendix", start)
    return text[start:end].rstrip() + "\n"


def legacy_map() -> dict[str, str]:
    """Index 11 anchors to where they live now, for a link that predates the rewrite."""
    out: dict[str, str] = {}
    for old, targets in data.crosswalk()["v11_to_v12"].items():
        key = old.lower()
        out[key] = f"#{targets[0].lower()}" if targets else f"/evidence/#v11-{key.replace('.', '-')}"
    return out


# ---------------------------------------------------------------------- build


def build(out: Path) -> list[str]:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "assets").mkdir()
    for name in ("site.css", "site.js", "favicon.svg"):
        shutil.copy(HERE / "static" / name, out / "assets" / name)
    asset_v = hashlib.sha256(
        b"".join((HERE / "static" / n).read_bytes() for n in ("site.css", "site.js"))).hexdigest()[:10]

    version, date = data.version()
    tests = data.tests()
    groups = data.by_group()
    scored_groups = [g for g in groups if g["scored"]]
    beside_groups = [g for g in groups if not g["scored"]]
    spec_text = spec.source_path().read_text(encoding="utf-8")

    env = Environment(loader=FileSystemLoader(HERE / "templates"), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    env.globals.update(
        base=BASE, repo=REPO, nav=NAV, version=version, date_human=human_date(date), date_short=short_date(date), asset_v=asset_v,
        n_tests=len(tests), n_scored=len(data.scored()), n_beside=len(tests) - len(data.scored()),
        tones=data.EVIDENCE_TONE, jsonld="")
    pages: list[str] = []

    def page(path: str, template: str, **ctx: Any) -> None:
        html = env.get_template(template).render(path=path, **ctx)
        target = out / path.strip("/") / "index.html" if path != "/" else out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        pages.append(path)

    creator = {"@type": "Organization", "name": "TEN7", "url": "https://ten7.com"}
    # ---- home
    points: dict[str, int] = {}
    for t in data.scored():
        points[t["evidence"]] = points.get(t["evidence"], 0) + t["weight"]
    evidence_points = sorted(points.items(), key=lambda kv: -kv[1])
    home_ld = Markup(json.dumps({
        "@context": "https://schema.org", "@type": "WebSite", "name": "The AI Readiness Index: an open standard",
        "url": BASE + "/", "inLanguage": "en",
        "about": "Whether machines can find, read, trust and use a website"}).replace("<", "\\u003c"))
    page("/", "index.html", page_id="home",
         title="The AI Readiness Index: an open standard",
         description=("A public standard for whether machines can find, read, trust and use a website: "
                      f"{len(tests)} tests, 100 points, every claim cited. Free to read, implement and challenge."),
         scored_groups=scored_groups, beside_groups=beside_groups, prompts=PROMPTS,
         evidence_points=evidence_points, jsonld=home_ld,
         specimen=next(t for t in tests if t["id"] == "RCH-1"))

    # ---- the standard
    standard_md = spec.strip_masthead(spec_text)
    body, headings = render_doc(standard_md)
    std_ld = Markup(json.dumps({
        "@context": "https://schema.org", "@type": "CreativeWork", "name": "The AI Readiness Index",
        "version": version, "dateModified": date, "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "creator": creator, "url": BASE + "/standard/", "inLanguage": "en"}).replace("<", "\\u003c"))
    page("/standard/", "standard.html", page_id="standard",
         title=f"The standard, version {version} · The AI Readiness Index",
         description=("What a website has to do to score 100: the scoring model, every test with its evidence, "
                      "and the changelog. Version " + version + "."),
         body=body, toc=standard_rail(headings), legacy_map=Markup(json.dumps(legacy_map())), jsonld=std_ld)

    # ---- the tests
    rail = [(g["key"], f"{g['number']} · {g['name']}" if g["number"] else g["name"],
             str(g["points"]) if g["scored"] else "·", False) for g in groups]
    rail.append(("rounding", "How points round", "", False))
    page("/tests/", "tests.html", page_id="tests",
         title=f"All {len(tests)} tests · The AI Readiness Index",
         description=f"Every test in the standard, grouped by category, with its evidence and sources. {len(data.scored())} are scored.",
         groups=groups, rail=rail, prompts=PROMPTS, evidence_labels=specdata.EVIDENCE_LABELS,
         legacy_map=Markup(json.dumps(legacy_map())))

    # ---- evidence
    guide_html, _ = spec.render(specdata.evidence_guide())
    guide = Markup(guide_html.replace("<h1 ", "<h3 ").replace("</h1>", "</h3>"))
    cross = data.crosswalk_document()["map"]
    page("/evidence/", "evidence.html", page_id="evidence",
         title="Evidence and sources · The AI Readiness Index",
         description="The evidence label, graded sources and review date behind every test, and the crosswalk from Index 11.",
         guide=guide, tests=tests, crosswalk=cross, new_in_v12=data.crosswalk()["new_in_v12"],
         toc=[("how-to-read", "How to read it", "", False), ("register", "The register", "", False),
              ("crosswalk", "Crosswalk from Index 11", "", False)])

    # ---- changelog
    log_body, log_headings = render_doc(changelog_markdown(spec_text))
    log_toc = [(h.slug, h.text, "", False) for h in log_headings if h.level == 2]
    page("/changelog/", "prose.html", page_id="changelog",
         title="Changelog · The AI Readiness Index", description="What changed in every version of the standard, and why.",
         eyebrow="Changelog", heading="Every version, and why it changed",
         lede=("A change to a weight, a gate or the scoring model is a new major version, and scores from different "
               "major versions cannot be compared."),
         meta=[f"Current: {version}", f"Effective {human_date(date)}"], body=log_body, toc=log_toc)

    # ---- contribute
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    c_body, c_headings = render_doc(contributing)
    page("/contribute/", "prose.html", page_id="contribute",
         title="How to contribute · The AI Readiness Index",
         description="Propose a test, correct a citation or challenge a weight.",
         eyebrow="Contribute", heading="Help change the standard",
         lede="Anyone can propose a change. Here is what makes one easy to accept.",
         meta=[], body=c_body, toc=[(h.slug, h.text, "", False) for h in c_headings if h.level == 2])

    # ---- about, data, 404
    page("/about/", "about.html", page_id="about",
         title="About this standard · The AI Readiness Index",
         description="An open standard created by TEN7 and independent of any scanner: what it is, who made it and how it is run.",
         toc=[("what", "What this is", "", False), ("provenance", "Who made it", "", False),
              ("governance", "How it is run", "", False), ("license", "License", "", False),
              ("privacy", "Privacy", "", False)])
    page("/data/", "data.html", page_id="data", title="Data and files · The AI Readiness Index",
         description="The standard and its registry as plain files at stable addresses.", files=DATA_FILES)
    html404 = env.get_template("404.html").render(
        path="/404.html", page_id="", title="Not found · The AI Readiness Index",
        description="That page is not in the standard.")
    (out / "404.html").write_text(html404, encoding="utf-8")

    # ---- machine-readable files
    (out / "standard.md").write_text(spec_text, encoding="utf-8")
    shutil.copy(ROOT / "tests.yaml", out / "tests.yaml")
    shutil.copy(ROOT / "crosswalk.yaml", out / "crosswalk.yaml")
    shutil.copy(ROOT / "schema" / "tests.schema.json", out / "tests.schema.json")
    (out / "tests.json").write_text(data.dumps(data.tests_document()), encoding="utf-8")
    rows = data.evidence_rows()
    (out / "evidence.json").write_text(data.dumps({"index_version": version, "index_date": date, "tests": rows}),
                                       encoding="utf-8")
    (out / "evidence.csv").write_text(_csv(rows), encoding="utf-8")
    (out / "crosswalk.json").write_text(data.dumps(data.crosswalk_document()), encoding="utf-8")
    (out / "llms.txt").write_text(_llms(version, date, len(tests)), encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    (out / "sitemap.xml").write_text(_sitemap(pages, date), encoding="utf-8")
    (out / "CNAME").write_text("openstandard.readinessindex.io\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    return pages


def _csv(rows: list[dict[str, Any]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["id", "question", "group", "evidence", "evidence_note", "scored", "points", "review_by",
                     "source_count", "v11_ids", "sources"])
    for r in rows:
        sources = " ; ".join(
            f"{s['title']}" + (f" <{s['url']}>" if s["url"] else "") + f" ({s['date']}, grade {s['grade']})"
            for s in r["sources"])
        writer.writerow([r["id"], r["question"], r["group"], r["evidence"], r["evidence_note"],
                         "yes" if r["scored"] else "no", r["points"], r["review_by"], r["source_count"],
                         " ".join(r["v11_ids"]), sources])
    return buffer.getvalue()


def _llms(version: str, date: str, count: int) -> str:
    return f"""# The AI Readiness Index: an open standard

> A public standard for whether machines can find, read, trust and use a website. Version {version}, effective {date}.
> {count} tests, 100 points, every claim cited. Licensed CC BY-SA 4.0. Created by TEN7; independent of any scanner.

## The standard
- [The standard]({BASE}/standard/): the scoring model, every test and the changelog. Markdown: {BASE}/standard.md
- [All tests]({BASE}/tests/): every test as a plain question, with its evidence label and sources
- [Evidence]({BASE}/evidence/): the evidence register and the crosswalk from Index 11
- [Changelog]({BASE}/changelog/): what changed in each version and why

## Machine-readable
- [tests.json]({BASE}/tests.json), [tests.yaml]({BASE}/tests.yaml), [tests.schema.json]({BASE}/tests.schema.json)
- [evidence.csv]({BASE}/evidence.csv), [evidence.json]({BASE}/evidence.json), [crosswalk.json]({BASE}/crosswalk.json)

## About
- [About this standard]({BASE}/about/): who made it, how it is run, license
- [Contribute]({BASE}/contribute/): propose a test or a correction
- Source and issues: {REPO}
"""


def _sitemap(pages: list[str], date: str) -> str:
    urls = "\n".join(f"  <url><loc>{BASE}{p}</loc><lastmod>{date}</lastmod></url>" for p in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "site")
    args = parser.parse_args()
    pages = build(args.out)
    print(f"built {len(pages)} pages into {args.out}")


if __name__ == "__main__":
    main()
