# Customized by jrwebb7 (2026-11).
"""Run the arXiv HTML pipeline with the extended transform stage."""

from argparse import ArgumentParser

from datafun_toolkit.logger import get_logger, log_header

from nlp.config import HTTP_REQUEST_HEADERS
from nlp.config_custom import (
    CUSTOM_NAME,
    CUSTOM_URL,
    EXPERIMENT_NAME,
    EXPERIMENT_URL,
    GENERATED_PATH,
)
from nlp.stage01_extract import run_extract
from nlp.stage02_validate import run_validate
from nlp.stage03_transform_custom import run_transform
from nlp.stage04_load import run_load

LOG = get_logger("abstract-analysis", level="INFO")


def run_pipeline(source_url: str, output_name: str) -> None:
    """Fetch, validate, transform, and save one arXiv abstract page."""
    raw_path = GENERATED_PATH / "raw" / f"{output_name}.html"
    csv_path = GENERATED_PATH / "processed" / f"{output_name}.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    log_header(LOG, f"arXiv abstract analysis for {output_name}")

    html = run_extract(
        source_url=source_url,
        http_request_headers=HTTP_REQUEST_HEADERS,
        raw_html_path=raw_path,
        LOG=LOG,
    )
    soup = run_validate(html_content=html, LOG=LOG)
    frame = run_transform(soup, LOG)
    run_load(df=frame, processed_csv_path=csv_path, LOG=LOG)
    LOG.info("Pipeline executed successfully. CSV: %s", csv_path)


def main() -> None:
    """Process the selected paper or repeat the original-paper experiment."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--experiment",
        action="store_true",
        help="Add a sentence count to the original Agents of Chaos example.",
    )
    if parser.parse_args().experiment:
        run_pipeline(EXPERIMENT_URL, EXPERIMENT_NAME)
    else:
        run_pipeline(CUSTOM_URL, CUSTOM_NAME)


if __name__ == "__main__":
    main()
