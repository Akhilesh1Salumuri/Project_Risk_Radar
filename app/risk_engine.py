from __future__ import annotations

from typing import Iterable

import pandas as pd

try:
    from app.learning_engine import find_learned_phrase_match
    from app.nlp_engine import detect_context_signals
    from app.pmbok_mapper import map_to_pmbok_category
except ModuleNotFoundError:
    from learning_engine import find_learned_phrase_match
    from nlp_engine import detect_context_signals
    from pmbok_mapper import map_to_pmbok_category
try:
    from app.schemas import Finding, SourceUpdate
except ModuleNotFoundError:
    from schemas import Finding, SourceUpdate


TYPE_RULES = [
    (
        "Compliance Risk",
        ["compliance", "risk team", "data sharing", "regulatory", "audit"],
    ),
    ("Data Issue", ["data", "mapping", "migration", "file", "quality", "incorrect", "missing field"]),
    ("Adoption Risk", ["training", "adoption", "business readiness", "users", "change management"]),
    ("Scope Change", ["scope", "change request", "new requirement", "additional requirement"]),
    ("Dependency", ["dependency", "dependent", "waiting", "until", "vendor", "api", "external"]),
    ("Pending Decision", ["decision", "sign off", "sign-off", "confirmation", "approval pending", "pending approval"]),
    ("Blocker", ["blocked", "cannot start", "cannot proceed", "stuck", "preventing", "not approved"]),
    ("Overdue Action", ["overdue", "late", "delayed", "missed", "past due", "not received"]),
    ("Risk", ["risk", "may not", "might not", "at risk", "concern"]),
]

RED_TERMS = ["cannot start", "cannot proceed", "blocked", "not approved", "overdue", "past due"]
AMBER_TERMS = ["delayed", "pending", "may not", "incomplete", "waiting", "risk", "sign off"]
GREEN_TERMS = ["no delivery impact", "on track", "complete", "completed", "resolved", "closed"]
WATCHLIST_TERMS = ["monitor", "watch", "minor", "formatting issue", "issue identified"]


def apply_base_phrase_rules(update_text: str) -> tuple[str, str, str]:
    text = str(update_text).lower()

    update_type = "General Update"
    matched_terms: list[str] = []
    for candidate_type, terms in TYPE_RULES:
        matches = [term for term in terms if term in text]
        if matches:
            update_type = candidate_type
            matched_terms = matches
            break

    if any(term in text for term in RED_TERMS):
        severity = "Red"
    elif any(term in text for term in AMBER_TERMS):
        severity = "Amber"
    elif any(term in text for term in GREEN_TERMS):
        severity = "Green"
    elif any(term in text for term in WATCHLIST_TERMS):
        severity = "Watchlist"
    else:
        severity = "Green" if update_type == "General Update" else "Watchlist"

    if update_type in {"Compliance Risk", "Data Issue", "Scope Change"}:
        severity = "Amber"
    if update_type == "Blocker":
        severity = "Red"

    rationale = "Matched: " + ", ".join(matched_terms[:3]) if matched_terms else "No risk keyword matched"
    return update_type, severity, rationale


def classify_text(update_text: str) -> tuple[str, str, str, str, str]:
    learned_match = find_learned_phrase_match(update_text)

    if learned_match:
        risk_type = str(learned_match["type"])
        severity = str(learned_match["severity"])
        pmbok_category = str(learned_match["pmbok_category"])
        confidence = "High"
        rationale = f"Learned phrase match: {learned_match.get('phrase', '')}"
        return risk_type, severity, pmbok_category, confidence, rationale

    signals = detect_context_signals(update_text)
    base_type, base_severity, base_rationale = apply_base_phrase_rules(update_text)

    risk_type = "General Update"
    severity = "Green"
    confidence = "Medium"
    rationale = "No risk keyword matched"

    if signals["has_blocking_language"]:
        risk_type = "Blocker"
        severity = "Red"
        confidence = "High"
        rationale = "Detected blocking language"
    elif signals["has_uncertainty"] and signals["has_schedule_impact"]:
        risk_type = "Risk"
        severity = "Amber"
        rationale = "Detected uncertainty with schedule impact"
    elif signals["has_decision_language"]:
        risk_type = "Pending Decision"
        severity = "Amber"
        rationale = "Detected decision language"
    elif signals["has_dependency_language"]:
        risk_type = "Dependency"
        severity = "Amber"
        rationale = "Detected dependency language"
    elif "unclear" in str(update_text).lower() or "not agreed" in str(update_text).lower():
        risk_type = "Risk"
        severity = "Amber"
        rationale = "Detected unresolved ownership or agreement risk"

    pmbok_category = map_to_pmbok_category(update_text, risk_type)

    if risk_type == "General Update":
        risk_type = base_type
        severity = base_severity
        rationale = base_rationale
        confidence = "Medium" if base_type != "General Update" else "Low"
    elif base_type in {"Compliance Risk", "Data Issue", "Scope Change"}:
        risk_type = base_type
        severity = base_severity
        rationale = base_rationale
        confidence = "Medium"
    elif risk_type == "Risk" and base_type == "Dependency":
        risk_type = base_type
        severity = "Amber"
        rationale = base_rationale
        confidence = "Medium"

    return risk_type, severity, pmbok_category, confidence, rationale


def build_finding_text(risk_type: str, update_text: str) -> str:
    if risk_type == "General Update":
        return "No active risk finding identified."
    return f"{risk_type} identified from project update."


def build_impact(severity: str, pmbok_category: str) -> str:
    if severity == "Red":
        return f"Immediate attention required due to {pmbok_category.lower()}."
    if severity == "Amber":
        return f"Potential delivery impact related to {pmbok_category.lower()}."
    if severity == "Watchlist":
        return f"Monitor for possible {pmbok_category.lower()}."
    return "No delivery impact identified."


def build_recommended_action(risk_type: str) -> str:
    actions = {
        "Blocker": "Escalate ownership and confirm the next action required to unblock delivery.",
        "Dependency": "Track dependency owner, due date, and required input until closure.",
        "Pending Decision": "Confirm decision owner and target decision date.",
        "Overdue Action": "Escalate overdue action and reset the completion commitment.",
        "Scope Change": "Confirm scope impact, approval path, and delivery trade-offs.",
        "Risk": "Monitor likelihood and impact, then define mitigation if trend worsens.",
    }
    return actions.get(risk_type, "Continue monitoring and update status if the situation changes.")


def _coerce_update(update: SourceUpdate | dict) -> SourceUpdate:
    if isinstance(update, SourceUpdate):
        return update
    return SourceUpdate(**update)


def classify_update(update: SourceUpdate | dict) -> Finding:
    source_update = _coerce_update(update)
    row = source_update.dict()
    text = row.get("update_text", "")
    risk_type, severity, pmbok_category, confidence, _rationale = classify_text(text)
    finding = build_finding_text(risk_type, text)
    impact = build_impact(severity, pmbok_category)
    recommended_action = build_recommended_action(risk_type)
    return Finding(
        update_id=row.get("update_id", ""),
        source_file=row.get("source_file", ""),
        source_type=row.get("source_type", ""),
        source_location=row.get("source_location", ""),
        project=row.get("project", "Unknown Project"),
        workstream=row.get("workstream", "General"),
        type=risk_type,
        severity=severity,
        pmbok_category=pmbok_category,
        finding=finding,
        evidence=text,
        impact=impact,
        owner=row.get("owner", "Owner unclear"),
        recommended_action=recommended_action,
        confidence=confidence,
    )


def normalize_updates_frame(df: pd.DataFrame, source: str) -> list[SourceUpdate]:
    if df.empty:
        return []

    normalized = df.copy()
    normalized.columns = [str(column).strip() for column in normalized.columns]

    if "update_text" not in normalized.columns:
        text_candidates = [column for column in normalized.columns if "update" in column.lower() or "text" in column.lower()]
        if text_candidates:
            normalized = normalized.rename(columns={text_candidates[0]: "update_text"})
        else:
            raise ValueError("CSV must include an update_text column.")

    for column in ["update_id", "source_file", "source_type", "source_location", "project", "workstream", "owner"]:
        if column not in normalized.columns:
            normalized[column] = ""

    updates: list[SourceUpdate] = []
    for _, row in normalized.iterrows():
        update_text = str(row.get("update_text", "")).strip()
        if not update_text:
            continue
        updates.append(
            SourceUpdate(
                update_id=str(row.get("update_id", "") or f"{source}-{len(updates) + 1}"),
                source_file=str(row.get("source_file", "") or source),
                source_type=str(row.get("source_type", "") or source),
                source_location=str(row.get("source_location", "") or ""),
                project=str(row.get("project", "") or "Unknown Project"),
                workstream=str(row.get("workstream", "") or "General"),
                update_text=update_text,
                owner=str(row.get("owner", "") or "Owner unclear"),
            )
        )
    return updates


def classify_updates(updates: Iterable[SourceUpdate | dict]) -> pd.DataFrame:
    records = []
    for update in updates:
        source_update = _coerce_update(update)
        finding = classify_update(source_update).dict()
        finding["update_text"] = source_update.update_text
        records.append(finding)
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)
