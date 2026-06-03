def map_to_pmbok_category(text: str, risk_type: str) -> str:
    text = str(text).lower()

    if risk_type == "Risk" and any(x in text for x in ["uat", "go-live", "deadline", "timeline", "delay", "slip", "slippage", "schedule"]):
        return "Schedule Risk"

    if any(x in text for x in ["legal", "compliance", "security", "audit", "privacy", "risk team"]):
        return "Compliance / Security Risk"

    if any(x in text for x in ["data", "mapping", "migration", "duplicate", "master data"]):
        return "Data Risk"

    if any(x in text for x in ["training", "sop", "handover", "adoption", "users not ready"]):
        return "Adoption / Change Risk"

    if any(x in text for x in ["scope", "requirement", "change request", "additional market"]):
        return "Scope Risk"

    if any(x in text for x in ["sender id", "approval", "sign off", "sign-off", "stakeholder", "owner unclear", "finance has not reverted"]):
        return "Stakeholder Risk"

    if any(x in text for x in ["api", "integration", "environment", "deployment", "access", "configuration"]):
        return "Technical / Integration Risk"

    if any(x in text for x in ["uat", "go-live", "deadline", "timeline", "delay", "slip", "slippage", "schedule"]):
        return "Schedule Risk"

    if any(x in text for x in ["budget", "cost", "invoice", "commercial", "pricing"]):
        return "Cost Risk"

    if any(x in text for x in ["defect", "testing", "test case", "test cases", "quality", "validation", "rework"]):
        return "Quality Risk"

    if any(x in text for x in ["sme", "resource", "capacity", "availability"]):
        return "Resource Risk"

    if any(x in text for x in ["vendor", "bank", "third party", "supplier"]):
        return "Procurement / Vendor Risk"

    return "Communication Risk"
