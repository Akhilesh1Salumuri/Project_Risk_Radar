from __future__ import annotations

from pathlib import Path
from datetime import datetime

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
MEMORY_PATH = ROOT_DIR / "memory" / "PROJECT_MEMORY.md"
UPDATE_LOG_PATH = ROOT_DIR / "memory" / "UPDATE_LOG.csv"
UPDATE_LOG_COLUMNS = [
    "timestamp",
    "source",
    "source_file",
    "source_type",
    "source_location",
    "project",
    "workstream",
    "update_text",
    "type",
    "severity",
    "pmbok_category",
    "owner",
    "status",
]


def ensure_memory_files_exist() -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not MEMORY_PATH.exists():
        MEMORY_PATH.write_text("project_memory:\n  latest_summary: []\n", encoding="utf-8")
    if not UPDATE_LOG_PATH.exists():
        pd.DataFrame(columns=UPDATE_LOG_COLUMNS).to_csv(UPDATE_LOG_PATH, index=False)
        return

    existing = pd.read_csv(UPDATE_LOG_PATH)
    changed = False
    for column in UPDATE_LOG_COLUMNS:
        if column not in existing.columns:
            existing[column] = ""
            changed = True
    if changed:
        existing[UPDATE_LOG_COLUMNS].to_csv(UPDATE_LOG_PATH, index=False)


def read_project_memory() -> str:
    ensure_memory_files_exist()
    return MEMORY_PATH.read_text(encoding="utf-8")


def save_project_memory(content: str) -> None:
    ensure_memory_files_exist()
    MEMORY_PATH.write_text(content, encoding="utf-8")


def read_update_log() -> pd.DataFrame:
    ensure_memory_files_exist()
    return pd.read_csv(UPDATE_LOG_PATH)


def append_update_log(finding: dict, source: str = "uploaded_file") -> None:
    ensure_memory_files_exist()

    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "source_file": finding.get("source_file", ""),
        "source_type": finding.get("source_type", ""),
        "source_location": finding.get("source_location", ""),
        "project": finding.get("project", ""),
        "workstream": finding.get("workstream", ""),
        "update_text": finding.get("evidence", ""),
        "type": finding.get("type", ""),
        "severity": finding.get("severity", ""),
        "pmbok_category": finding.get("pmbok_category", ""),
        "owner": finding.get("owner", "Owner unclear"),
        "status": finding.get("status", "Open"),
    }

    df = pd.read_csv(UPDATE_LOG_PATH)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(UPDATE_LOG_PATH, index=False)
