from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .analysis import (
    DEFAULT_DRY_THRESHOLD,
    DEFAULT_HEAVY_THRESHOLD,
    RainfallSummary,
    analyze_rainfall,
)
from .data_loader import load_values, prompt_for_readings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze rainfall measurements and produce farming guidance.",
    )
    parser.add_argument(
        "--data",
        type=float,
        nargs="*",
        help="Rainfall readings (mm) entered directly, e.g. --data 0 5.5 12 32",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Optional path to a CSV or text file containing rainfall readings.",
    )
    parser.add_argument(
        "--dry-threshold",
        type=float,
        default=DEFAULT_DRY_THRESHOLD,
        help=f"Rainfall (mm) at or below which a day is marked dry. Default {DEFAULT_DRY_THRESHOLD}.",
    )
    parser.add_argument(
        "--heavy-threshold",
        type=float,
        default=DEFAULT_HEAVY_THRESHOLD,
        help=f"Rainfall (mm) at or above which a day is marked heavy. Default {DEFAULT_HEAVY_THRESHOLD}.",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.data and not args.file:
        print(
            "No rainfall readings supplied via --data/--file. "
            "Enter values interactively (comma or space separated)."
        )
        args.data = prompt_for_readings()

    return args


def format_report(summary: RainfallSummary) -> str:
    lines = [
        "Rainfall Data Analyzer",
        "-" * 32,
        f"Total rainfall       : {summary.total} mm",
        f"Average per day      : {summary.average} mm",
        f"Minimum / Maximum    : {summary.minimum} mm / {summary.maximum} mm",
        f"Dry days (<= threshold)  : {summary.dry_day_indices or 'None'}",
        f"Heavy days (>= threshold): {summary.heavy_day_indices or 'None'}",
        f"Overall rainfall level   : {summary.rainfall_level}",
        "",
        "Farming guidance:",
    ]
    lines.extend(f"- {insight}" for insight in summary.insights)
    return "\n".join(lines)


def run_cli(argv: Sequence[str] | None = None) -> None:
    try:
        args = parse_args(argv)
        values = load_values(args.data, args.file)
        summary = analyze_rainfall(values, args.dry_threshold, args.heavy_threshold)
        print(format_report(summary))
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)

