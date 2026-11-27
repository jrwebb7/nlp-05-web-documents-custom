# Customized by jrwebb7 (2026-11).
"""Extend the example transform with an abstract sentence count."""

import logging
import re

from bs4 import BeautifulSoup
import pandas as pd

from nlp.stage03_transform import run_transform as run_example_transform

SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+")


def count_abstract_sentences(abstract: str) -> int:
    """Count text spans split by sentence-ending punctuation and whitespace."""
    text = abstract.strip()
    if not text or text.casefold() == "unknown":
        return 0
    return len(SENTENCE_BREAK.split(text))


def run_transform(soup: BeautifulSoup, logger: logging.Logger) -> pd.DataFrame:
    """Return the extracted metadata with one additional derived field."""
    frame = run_example_transform(soup, logger)
    frame["abstract_sentence_count"] = frame["abstract"].map(count_abstract_sentences)
    logger.info(
        "Abstract sentence count: %s", frame["abstract_sentence_count"].tolist()
    )
    return frame
