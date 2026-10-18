"""What the spec says about each test in plain language, read out of the spec.

`docs/AI-READINESS-INDEX.md` is the only place the plain-language question, the
description and the outside citation for a test are written. They used to live in
`language.py` and `notes.py` as well, which made three copies of the same prose and
two different wordings of it for the quick scan's tests. This module reads
them back out of the Markdown, so `/tests`, the reports and the quick scan show what
the standard says and nothing else.

The reading is by label, never by position. A test's section carries three bullets
this module owns:

    - **Question:** Can AI crawlers reach your site?
    - **Fixed by:** Search specialist, Site owner
    - **Why this matters:** The description. [Source name](https://…): why that source.

`Fixed by` names who typically fixes the test, one to three of the roles the spec defines
in its "Who fixes it" table, the first being who does or drives the work. This module
reads that table too, so a name in a bullet that is not a role there is an error.

It is strict about all of it, because a malformed bullet would otherwise reach a
customer's report as a blank row. Anything missing, repeated or unparseable raises
`SpecDataError` naming the test, and `tests/test_specdata.py` runs the same reading
on the real document so the build fails first.

Nothing here imports a scanner. This file is the strict reader the site is built from,
and it has a twin in the scanner's own repository that reads the same document.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .spec import _source_path

#: A heading that opens a test: `### RCH-1 — Title`, `### EXT-12 — …`, `### MSR-7 — …`.
_TEST_HEADING = re.compile(r"^### ((?:RCH|RED|UND|ACT|PST|EXT|MSR)-\d+) — ")
_ANY_HEADING = re.compile(r"^#{1,3} ")
_BULLET = re.compile(r"^- \*\*(?P<label>[^*:]+):\*\*\s*(?P<text>.*)$")
_OWNED_LABELS = ("Question", "Why this matters", "Fixed by")
#: Read when present, validated when present, never required by the parser: the spec's own
#: test (`tests/test_specdata.py`) is what requires them of every test, so a short fixture
#: in a unit test need not carry them.
_OPTIONAL_LABELS = ("Evidence", "Review by", "Sources", "Replaces")
#: The six evidence labels of "What counts as evidence". A label may be followed by a
#: parenthetical that narrows it, which is part of the claim and is kept.
EVIDENCE_LABELS = ("AI product", "Search index", "Standard only", "None found", "Practice",
                   "Scanner-listed")
_EVIDENCE = re.compile(r"^(?P<label>[A-Za-z -]+?)(?:\s*\((?P<note>[^)]+)\))?$")
_SOURCE_GRADE = re.compile(r"^(?P<head>.+)\s+\((?P<grade>[ABC])\)$")
_SOURCE_LINK = re.compile(r"^\[(?P<title>[^\]]+)\]\((?P<url>https?://[^)\s]+)\)$")
_EMBEDDED_LINK = re.compile(r"\[(?P<title>[^\]]+)\]\((?P<url>https?://[^)\s]+)\)")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
#: The most roles an entry may list: past three the answer stops saying whose desk it is.
MAX_ROLES = 3
_ROLES_HEADING = re.compile(r"^### Who fixes it\s*$")

#: The description, then one link, then a colon and the reason that source is worth
#: citing. Non-greedy on the description so the first link is the citation.
_WHY = re.compile(
    r"^(?P<description>.+?)\s+\[(?P<source>[^\]]+)\]\((?P<url>https://[^)\s]+)\):\s*"
    r"(?P<reason>.+)$")


class SpecDataError(ValueError):
    """A test's section does not say what this module needs it to say."""


@dataclass(frozen=True)
class Role:
    """One of the people the standard says can fix a test, from its "Who fixes it" table."""

    name: str
    who: str
    does: str

    @property
    def slug(self) -> str:
        """`front-end-developer`: what a URL or an HTML id calls the role."""
        return re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")


@dataclass(frozen=True)
class TestContent:
    """One test, in the words the standard uses for somebody who has never read it."""

    __test__ = False  # not a pytest class, whatever its name starts with

    id: str
    question: str
    description: str
    #: Who is being cited, the link to their own documentation, and one sentence on
    #: why that source carries weight (not what the test measures: that is the
    #: description).
    source: str
    url: str
    source_why: str
    #: Who typically fixes it, role names as the spec's table writes them, the one that
    #: does or drives the work first. Resolve them with `role()`.
    fixed_by: tuple[str, ...] = ()
    #: One of `EVIDENCE_LABELS`, and the narrowing parenthetical if the spec gives one.
    #: Empty for a section that carries no Evidence bullet.
    evidence: str = ""
    evidence_note: str = ""
    #: The date the test is next re-read, as the spec writes it (ISO 8601).
    review_by: str = ""
    #: Every citation behind the evidence label, in the order the spec lists them.
    sources: tuple[Source, ...] = ()
    #: The Index 11 ids this test replaces, as the spec writes them. The crosswalk module
    #: holds the same map from the other side; the register page shows this one.
    replaces: tuple[str, ...] = ()


@dataclass(frozen=True)
class Source:
    """One citation from a test's `Sources` bullet."""

    title: str
    #: None for an entry the spec marks "address to confirm": the citation is kept and
    #: shown without a link rather than dropped or given a guessed address.
    url: str | None
    #: As written: an ISO date or month, `undated`, `current`, `draft`, or a short note.
    date: str
    #: A, B or C, from "Source grades".
    grade: str


def _split_entries(text: str) -> list[str]:
    """Split on `; ` outside brackets and parentheses, because a title may contain one."""
    entries, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth = max(0, depth - 1)
        elif ch == ";" and depth == 0:
            entries.append(text[start:i].strip())
            start = i + 1
    entries.append(text[start:].strip())
    return [e for e in entries if e]


def parse_sources(test_id: str, text: str) -> tuple[Source, ...]:
    """`[Title](url), 2026-04-07 (A); Title (address to confirm), undated (B)` as tuples."""
    found = []
    for entry in _split_entries(text):
        graded = _SOURCE_GRADE.match(entry)
        if not graded and not entry.startswith("["):
            # A closing remark in the spec's own words (MSR-4 notes what the register says),
            # not a citation: it has no link, date or grade to show.
            continue
        if not graded:
            raise SpecDataError(f"{test_id}: source {entry!r} must end in a grade (A), (B) or (C)")
        head, grade = graded["head"], graded["grade"]
        if ", " not in head:
            raise SpecDataError(f"{test_id}: source {entry!r} needs a date after the title")
        cited, date = head.rsplit(", ", 1)
        link = _SOURCE_LINK.match(cited)
        if link:
            title, url = link["title"].strip(), link["url"]
        elif _EMBEDDED_LINK.search(cited):
            # "None recorded in the register beyond [X](url) cited under Why this matters":
            # the one source there is, so it is shown as that source and not as the sentence.
            embedded = _EMBEDDED_LINK.search(cited)
            title, url = embedded["title"].strip(), embedded["url"]
        else:
            title, url = re.sub(r"\s*\(address to confirm\)\s*$", "", cited).strip(), None
        found.append(Source(title=title, url=url, date=date.strip(), grade=grade))
    return tuple(found)


def parse_roles(markdown: str) -> tuple[Role, ...]:
    """The roles in the spec's "Who fixes it" table, in the order it lists them."""
    lines = markdown.split("\n")
    start = next((i for i, line in enumerate(lines) if _ROLES_HEADING.match(line)), None)
    if start is None:
        raise SpecDataError("no 'Who fixes it' section")
    roles: list[Role] = []
    for line in lines[start + 1:]:
        if _ANY_HEADING.match(line) or line.startswith("---"):
            break
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("Role",) or set(cells[0]) <= set("-: "):
            continue
        roles.append(Role(name=cells[0], who=cells[1], does=cells[2]))
    names = [r.name for r in roles]
    if len(roles) < 2 or len(set(names)) != len(names) or not all(r.who and r.does for r in roles):
        raise SpecDataError("the 'Who fixes it' table must list distinct roles, each with who "
                            "they are and what they do")
    return tuple(roles)


def parse(markdown: str) -> dict[str, TestContent]:
    """Every test's content, keyed by id, in document order."""
    known = {r.name for r in parse_roles(markdown)}
    found: dict[str, TestContent] = {}
    current: str | None = None
    bullets: dict[str, str] = {}

    def close() -> None:
        if current is not None:
            if current in found:
                raise SpecDataError(f"{current}: the section appears more than once")
            found[current] = _content(current, bullets, known)

    for line in markdown.split("\n"):
        heading = _TEST_HEADING.match(line)
        if heading or _ANY_HEADING.match(line):
            close()
            current, bullets = (heading.group(1) if heading else None), {}
            continue
        if current is None:
            continue
        bullet = _BULLET.match(line)
        if bullet and bullet["label"] in _OWNED_LABELS + _OPTIONAL_LABELS:
            label = bullet["label"]
            if label in bullets:
                raise SpecDataError(f"{current}: more than one '{label}' bullet")
            bullets[label] = bullet["text"].strip()
    close()
    return found


def _content(test_id: str, bullets: dict[str, str], known_roles: set[str]) -> TestContent:
    for label in _OWNED_LABELS:
        if not bullets.get(label):
            raise SpecDataError(f"{test_id}: no '{label}' bullet")
    fixed_by = tuple(name.strip() for name in bullets["Fixed by"].split(","))
    if not 1 <= len(fixed_by) <= MAX_ROLES or len(set(fixed_by)) != len(fixed_by):
        raise SpecDataError(f"{test_id}: 'Fixed by' lists one to {MAX_ROLES} different roles")
    unknown = [name for name in fixed_by if name not in known_roles]
    if unknown:
        raise SpecDataError(f"{test_id}: 'Fixed by' names {unknown}, which the 'Who fixes it' "
                            "table does not define")
    question = bullets["Question"]
    if not question.endswith("?"):
        raise SpecDataError(f"{test_id}: the question does not end in a question mark")
    why = _WHY.match(bullets["Why this matters"])
    if not why:
        raise SpecDataError(
            f"{test_id}: 'Why this matters' must read: description, then "
            "[Source](https://…): why that source is worth citing")
    evidence, note = "", ""
    if "Evidence" in bullets:
        match = _EVIDENCE.match(bullets["Evidence"])
        if not match or match["label"] not in EVIDENCE_LABELS:
            raise SpecDataError(f"{test_id}: 'Evidence' must be one of {list(EVIDENCE_LABELS)}, "
                                "optionally followed by a parenthetical")
        evidence, note = match["label"], (match["note"] or "").strip()
    review_by = bullets.get("Review by", "")
    if "Review by" in bullets and not _DATE.match(review_by):
        raise SpecDataError(f"{test_id}: 'Review by' must be a date like 2027-05-02")
    sources = parse_sources(test_id, bullets["Sources"]) if bullets.get("Sources") else ()
    replaces = tuple(r.strip() for r in bullets["Replaces"].split(",")) \
        if bullets.get("Replaces") else ()
    return TestContent(
        id=test_id, question=question, description=why["description"].strip(),
        source=why["source"].strip(), url=why["url"], source_why=why["reason"].strip(),
        fixed_by=fixed_by, evidence=evidence, evidence_note=note, review_by=review_by,
        sources=sources, replaces=replaces)


@lru_cache(maxsize=2)
def _load(path: str, mtime: float) -> dict[str, TestContent]:
    return parse(Path(path).read_text(encoding="utf-8"))


def content() -> dict[str, TestContent]:
    """Every test's content from the packaged or repository spec."""
    path = _source_path()
    return _load(str(path), path.stat().st_mtime)


def for_test(test_id: str) -> TestContent | None:
    return content().get(test_id)


@lru_cache(maxsize=2)
def _roles(path: str, mtime: float) -> tuple[Role, ...]:
    return parse_roles(Path(path).read_text(encoding="utf-8"))


def roles() -> tuple[Role, ...]:
    """The six roles, from the packaged or repository spec."""
    path = _source_path()
    return _roles(str(path), path.stat().st_mtime)


def role(name: str) -> Role | None:
    return next((r for r in roles() if r.name == name), None)


def fixers_for(test_id: str) -> tuple[Role, ...]:
    """Who typically fixes this test, lead first. Empty for an id the spec does not know,
    which a stored result from a later or earlier Index can carry."""
    entry = for_test(test_id)
    return tuple(r for r in (role(n) for n in entry.fixed_by) if r) if entry else ()


def evidence_for(test_id: str) -> tuple[str, str] | None:
    """The evidence label and its narrowing parenthetical (possibly empty) for a test, or
    None for an id the spec does not know or a section with no Evidence bullet."""
    entry = for_test(test_id)
    return (entry.evidence, entry.evidence_note) if entry and entry.evidence else None


def review_by(test_id: str) -> str | None:
    """The ISO date a test is next re-read, or None when the spec gives none."""
    entry = for_test(test_id)
    return (entry.review_by or None) if entry else None


_GUIDE_HEADING = re.compile(r"^## What counts as evidence\s*$")


def parse_evidence_guide(markdown: str) -> str:
    """The body of "What counts as evidence": the five labels, the three grades and the
    policy, as the spec's own Markdown, from the line after its heading to the rule that
    ends the section. The sentence that points at a repository file is dropped, because on
    a public page it names something the reader cannot open."""
    lines = markdown.split("\n")
    start = next((i for i, line in enumerate(lines) if _GUIDE_HEADING.match(line)), None)
    if start is None:
        raise SpecDataError("no 'What counts as evidence' section")
    body: list[str] = []
    for line in lines[start + 1:]:
        if line.startswith("---") or re.match(r"^#{1,2} ", line):
            break
        body.append(line)
    text = "\n".join(body).strip()
    text = re.sub(r"\s*The register behind them is `[^`]+`\.", "", text)
    if "### Evidence labels" not in text or "### Source grades" not in text:
        raise SpecDataError("'What counts as evidence' must carry 'Evidence labels' and "
                            "'Source grades'")
    return text


def evidence_guide() -> str:
    """The evidence section of the packaged or repository spec, as Markdown."""
    path = _source_path()
    return _guide(str(path), path.stat().st_mtime)


@lru_cache(maxsize=2)
def _guide(path: str, mtime: float) -> str:
    return parse_evidence_guide(Path(path).read_text(encoding="utf-8"))
