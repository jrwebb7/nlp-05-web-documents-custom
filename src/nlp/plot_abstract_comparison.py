# Customized by jrwebb7 (2026-11).
"""Build the report CSV and chart from both pipeline runs."""

from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import pandas as pd

from nlp.config import ROOT_PATH
from nlp.config_custom import CUSTOM_NAME, EXPERIMENT_NAME, GENERATED_PATH

COMPARISON_COLUMNS = [
    "arxiv_id",
    "title",
    "subjects",
    "author_count",
    "abstract_word_count",
    "abstract_sentence_count",
]


def main() -> None:
    """Publish the comparison metrics and a labeled sentence-count figure."""
    processed = GENERATED_PATH / "processed"
    reports = [
        pd.read_csv(
            processed / f"{name}.csv",
            usecols=COMPARISON_COLUMNS,
            dtype={"arxiv_id": "string"},
        )
        for name in (EXPERIMENT_NAME, CUSTOM_NAME)
    ]
    summary = pd.concat(reports, ignore_index=True)

    docs = ROOT_PATH / "docs"
    csv_path = docs / "data" / "abstract-comparison.csv"
    chart_path = docs / "images" / "abstract-sentence-counts.png"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    chart_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(
        csv_path, columns=COMPARISON_COLUMNS, index=False, lineterminator="\n"
    )

    counts = summary["abstract_sentence_count"]
    figure = Figure(figsize=(7.6, 3.2), layout="constrained", facecolor="white")
    axis = figure.subplots()
    bars = axis.barh(
        summary["title"], counts, height=0.48, color=["#59728b", "#19776b"]
    )
    axis.invert_yaxis()
    axis.set_title(
        "Abstract sentence counts on arXiv", loc="left", weight="bold", pad=14
    )
    axis.set_xlabel("Sentences per abstract")
    axis.set_xlim(0, int(counts.max()) + 2)
    axis.xaxis.set_major_locator(MaxNLocator(integer=True))
    axis.set_axisbelow(True)
    axis.grid(axis="x", color="#d6e0e5", linewidth=0.7)
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0, pad=8, labelsize=11)
    axis.bar_label(bars, padding=6, weight="bold")
    figure.savefig(chart_path, dpi=140, pil_kwargs={"optimize": True})


if __name__ == "__main__":
    main()
