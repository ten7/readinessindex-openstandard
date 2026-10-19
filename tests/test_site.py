"""The built site: every address works, every anchor exists, and the files parse.

The pages are generated, so these tests do not check wording. They check the promises the
site makes: a test's address is its ID, an old Index 11 address still lands somewhere, no
internal link is dead, the machine-readable files are the same data as the pages, and the
site is clear that it is a standard and not a company's product.
"""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

import pytest
import yaml

from build import build as site_build
from build import data, spec

PAGES = ["/", "/standard/", "/tests/", "/evidence/", "/changelog/", "/contribute/", "/about/", "/data/"]


@pytest.fixture(scope="module")
def out(tmp_path_factory) -> Path:
    target = tmp_path_factory.mktemp("site")
    site_build.build(target)
    return target


def read(out: Path, path: str) -> str:
    file = out / path.strip("/") / "index.html" if path.endswith("/") else out / path.lstrip("/")
    return file.read_text(encoding="utf-8")


def ids_in(html: str) -> set[str]:
    return set(re.findall(r'\bid="([^"]+)"', html))


def test_every_page_is_built(out: Path) -> None:
    for page in PAGES:
        assert "<h1" in read(out, page), page
    assert (out / "404.html").exists() and (out / ".nojekyll").exists()


def test_a_test_address_is_its_id_on_the_document_and_on_the_tests_page(out: Path) -> None:
    standard, tests = ids_in(read(out, "/standard/")), ids_in(read(out, "/tests/"))
    for t in data.tests():
        anchor = t["id"].lower()
        assert anchor in standard, f"{t['id']} has no section on /standard/"
        assert anchor in tests, f"{t['id']} has no row on /tests/"


def test_no_internal_link_is_dead(out: Path) -> None:
    for page in PAGES + ["/404.html"]:
        html = read(out, page)
        for href in re.findall(r'href="(/[^"]*)"', html):
            path, _, fragment = href.partition("#")
            path = path.split("?")[0]
            if not path:
                continue
            target = out / path.lstrip("/")
            if path.endswith("/"):
                target = target / "index.html"
            assert target.exists(), f"{page} links to {href}, which is not built"
            if fragment and target.suffix == ".html":
                assert fragment in ids_in(target.read_text(encoding="utf-8")), \
                    f"{page} links to {href}, but #{fragment} does not exist"


def test_an_index_11_address_lands_somewhere(out: Path) -> None:
    legacy = json.loads(re.search(r'id="legacy-map">(.*?)</script>', read(out, "/standard/"), re.S).group(1))
    assert legacy["air-1.2"] == "#rch-2"
    assert legacy["air-1.5"] == "/evidence/#v11-air-1-5"
    evidence_ids = ids_in(read(out, "/evidence/"))
    standard_ids = ids_in(read(out, "/standard/"))
    for old, target in legacy.items():
        if target.startswith("#"):
            assert target[1:] in standard_ids, old
        else:
            assert target.split("#")[1] in evidence_ids, old


def test_the_machine_readable_files_parse_and_agree_with_the_registry(out: Path) -> None:
    ids = [c["id"] for c in data.registry()["checks"]]
    tests = json.loads((out / "tests.json").read_text(encoding="utf-8"))
    assert [t["id"] for t in tests["tests"]] == ids
    assert tests["index_version"] == data.version()[0]
    evidence = json.loads((out / "evidence.json").read_text(encoding="utf-8"))
    assert [t["id"] for t in evidence["tests"]] == ids
    rows = list(csv.DictReader(io.StringIO((out / "evidence.csv").read_text(encoding="utf-8"))))
    assert [r["id"] for r in rows] == ids
    assert yaml.safe_load((out / "tests.yaml").read_text(encoding="utf-8")) == data.registry()
    crosswalk = json.loads((out / "crosswalk.json").read_text(encoding="utf-8"))
    assert len(crosswalk["map"]) == len(data.crosswalk()["v11_to_v12"])
    json.loads((out / "tests.schema.json").read_text(encoding="utf-8"))
    assert (out / "standard.md").read_text(encoding="utf-8") == spec.source_path().read_text(encoding="utf-8")


def test_the_category_prompts_are_the_documents_own_words() -> None:
    text = spec.source_path().read_text(encoding="utf-8").lower()
    for name, prompt in site_build.PROMPTS.items():
        assert f"**{name.lower()}:** {prompt.lower()}" in text, name


def test_every_page_has_one_h1_a_canonical_and_no_third_party_resource(out: Path) -> None:
    for page in PAGES:
        html = read(out, page)
        assert len(re.findall(r"<h1[ >]", html)) == 1, page
        assert f'rel="canonical" href="{site_build.BASE}{page}"' in html, page
        assert not re.search(r'<script[^>]+src="https?://', html), page
        assert not re.search(r'<link[^>]+rel="(stylesheet|preload|icon)"[^>]+href="https?://', html), page


def test_the_site_says_it_is_a_standard_and_names_ten7_and_its_product(out: Path) -> None:
    for page in PAGES:
        html = read(out, page)
        assert "Open standard by TEN7" in html, page
        assert 'href="https://ten7.com"' in html and 'href="https://readinessindex.io"' in html, page
        assert "a product of ten7" in html.lower(), page
        assert "commercial business" not in html and "for-profit" not in html, page
    about = read(out, "/about/")
    assert "Neither TEN7 nor its product is the standard" in about
    assert "not a separate company" in about
    assert "CC BY-SA 4.0" in about


def test_no_page_borrows_either_companys_branding(out: Path) -> None:
    css = (out / "assets" / "site.css").read_text(encoding="utf-8").lower()
    for borrowed in ("rubik", "work sans", "source serif", "roboto mono", "--t7-"):
        assert borrowed not in css, borrowed
    for page in PAGES:
        html = read(out, page).lower()
        assert "<img" not in html, f"{page} carries an image, and the site carries no logo"


def test_every_anchor_the_scanner_site_links_to_exists(out: Path) -> None:
    """The product site linked /tests#rounding and /open-standard#grade-bands before the standard
    moved. Both keep working because the anchors exist here."""
    assert "rounding" in ids_in(read(out, "/tests/"))
    assert "grade-bands" in ids_in(read(out, "/standard/"))
    for n in range(1, 5):
        assert f"d{n}" in ids_in(read(out, "/tests/"))


def test_the_old_scanner_site_anchors_are_translated_in_the_script(out: Path) -> None:
    script = (out / "assets" / "site.js").read_text(encoding="utf-8")
    assert "(?:c|row)-" in script and "d-(" in script


def test_the_icon_is_an_orange_square_in_every_format_a_browser_asks_for(out: Path) -> None:
    import struct
    import zlib

    svg = (out / "assets" / "favicon.svg").read_text(encoding="utf-8")
    assert 'fill="#fb9d61"' in svg and 'x="16" y="16" width="32" height="32"' in svg

    def pixels(data: bytes) -> tuple[int, list[bytes]]:
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, _ = struct.unpack(">II", data[16:24])
        idat = b"".join(data[i + 8:i + 8 + n] for i, n in
                        ((j, struct.unpack(">I", data[j:j + 4])[0]) for j in range(8, len(data) - 12)
                         if data[j + 4:j + 8] == b"IDAT"))
        raw = zlib.decompress(idat)
        stride = width * 4 + 1
        return width, [raw[y * stride + 1:(y + 1) * stride] for y in range(width)]

    width, rows = pixels((out / "assets" / "favicon-32.png").read_bytes())
    assert rows[width // 2][(width // 2) * 4:(width // 2) * 4 + 4] == bytes((0xFB, 0x9D, 0x61, 255))
    assert rows[0][0:4] == bytes((0, 0, 0, 0)), "the corner is transparent"
    assert rows[width // 4 - 1][(width // 4 - 1) * 4 + 3] == 0 and rows[width // 4][(width // 4) * 4 + 3] == 255, \
        "the square starts a quarter in: half the icon's width, centered"
    ico = (out / "favicon.ico").read_bytes()
    assert ico[:4] == b"\x00\x00\x01\x00" and struct.unpack("<H", ico[4:6])[0] == 3
    assert (out / "apple-touch-icon.png").read_bytes()[:4] == b"\x89PNG"
    for page in PAGES:
        html = read(out, page)
        assert 'href="/favicon.ico"' in html and 'rel="apple-touch-icon"' in html, page


def test_the_site_is_light_only(out: Path) -> None:
    css = (out / "assets" / "site.css").read_text(encoding="utf-8")
    assert "prefers-color-scheme" not in css
    assert "color-scheme: light;" in css
    for page in PAGES:
        assert '<meta name="color-scheme" content="light">' in read(out, page), page
