"""The reader of the document is strict, so a malformed entry fails here by name.

A test's plain-language question, who fixes it, why it matters, its evidence label and
its graded sources are written once, in the document. A bullet that is missing, repeated
or unparseable would otherwise reach a reader as a blank row.
"""

from __future__ import annotations

import pytest

from build import data, spec, specdata


def test_every_test_in_the_registry_has_complete_content() -> None:
    for t in data.registry()["checks"]:
        entry = specdata.for_test(t["id"])
        assert entry is not None, t["id"]
        assert entry.question.endswith("?"), t["id"]
        assert entry.description and entry.source and entry.url.startswith("https://"), t["id"]
        assert entry.fixed_by, t["id"]
        assert entry.evidence in specdata.EVIDENCE_LABELS, t["id"]
        assert entry.review_by, t["id"]
        assert entry.sources, t["id"]


def test_there_are_six_fixer_roles_and_every_one_is_used() -> None:
    roles = [r.name for r in specdata.roles()]
    assert roles == ["Site owner", "Content team", "Search specialist", "Front-end developer",
                     "Back-end developer", "Operations"]
    used = {name for t in data.registry()["checks"] for name in specdata.for_test(t["id"]).fixed_by}
    assert used == set(roles)


def test_a_scored_test_never_rests_on_a_grade_c_source_alone() -> None:
    for t in data.tests():
        if t["scored"]:
            assert any(s["grade"] in ("A", "B") for s in t["sources"]), t["id"]


def test_a_scored_test_has_documented_use() -> None:
    allowed = {"AI product", "Search index", "Practice"}
    bad = [t["id"] for t in data.tests() if t["scored"] and t["evidence"] not in allowed]
    assert not bad, bad


def test_a_malformed_entry_raises_naming_the_test() -> None:
    text = spec.source_path().read_text(encoding="utf-8")
    start = text.index("### RCH-1 — ")
    cut = text.index("- **Why this matters:**", start)
    end = text.index("\n", cut)
    broken = text[:cut] + text[end + 1:]
    with pytest.raises(specdata.SpecDataError, match="RCH-1"):
        specdata.parse(broken)
