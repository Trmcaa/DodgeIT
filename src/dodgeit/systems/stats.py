"""Persistent lifetime statistics stored in stats.json."""

import json
from pathlib import Path


STATS_PATH = Path(__file__).parents[3] / "stats.json"
DEFAULT_STATS = {
    "total_runs": 0,
    "best_score": 0,
    "total_score": 0,
    "total_hits_taken": 0,
    "speed_upgrades": 0,
    "survivability_upgrades": 0,
    "difficulty_runs": {
        "easy": 0,
        "medium": 0,
        "hard": 0,
    },
}


def load():
    """Load lifetime stats, repairing missing fields when needed."""
    try:
        with STATS_PATH.open("r", encoding="utf-8") as file:
            saved_stats = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        saved_stats = {}

    stats = DEFAULT_STATS.copy()
    stats.update(saved_stats)
    stats["difficulty_runs"] = DEFAULT_STATS["difficulty_runs"].copy()
    stats["difficulty_runs"].update(saved_stats.get("difficulty_runs", {}))
    return stats


def save(stats):
    """Write lifetime stats in a readable, stable format."""
    with STATS_PATH.open("w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)


def record_run(stats, difficulty, score, hits_taken, purchased_upgrades):
    """Add one completed run and persist the updated totals."""
    stats["total_runs"] += 1
    stats["best_score"] = max(stats["best_score"], score)
    stats["total_score"] += max(0, score)
    stats["total_hits_taken"] += hits_taken
    stats["difficulty_runs"][difficulty] += 1
    stats["speed_upgrades"] += purchased_upgrades["speed"]
    stats["survivability_upgrades"] += purchased_upgrades["survivability"]
    save(stats)
