from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


def prompt_for_readings() -> List[float]:
    raw = input("Rainfall readings (mm): ").strip()
    if not raw:
        raise ValueError("No rainfall data entered.")
    tokens = raw.replace(",", " ").split()
    return _to_float_list(tokens)


def load_values(
    inline_values: Optional[Sequence[float]],
    file_path: Optional[Path],
) -> List[float]:
    values: List[float] = []

    if inline_values:
        values.extend(inline_values)

    if file_path:
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        suffix = file_path.suffix.lower()
        if suffix in {".csv", ".tsv"}:
            delimiter = "," if suffix == ".csv" else "\t"
            with file_path.open("r", encoding="utf-8") as fh:
                reader = csv.reader(fh, delimiter=delimiter)
                for row in reader:
                    values.extend(_to_float_list(row))
        else:
            with file_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    values.extend(_to_float_list(line.replace(",", " ").split()))

    values = [v for v in values if v is not None]

    if not values:
        raise ValueError("No rainfall data found in the provided sources.")

    return values


def _to_float_list(tokens: Iterable[str]) -> List[float]:
    parsed: List[float] = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        try:
            parsed.append(float(token))
        except ValueError as exc:  # pragma: no cover
            raise ValueError(f"Unable to parse rainfall value '{token}'.") from exc
    return parsed

