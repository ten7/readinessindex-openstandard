"""tests.yaml must be a faithful, complete encoding of the standard.

The interesting tests parse AI-READINESS-INDEX.md and compare it with the registry. The
document is the source of truth, so the document is the fixture: edit it without
updating the YAML and CI fails, and the reverse.

These are the checks any reader of the standard can verify. What a particular scanner
does with the registry (its gates in code, its quick scan) is that scanner's own test.
"""

from __future__ import annotations

import json
import re

import jsonschema
import pytest

from build import data, spec

ROOT = spec.ROOT
FAMILIES = ("RCH", "RED", "UND", "ACT", "PST", "EXT", "MSR")
PREFIX_OF_DIMENSION = {1: "RCH", 2: "RED", 3: "UND", 4: "ACT"}
APPENDIX_ROW = re.compile(r"^\|\s*([A-Z]{3}-\d+)\s*\|\s*(\d+)\s*\|", re.MULTILINE)


@pytest.fixture(scope="module")
def registry():
    return data.registry()


@pytest.fixture(scope="module")
def spec_text() -> str:
    return spec.source_path().read_text(encoding="utf-8")


def order(test_id: str) -> tuple[int, int]:
    family, number = test_id.split("-")
    return FAMILIES.index(family), int(number)


def test_the_registry_matches_its_schema(registry) -> None:
    schema = json.loads((ROOT / "schema" / "tests.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(registry, schema)


def test_no_duplicate_ids(registry) -> None:
    ids = [c["id"] for c in registry["checks"]]
    assert len(set(ids)) == len(ids)


def test_ids_are_listed_family_by_family_in_number_order(registry) -> None:
    ids = [c["id"] for c in registry["checks"]]
    assert ids == sorted(ids, key=order)


def test_a_scored_test_id_names_its_own_category(registry) -> None:
    wrong = [c["id"] for c in registry["checks"]
             if "dimension" in c and c["id"].split("-")[0] != PREFIX_OF_DIMENSION[c["dimension"]]]
    assert not wrong, wrong


def test_the_scored_tests_are_worth_exactly_one_hundred(registry) -> None:
    scored = [c for c in registry["checks"] if "tier" not in c]
    assert sum(c["weight"] for c in scored) == 100


def test_each_category_weight_is_the_sum_of_its_tests(registry) -> None:
    for dim in registry["dimensions"]:
        got = sum(c["weight"] for c in registry["checks"] if c.get("dimension") == dim["id"])
        assert got == dim["weight"], dim["name"]


def test_no_unscored_test_can_move_a_score(registry) -> None:
    beside = [c for c in registry["checks"] if "tier" in c]
    assert beside and all(c["weight"] == 0 and "dimension" not in c for c in beside)


def test_every_scored_test_is_worth_at_least_a_point(registry) -> None:
    assert all(c["weight"] >= 1 for c in registry["checks"] if "tier" not in c)


def test_exactly_two_gates(registry) -> None:
    assert [c["id"] for c in registry["checks"] if c["gate"]] == ["RCH-1", "RCH-2"]


def test_a_conditional_test_says_when_and_an_unconditional_one_does_not(registry) -> None:
    for c in registry["checks"]:
        has = bool(c.get("precondition") or c.get("requires"))
        assert has == (c["applicability"] == "conditional"), c["id"]
        assert not (c.get("precondition") and c.get("requires")), c["id"]


def test_dependencies_name_real_tests_and_never_loop(registry) -> None:
    ids = {c["id"] for c in registry["checks"]}
    edges = {}
    for c in registry["checks"]:
        req = c.get("requires")
        if req:
            targets = [req["check"]] if req.get("check") else list(req.get("any_of", []))
            assert set(targets) <= ids, c["id"]
            edges[c["id"]] = targets

    def walk(node: str, seen: tuple[str, ...]) -> None:
        assert node not in seen, f"dependency cycle through {node}"
        for nxt in edges.get(node, []):
            walk(nxt, (*seen, node))

    for node in edges:
        walk(node, ())


def test_the_version_and_date_match_the_document(registry, spec_text: str) -> None:
    stated = re.search(r"\*\*Version ([\d.]+) — specification\*\*\s*\nEffective ([\d-]+)\.", spec_text)
    assert stated, "the document's title block is not in the expected shape"
    assert (stated.group(1), stated.group(2)) == (registry["index_version"], registry["index_date"])


def test_weights_match_the_appendix(registry, spec_text: str) -> None:
    appendix = {m.group(1): int(m.group(2)) for m in APPENDIX_ROW.finditer(spec_text)}
    scored = {c["id"]: c["weight"] for c in registry["checks"] if "tier" not in c}
    assert appendix == scored


def test_category_headings_match_the_registry(registry, spec_text: str) -> None:
    rows = re.findall(r"^## #(\d) · ([^·]+?) · (\d+) tests · (\d+) pts", spec_text, re.MULTILINE)
    declared = {int(n): (name.strip(), int(count), int(w)) for n, name, count, w in rows}
    assert len(declared) == len(registry["dimensions"])
    for dim in registry["dimensions"]:
        name, count, weight = declared[dim["id"]]
        assert (dim["name"], dim["weight"]) == (name, weight)
        assert count == sum(1 for c in registry["checks"] if c.get("dimension") == dim["id"])


def test_every_test_has_its_section_with_the_registry_title(registry, spec_text: str) -> None:
    missing = [c["id"] for c in registry["checks"]
               if f"### {c['id']} — {c['title']}" not in spec_text]
    assert not missing, missing


def test_the_document_declares_no_test_the_registry_lacks(registry, spec_text: str) -> None:
    in_doc = set(re.findall(r"^### ((?:RCH|RED|UND|ACT|PST|EXT|MSR)-\d+) — ", spec_text, re.MULTILINE))
    assert in_doc == {c["id"] for c in registry["checks"]}


def test_the_crosswalk_points_only_at_real_tests() -> None:
    ids = {c["id"] for c in data.registry()["checks"]}
    cross = data.crosswalk()
    for old, targets in cross["v11_to_v12"].items():
        assert old.split("-")[0] in {"AIR", "LI", "BP"}, old
        assert set(targets) <= ids, old
    assert set(cross["new_in_v12"]) <= ids
    # A test is either new, or somebody's successor. Never both, never neither.
    successors = {t for targets in cross["v11_to_v12"].values() for t in targets}
    assert successors | set(cross["new_in_v12"]) == ids
    assert not successors & set(cross["new_in_v12"])
