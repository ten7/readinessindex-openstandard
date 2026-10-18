"""The standard as data: the registry, the spec's words about each test, the crosswalk.

Everything the site and its machine-readable files say comes from three files at the
repository root (`tests.yaml`, `AI-READINESS-INDEX.md`, `crosswalk.yaml`) and nothing
else, so a corrected citation in the document is a corrected row on every page, in the
CSV and in the JSON with nothing to keep in step.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from . import specdata

ROOT = Path(__file__).resolve().parents[1]

#: Display order and labels of the three groups beside the score.
GROUPS = {
    "posture": ("Posture", "Choices that are yours to make. A choice is not a defect, so these are shown and never scored."),
    "extras": ("Extras", "Good practice with no documented reader, and a few early signals. Measured and reported, never scored."),
    "measurement": ("Measurement", "How you track AI traffic. Real work that a scan cannot see, so it is guidance, not points."),
}

#: What each evidence label means, in a phrase, for the chips.
EVIDENCE_TONE = {
    "AI product": "strong",
    "Search index": "strong",
    "Practice": "practice",
    "Standard only": "weak",
    "None found": "none",
    "Scanner-listed": "weak",
}


@lru_cache(maxsize=1)
def registry() -> dict[str, Any]:
    return yaml.safe_load((ROOT / "tests.yaml").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def crosswalk() -> dict[str, Any]:
    return yaml.safe_load((ROOT / "crosswalk.yaml").read_text(encoding="utf-8"))


def version() -> tuple[str, str]:
    r = registry()
    return r["index_version"], r["index_date"]


def v11_ids(new_id: str) -> list[str]:
    return [old for old, targets in crosswalk()["v11_to_v12"].items() if new_id in targets]


def dimension_of(test: dict[str, Any]) -> dict[str, Any] | None:
    for d in registry()["dimensions"]:
        if d["id"] == test.get("dimension"):
            return d
    return None


def tier_of(test: dict[str, Any]) -> str:
    return test.get("tier", "core")


def tests() -> list[dict[str, Any]]:
    """Every test, in registry order, with the spec's words merged in."""
    out = []
    for t in registry()["checks"]:
        entry = specdata.for_test(t["id"])
        if entry is None:
            raise ValueError(f"{t['id']} is in tests.yaml and has no section in the standard")
        dim = dimension_of(t)
        roles = [r.name for r in specdata.fixers_for(t["id"])]
        out.append({
            **t,
            "tier": tier_of(t),
            "group": dim["name"] if dim else GROUPS[tier_of(t)][0],
            "scored": tier_of(t) == "core",
            "question": entry.question,
            "description": entry.description,
            "source": {"name": entry.source, "url": entry.url, "why": entry.source_why},
            "fixed_by": roles,
            "evidence": entry.evidence,
            "evidence_note": entry.evidence_note,
            "review_by": entry.review_by,
            "sources": [{"title": s.title, "url": s.url, "date": s.date, "grade": s.grade}
                        for s in entry.sources],
            "replaces": v11_ids(t["id"]),
        })
    return out


def scored() -> list[dict[str, Any]]:
    return [t for t in tests() if t["scored"]]


def by_group() -> list[dict[str, Any]]:
    """The four scored categories, then the three groups beside them."""
    all_tests = tests()
    groups: list[dict[str, Any]] = []
    for d in registry()["dimensions"]:
        members = [t for t in all_tests if t["scored"] and t["dimension"] == d["id"]]
        groups.append({"key": f"d{d['id']}", "name": d["name"], "number": d["id"],
                       "points": d["weight"], "scored": True, "tests": members})
    for key, (name, why) in GROUPS.items():
        members = [t for t in all_tests if t["tier"] == key]
        groups.append({"key": key, "name": name, "number": None, "points": 0,
                       "scored": False, "why": why, "tests": members})
    return groups


def evidence_rows() -> list[dict[str, Any]]:
    return [{
        "id": t["id"], "question": t["question"], "group": t["group"],
        "evidence": t["evidence"], "evidence_note": t["evidence_note"],
        "scored": t["scored"], "points": t["weight"], "review_by": t["review_by"],
        "source_count": len(t["sources"]), "v11_ids": t["replaces"], "sources": t["sources"],
    } for t in tests()]


def tests_document() -> dict[str, Any]:
    version_, date = version()
    return {"index_version": version_, "index_date": date,
            "license": "CC BY-SA 4.0",
            "categories": registry()["dimensions"],
            "tests": [{
                "id": t["id"], "question": t["question"], "title": t["title"],
                "group": t["group"], "scored": t["scored"], "points": t["weight"],
                "gate": t["gate"], "applicability": t["applicability"],
                "verification": t["verification"], "effort": t["effort"],
                "fixed_by": t["fixed_by"], "evidence": t["evidence"],
                "evidence_note": t["evidence_note"], "review_by": t["review_by"],
                "sources": t["sources"], "replaces": t["replaces"],
            } for t in tests()]}


def crosswalk_document() -> dict[str, Any]:
    version_, date = version()
    ids = {t["id"]: t for t in tests()}
    rows = []
    for old, targets in crosswalk()["v11_to_v12"].items():
        rows.append({"v11": old, "v12": list(targets), "retired": not targets,
                     "targets": [{"id": t, "scored": ids[t]["scored"]} for t in targets]})
    return {"index_version": version_, "index_date": date, "map": rows,
            "new_in_v12": list(crosswalk()["new_in_v12"])}


def dumps(document: Any) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"
