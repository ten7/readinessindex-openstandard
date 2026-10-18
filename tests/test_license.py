"""LICENSE is the license, in full, so that GitHub and every reader recognizes it.

The attribution and trademark note are in NOTICE.md. Keeping them out of LICENSE is what
lets GitHub's detector match the file against the Creative Commons text.
"""

from build import spec


def test_the_license_file_is_the_creative_commons_legal_code() -> None:
    text = (spec.ROOT / "LICENSE").read_text(encoding="utf-8")
    assert text.startswith("Attribution-ShareAlike 4.0 International")
    assert "Section 6 -- Term and Termination." in text
    assert len(text) > 18000


def test_the_notice_says_who_to_credit_and_that_the_name_is_not_licensed() -> None:
    text = " ".join((spec.ROOT / "NOTICE.md").read_text(encoding="utf-8").split())
    assert "credit TEN7 as the creator of the AI Readiness Index" in text
    assert "Nobody may use the name" in text
