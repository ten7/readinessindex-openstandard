"""Renders the standard's Markdown as the site's HTML, with the anchors people cite.

The anchors matter more than they look: a standard nobody can link into is a
standard nobody quotes. Every section and every test gets an address, and a test's
address is its ID and nothing else (`#rch-1`), so it survives the test being
retitled.

This is the same renderer the scanner's own web application uses, kept as a copy so
that either repository works alone. Both are held to the same reading by running the
same strict test over the same document.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token

ROOT = Path(__file__).resolve().parents[1]


def source_path() -> Path:
    """The standard, as the repository root holds it."""
    return ROOT / "AI-READINESS-INDEX.md"


_source_path = source_path


#: A heading that opens with a check ID. Those anchors are the ones people cite.
#: LI- and BP- items are unscored, but they are cited the same way and need the
#: same short anchor.
CHECK_HEADING = re.compile(r"^((?:RCH|RED|UND|ACT|PST|EXT|MSR)-\d+)\b")


def slugify(text: str) -> str:
    """A stable anchor from heading text.

    A check gets its ID and nothing else — `#air-1.1`, not
    `#air-11-no-blanket-robotstxt-blocks-on-ai-crawler-user-agents`. That address is
    short enough to paste into an email, it survives somebody rewording the title,
    and it keeps the dot, so RCH-1 and AIR-11 could never collide. Everything else
    is slugged the ordinary way.
    """
    check = CHECK_HEADING.match(text.strip())
    if check:
        return check.group(1).lower()
    slug = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", slug) or "section"


@dataclass(frozen=True)
class Heading:
    level: int
    text: str
    slug: str


@dataclass(frozen=True)
class Rendered:
    html: str
    headings: list[Heading]


def _markdown_it() -> MarkdownIt:
    # CommonMark plus tables. No raw HTML: the source is ours, but a renderer that
    # cannot emit unescaped HTML is one fewer thing to reason about.
    return MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")


def render(markdown: str) -> tuple[str, list[Heading]]:
    """Markdown to HTML, with an anchor on every heading and a list of them.

    The anchors matter more than they look: a methodology nobody can link into is a
    methodology nobody quotes. Every section and every check gets an address.
    """
    md = _markdown_it()
    tokens = md.parse(markdown)
    headings: list[Heading] = []
    seen: dict[str, int] = {}

    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        inline = tokens[index + 1]
        text = "".join(
            child.content for child in (inline.children or []) if child.type == "text"
        ).strip() or inline.content.strip()

        slug = slugify(text)
        seen[slug] = seen.get(slug, 0) + 1
        if seen[slug] > 1:
            slug = f"{slug}-{seen[slug]}"

        token.attrSet("id", slug)
        headings.append(Heading(level=int(token.tag[1]), text=text, slug=slug))

    _normalise_levels(tokens, headings)
    html = md.renderer.render(_label_tables(tokens), md.options, {})
    return _badge_grade_cells(html), headings


def _label_tables(tokens: list[Token]) -> list[Token]:
    """Give every table a scope on its header cells and a caption. RED-15.

    A Markdown table has no caption to carry, so it takes the heading it sits
    under — which is what the section is called and therefore what the table is
    a table of. The caption is `sr-only` because that heading is already on the
    screen an inch above it: repeating it visibly would be noise, while leaving
    it out entirely means a screen reader announcing "table with 69 rows" and
    nothing about what is in them.

    `scope="col"` is the half that matters most and costs nothing to look at.
    Without it a row is read as seven values; with it, each one is read against
    the column it belongs to.
    """
    labelled: list[Token] = []
    for index, token in enumerate(tokens):
        if token.type == "th_open":
            token.attrSet("scope", "col")
        labelled.append(token)
        if token.type == "table_open":
            heading = _heading_above(tokens, index)
            if heading:
                caption = Token("html_block", "", 0)
                caption.content = (
                    f'<caption class="sr-only">{escape(heading)}</caption>')
                labelled.append(caption)
    return labelled


def _heading_above(tokens: list[Token], index: int) -> str:
    """The text of the nearest heading before `index`, or "" if there is none."""
    for position in range(index - 1, 0, -1):
        if tokens[position - 1].type == "heading_open":
            # The raw inline source, minus the one piece of Markdown that
            # survives into it: a heading like "Attestation against an
            # `auto-partial` check" would otherwise read its backticks aloud.
            return tokens[position].content.replace("`", "").strip()
    return ""


def _normalise_levels(tokens, headings: list[Heading]) -> None:
    """Make the rendered outline descend without skipping, and carry one `<h1>`.

    The document is written for two readers, and the Markdown reflects that
    rather than HTML's rules: it opens two top-level parts with `#`, and its
    changelog entries and asides are `####` sitting directly under a `##`. Read
    as a document that is fine. Rendered as a page it produces two `<h1>`s and
    an h2-to-h4 jump — which fails RED-14 and RED-13, two of the thirty-seven
    tests this site publishes and scores other people against.

    So the levels are recomputed here rather than edited there. The source is a
    versioned standard with a changelog discipline; its heading *depth* is what
    matters and that is preserved exactly — each distinct depth simply maps to
    the next available HTML level. Slugs come from the text and never move, so
    every existing anchor still resolves.
    """
    depths: list[int] = []
    rebuilt: list[Heading] = []
    parts = 0
    for heading in headings:
        while depths and depths[-1] >= heading.level:
            depths.pop()
        depths.append(heading.level)
        if len(depths) == 1:
            parts += 1
        # The document opens two top-level parts. The first is the page's
        # title and keeps h1; the second is a part *of* that page, so it and
        # everything under it shift down one — which is what leaves exactly one
        # h1 without flattening the outline.
        level = len(depths) + (1 if parts > 1 else 0)
        rebuilt.append(replace(heading, level=min(level, 6)))
    headings[:] = rebuilt

    index = 0
    for token in tokens:
        if token.type not in ("heading_open", "heading_close"):
            continue
        level = headings[index].level
        token.tag = f"h{level}"
        if token.type == "heading_close":
            index += 1


#: The Grade bands table's own words, wherever they appear as a bare cell —
#: colored to match the same five tones report/dials.py::GRADE_BANDS already
#: assigns those exact names (b0 = Not ready ... b4 = Exemplary), plus Gated,
#: a separate fact rather than a sixth grade. This recolors cells the document
#: already rendered; it does not add or change a single word of the document
#: itself, so the table stays the one place those names and floors are said.
_GRADE_TONE = {
    "Not ready": "b0", "Weak": "b1", "Adequate": "b2",
    "Strong": "b3", "Exemplary": "b4", "Gated": "gated",
}
_GRADE_CELL = re.compile(
    r"<td>(?:<strong>)?(" + "|".join(re.escape(g) for g in _GRADE_TONE) + r")(?:</strong>)?</td>")


def _badge_grade_cells(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        word = match.group(1)
        return (f'<td><span class="grade-badge grade-badge--{_GRADE_TONE[word]}">'
               f"{word}</span></td>")
    return _GRADE_CELL.sub(replace, html)


def strip_masthead(markdown: str) -> str:
    """The document without the lines between its title and its first section.

    Those lines (version, effective date, repository, the license paragraph) are the
    standalone document's own header and are what the file is checked against: the
    registry's version and date, and the license text, are asserted equal to them. On the
    web page the title is meant to be the first thing, so they are cut from what is
    rendered and never from the file. Left alone when the document has no section yet.
    """
    first_section = markdown.find("\n## ")
    if not markdown.startswith("# ") or first_section < 0:
        return markdown
    title = markdown[:markdown.index("\n")]
    return title + "\n" + markdown[first_section:]
