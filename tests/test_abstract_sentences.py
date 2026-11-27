"""Check sentence boundaries for arXiv-style abstract text."""

import pytest

from nlp.stage03_transform_custom import count_abstract_sentences


@pytest.mark.parametrize(
    ("abstract", "expected"),
    [
        ("The score was 28.4. The next run took 3.5 days.", 2),
        ("First result!\nSecond result?  Final result.", 3),
        (" \n ", 0),
        ("unknown", 0),
    ],
)
def test_count_abstract_sentences(abstract: str, expected: int) -> None:
    """Keep decimal points inside a sentence and handle absent text."""
    assert count_abstract_sentences(abstract) == expected
