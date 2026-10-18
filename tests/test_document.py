"""The standard's pages are the document, rendered. Not a rewrite of it.

Sentences that carry the argument have to survive the trip, or the published standard is
marketing about the standard. These tests read the rendered HTML, never the Markdown.
"""

from __future__ import annotations

import pytest

from build import build as site_build
from build import data, spec


@pytest.fixture(scope="module")
def rendered():
    html, headings = spec.render(spec.strip_masthead(spec.source_path().read_text(encoding="utf-8")))
    return html, headings


def test_the_sentences_that_carry_the_argument_survive(rendered) -> None:
    html, _ = rendered
    for sentence in ("A beautiful site can score 12", "can machines find, read, trust, and use this website"):
        assert sentence.lower() in html.lower(), sentence


def test_the_versioning_and_the_changelog_survive(rendered) -> None:
    html, _ = rendered
    assert "Versioning and change control" in html
    assert data.version()[0] in html


def test_every_test_has_a_section_and_every_heading_an_address(rendered) -> None:
    html, headings = rendered
    slugs = [h.slug for h in headings]
    assert len(slugs) == len(set(slugs)), "an anchor that points at two places"
    for test in data.registry()["checks"]:
        assert f'id="{test["id"].lower()}"' in html, test["id"]


def test_the_document_has_exactly_one_h1_after_rendering(rendered) -> None:
    html, _ = rendered
    assert html.count("<h1 ") == 1


def test_the_grade_bands_table_is_recolored_not_reworded(rendered) -> None:
    html, _ = rendered
    for word, tone in [("Exemplary", "b4"), ("Strong", "b3"), ("Adequate", "b2"),
                       ("Weak", "b1"), ("Not ready", "b0"), ("Gated", "gated")]:
        assert f'<span class="grade-badge grade-badge--{tone}">{word}</span>' in html


def test_a_grade_word_is_badged_only_in_the_grade_bands_table(rendered) -> None:
    html, _ = rendered
    for word in ("Exemplary", "Strong", "Adequate", "Weak", "Not ready"):
        assert html.count(f">{word}</span>") == 1, word


def test_the_badge_is_a_narrow_substitution() -> None:
    html = "<table><tr><td>Weak</td><td>Some prose that says Weak too.</td></tr></table>"
    assert spec._badge_grade_cells(html) == (
        '<table><tr><td><span class="grade-badge grade-badge--b1">Weak</span></td>'
        "<td>Some prose that says Weak too.</td></tr></table>")


def test_no_internal_reference_reaches_the_public_document() -> None:
    text = spec.source_path().read_text(encoding="utf-8")
    for internal in ("TEN7RD", "atlassian", "ten7_air", "readinessindex-web", "docs/EVIDENCE-REGISTER"):
        assert internal not in text.replace("changelog", ""), internal


def test_the_changelog_slice_is_the_section_the_document_names() -> None:
    text = spec.source_path().read_text(encoding="utf-8")
    slice_ = site_build.changelog_markdown(text)
    assert slice_.startswith("## Versioning and change control")
    assert "## Appendix" not in slice_
