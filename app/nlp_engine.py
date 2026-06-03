import re
from difflib import SequenceMatcher


def normalize_text(text: str) -> str:
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_candidate_phrases(text: str) -> list[str]:
    text = normalize_text(text)
    words = text.split()
    phrases = []

    for n in [2, 3, 4, 5]:
        for i in range(len(words) - n + 1):
            phrases.append(" ".join(words[i : i + n]))

    return phrases


def fuzzy_match_score(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def detect_context_signals(text: str) -> dict:
    text = normalize_text(text)

    return {
        "has_blocking_language": any(
            phrase in text
            for phrase in [
                "cannot start",
                "cannot proceed",
                "unable to move ahead",
                "blocked",
                "stuck",
                "on hold",
            ]
        ),
        "has_dependency_language": any(
            phrase in text
            for phrase in [
                "waiting for",
                "dependent on",
                "requires input",
                "not reverted",
                "pending from",
                "awaiting confirmation",
            ]
        ),
        "has_decision_language": any(
            phrase in text
            for phrase in [
                "approval pending",
                "sign off pending",
                "sign-off pending",
                "sign off",
                "sign-off",
                "decision required",
                "not approved",
                "not confirmed",
            ]
        ),
        "has_schedule_impact": any(
            phrase in text
            for phrase in [
                "uat",
                "go-live",
                "milestone",
                "deadline",
                "timeline",
                "delay",
                "slip",
                "slippage",
                "as planned",
            ]
        ),
        "has_uncertainty": any(
            phrase in text
            for phrase in [
                "may not",
                "may slip",
                "might not",
                "unlikely",
                "risk of",
                "could impact",
                "potentially",
            ]
        ),
    }
