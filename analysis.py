from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import List, Sequence, Tuple


DEFAULT_DRY_THRESHOLD = 2.0  # mm/day considered as dry
DEFAULT_HEAVY_THRESHOLD = 20.0  # mm/day considered as heavy rain


@dataclass(frozen=True)
class RainfallSummary:
    total: float
    average: float
    minimum: float
    maximum: float
    dry_day_indices: Tuple[int, ...]
    heavy_day_indices: Tuple[int, ...]
    rainfall_level: str
    insights: Tuple[str, ...]


def analyze_rainfall(
    values: Sequence[float],
    dry_threshold: float,
    heavy_threshold: float,
) -> RainfallSummary:
    total = sum(values)
    avg = mean(values)
    minimum = min(values)
    maximum = max(values)

    dry_days = tuple(idx for idx, value in enumerate(values, start=1) if value <= dry_threshold)
    heavy_days = tuple(idx for idx, value in enumerate(values, start=1) if value >= heavy_threshold)

    rainfall_level = classify_rainfall(avg, heavy_threshold)
    insights = tuple(
        generate_insights(
            dry_days=dry_days,
            heavy_days=heavy_days,
            rainfall_level=rainfall_level,
            dry_threshold=dry_threshold,
            heavy_threshold=heavy_threshold,
            peak_rain=maximum,
        )
    )

    return RainfallSummary(
        total=round(total, 2),
        average=round(avg, 2),
        minimum=round(minimum, 2),
        maximum=round(maximum, 2),
        dry_day_indices=dry_days,
        heavy_day_indices=heavy_days,
        rainfall_level=rainfall_level,
        insights=insights,
    )


def classify_rainfall(average: float, heavy_threshold: float) -> str:
    ratio = average / heavy_threshold if heavy_threshold else 0

    if ratio < 0.25:
        return "Deficit"
    if ratio < 0.8:
        return "Adequate"
    if ratio < 1.2:
        return "High"
    return "Excessive"


def generate_insights(
    dry_days: Sequence[int],
    heavy_days: Sequence[int],
    rainfall_level: str,
    dry_threshold: float,
    heavy_threshold: float,
    peak_rain: float,
) -> List[str]:
    insights: List[str] = []
    longest_dry_spell = _longest_streak(dry_days)

    if dry_days:
        insights.append(
            f"{len(dry_days)} dry day(s) (<= {dry_threshold} mm). Consider supplemental irrigation."
        )
    if longest_dry_spell >= 3:
        insights.append(f"Dry spell lasting {longest_dry_spell} days detected. Delay sowing shallow-root crops.")

    if heavy_days:
        insights.append(
            f"{len(heavy_days)} heavy rainfall day(s) (>= {heavy_threshold} mm). Monitor drainage and bunds."
        )
    if peak_rain >= heavy_threshold * 1.5:
        insights.append("Extreme downpour spotted. Prepare for waterlogging and soil erosion control.")

    if rainfall_level == "Deficit":
        insights.append("Rainfall deficit. Prioritize drought-tolerant crops and schedule irrigation cycles.")
    elif rainfall_level == "Adequate":
        insights.append("Rainfall is adequate. Proceed with sowing and routine irrigation checks.")
    elif rainfall_level in {"High", "Excessive"}:
        insights.append("Rainfall surplus. Focus on drainage, pest/disease scouting, and nitrogen leaching checks.")

    if not insights:
        insights.append("Rainfall is stable. Maintain standard field operations.")

    return insights


def _longest_streak(day_indices: Sequence[int]) -> int:
    if not day_indices:
        return 0

    longest = current = 1
    previous = day_indices[0]
    for day in day_indices[1:]:
        if day == previous + 1:
            current += 1
        else:
            longest = max(longest, current)
            current = 1
        previous = day
    return max(longest, current)

