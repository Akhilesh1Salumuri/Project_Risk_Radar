from datetime import datetime
from pathlib import Path

import pandas as pd

try:
    from app.nlp_engine import fuzzy_match_score, normalize_text
except ModuleNotFoundError:
    from nlp_engine import fuzzy_match_score, normalize_text


PHRASE_MEMORY_PATH = Path("memory/PHRASE_MEMORY.csv")
FEEDBACK_PATH = Path("memory/CLASSIFICATION_FEEDBACK.csv")
LEARNED_TAXONOMY_PATH = Path("memory/LEARNED_TAXONOMY.md")


def yaml_string(value: object) -> str:
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def ensure_learning_files_exist():
    Path("memory").mkdir(exist_ok=True)

    if not PHRASE_MEMORY_PATH.exists():
        pd.DataFrame(
            columns=[
                "phrase",
                "normalized_phrase",
                "type",
                "severity",
                "pmbok_category",
                "confidence",
                "learned_from",
                "created_at",
                "last_used_at",
                "usage_count",
            ]
        ).to_csv(PHRASE_MEMORY_PATH, index=False)

    if not FEEDBACK_PATH.exists():
        pd.DataFrame(
            columns=[
                "timestamp",
                "update_text",
                "old_type",
                "old_severity",
                "old_pmbok_category",
                "new_type",
                "new_severity",
                "new_pmbok_category",
                "user_phrase",
                "notes",
            ]
        ).to_csv(FEEDBACK_PATH, index=False)

    if not LEARNED_TAXONOMY_PATH.exists():
        LEARNED_TAXONOMY_PATH.write_text("# Learned Taxonomy\n", encoding="utf-8")


def load_phrase_memory() -> pd.DataFrame:
    ensure_learning_files_exist()
    return pd.read_csv(PHRASE_MEMORY_PATH)


def find_learned_phrase_match(text: str, threshold: float = 0.82) -> dict | None:
    ensure_learning_files_exist()
    text_norm = normalize_text(text)
    memory = load_phrase_memory()

    best_match = None
    best_score = 0

    for _, row in memory.iterrows():
        phrase = str(row["normalized_phrase"])
        score = fuzzy_match_score(text_norm, phrase)

        if phrase in text_norm:
            score = 1.0

        if score > best_score:
            best_score = score
            best_match = row.to_dict()

    if best_match and best_score >= threshold:
        best_match["match_score"] = best_score
        return best_match

    return None


def save_user_feedback(
    update_text: str,
    old_type: str,
    old_severity: str,
    old_pmbok_category: str,
    new_type: str,
    new_severity: str,
    new_pmbok_category: str,
    user_phrase: str,
    notes: str = "",
):
    ensure_learning_files_exist()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    feedback = pd.read_csv(FEEDBACK_PATH)
    feedback = pd.concat(
        [
            feedback,
            pd.DataFrame(
                [
                    {
                        "timestamp": now,
                        "update_text": update_text,
                        "old_type": old_type,
                        "old_severity": old_severity,
                        "old_pmbok_category": old_pmbok_category,
                        "new_type": new_type,
                        "new_severity": new_severity,
                        "new_pmbok_category": new_pmbok_category,
                        "user_phrase": user_phrase,
                        "notes": notes,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )
    feedback.to_csv(FEEDBACK_PATH, index=False)

    add_or_update_phrase_memory(
        phrase=user_phrase,
        risk_type=new_type,
        severity=new_severity,
        pmbok_category=new_pmbok_category,
    )


def add_or_update_phrase_memory(
    phrase: str,
    risk_type: str,
    severity: str,
    pmbok_category: str,
):
    ensure_learning_files_exist()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    phrase_norm = normalize_text(phrase)

    memory = pd.read_csv(PHRASE_MEMORY_PATH)

    existing = memory["normalized_phrase"] == phrase_norm

    if existing.any():
        memory.loc[existing, "type"] = risk_type
        memory.loc[existing, "severity"] = severity
        memory.loc[existing, "pmbok_category"] = pmbok_category
        memory.loc[existing, "last_used_at"] = now
        memory.loc[existing, "usage_count"] = memory.loc[existing, "usage_count"].fillna(0).astype(int) + 1
    else:
        memory = pd.concat(
            [
                memory,
                pd.DataFrame(
                    [
                        {
                            "phrase": phrase,
                            "normalized_phrase": phrase_norm,
                            "type": risk_type,
                            "severity": severity,
                            "pmbok_category": pmbok_category,
                            "confidence": "High",
                            "learned_from": "user_feedback",
                            "created_at": now,
                            "last_used_at": now,
                            "usage_count": 1,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    memory.to_csv(PHRASE_MEMORY_PATH, index=False)
    update_learned_taxonomy_md()


def update_learned_taxonomy_md():
    memory = pd.read_csv(PHRASE_MEMORY_PATH)

    lines = [
        "learned_taxonomy:",
        "  description: User-specific phrases learned from feedback.",
        "  learned_phrases:",
    ]

    if memory.empty:
        lines.append("    []")
    else:
        for _, row in memory.sort_values(by=["type", "phrase"]).iterrows():
            lines.append(f"    - type: {yaml_string(row['type'])}")
            lines.append(f"      phrase: {yaml_string(row['phrase'])}")
            lines.append(f"      pmbok_category: {yaml_string(row['pmbok_category'])}")
            lines.append(f"      severity: {yaml_string(row['severity'])}")
            lines.append(f"      usage_count: {row['usage_count']}")

    LEARNED_TAXONOMY_PATH.write_text("\n".join(lines), encoding="utf-8")
