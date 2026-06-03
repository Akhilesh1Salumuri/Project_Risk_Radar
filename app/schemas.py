from pydantic import BaseModel
from typing import Optional, Literal


RiskType = Literal[
    "Risk",
    "Blocker",
    "Dependency",
    "Pending Decision",
    "Overdue Action",
    "Scope Change",
    "Data Issue",
    "Compliance Risk",
    "Adoption Risk",
    "General Update",
]

Severity = Literal["Red", "Amber", "Green", "Watchlist"]
Confidence = Literal["High", "Medium", "Low"]


class SourceUpdate(BaseModel):
    update_id: str
    source_file: str = ""
    source_type: str = ""
    source_location: str = ""
    project: str = "Unknown Project"
    workstream: str = "General"
    update_text: str
    owner: str = "Owner unclear"


class Finding(BaseModel):
    update_id: str
    source_file: str = ""
    source_type: str = ""
    source_location: str = ""
    project: str
    workstream: str
    type: RiskType
    severity: Severity
    pmbok_category: str = "Communication Risk"
    finding: str
    evidence: str
    impact: str
    owner: Optional[str] = "Owner unclear"
    recommended_action: str
    confidence: Confidence


LOG_COLUMNS = [
    "update_id",
    "source_file",
    "source_type",
    "source_location",
    "project",
    "workstream",
    "update_text",
    "type",
    "severity",
    "pmbok_category",
    "finding",
    "evidence",
    "impact",
    "owner",
    "recommended_action",
    "confidence",
]
