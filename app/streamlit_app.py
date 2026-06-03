from __future__ import annotations

import pandas as pd
import streamlit as st

try:
    from app.file_ingestor import SUPPORTED_EXTENSIONS, parse_uploaded_file
    from app.learning_engine import save_user_feedback
    from app.memory_manager import append_update_log, read_project_memory, save_project_memory
    from app.risk_engine import classify_update
except ModuleNotFoundError:
    from file_ingestor import SUPPORTED_EXTENSIONS, parse_uploaded_file
    from learning_engine import save_user_feedback
    from memory_manager import append_update_log, read_project_memory, save_project_memory
    from risk_engine import classify_update


SOURCE_COLUMNS = [
    "update_id",
    "source_file",
    "source_type",
    "source_location",
    "project",
    "workstream",
    "update_text",
    "owner",
]
EXPORT_COLUMNS = [
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
    "confidence",
    "owner",
    "recommended_action",
]
TYPE_OPTIONS = [
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
SEVERITY_OPTIONS = ["Red", "Amber", "Green", "Watchlist"]
PMBOK_CATEGORY_OPTIONS = [
    "Schedule Risk",
    "Scope Risk",
    "Cost Risk",
    "Quality Risk",
    "Resource Risk",
    "Stakeholder Risk",
    "Procurement / Vendor Risk",
    "Technical / Integration Risk",
    "Data Risk",
    "Compliance / Security Risk",
    "Adoption / Change Risk",
    "Communication Risk",
]


st.set_page_config(page_title="Project Risk Monitor", layout="wide")


def show_metrics(register: pd.DataFrame) -> None:
    total = len(register)
    red = int((register["severity"] == "Red").sum()) if not register.empty else 0
    amber = int((register["severity"] == "Amber").sum()) if not register.empty else 0
    watchlist = int((register["severity"] == "Watchlist").sum()) if not register.empty else 0
    blockers = int((register["type"] == "Blocker").sum()) if not register.empty else 0

    cols = st.columns(5)
    cols[0].metric("Updates", total)
    cols[1].metric("Red", red)
    cols[2].metric("Amber", amber)
    cols[3].metric("Watchlist", watchlist)
    cols[4].metric("Blockers", blockers)


def render_register(register: pd.DataFrame) -> None:
    st.subheader("Risk Register")
    if register.empty:
        st.info("No classified updates yet.")
        return

    display_frame = register.copy()
    for column in EXPORT_COLUMNS:
        if column not in display_frame.columns:
            display_frame[column] = ""

    ordered = register.sort_values(
        by="severity",
        key=lambda column: column.map({"Red": 0, "Amber": 1, "Watchlist": 2, "Green": 3}).fillna(4),
    )
    st.dataframe(
        display_frame.loc[ordered.index, EXPORT_COLUMNS],
        use_container_width=True,
        hide_index=True,
    )


def option_index(options: list[str], value: object, default: str) -> int:
    normalized_value = "" if pd.isna(value) else str(value)
    if normalized_value in options:
        return options.index(normalized_value)
    return options.index(default)


def render_teach_app(register: pd.DataFrame) -> None:
    st.subheader("Teach the app")
    if register.empty:
        st.info("Classify at least one update before saving corrections.")
        return

    findings = register.reset_index(drop=True).copy()
    for column in ["update_text", "type", "severity", "pmbok_category"]:
        if column not in findings.columns:
            findings[column] = ""

    def format_finding(index: int) -> str:
        row = findings.loc[index]
        text = str(row.get("update_text", ""))
        label = text[:90] + "..." if len(text) > 90 else text
        return f"{index + 1}. {label}"

    selected_index = st.selectbox(
        "Select a finding the app classified",
        options=list(findings.index),
        format_func=format_finding,
    )
    selected = findings.loc[selected_index]
    old_type = str(selected.get("type", "") or "General Update")
    old_severity = str(selected.get("severity", "") or "Green")
    old_pmbok_category = str(selected.get("pmbok_category", "") or "Communication Risk")
    update_text = str(selected.get("update_text", "") or "")

    with st.form("teach_app_form", clear_on_submit=True):
        st.text_area("Update text", value=update_text, disabled=True)
        st.caption(f"App classified as: {old_type} / {old_severity} / {old_pmbok_category}")

        cols = st.columns(3)
        new_type = cols[0].selectbox(
            "Correct type",
            TYPE_OPTIONS,
            index=option_index(TYPE_OPTIONS, old_type, "General Update"),
        )
        new_severity = cols[1].selectbox(
            "Correct severity",
            SEVERITY_OPTIONS,
            index=option_index(SEVERITY_OPTIONS, old_severity, "Green"),
        )
        new_pmbok_category = cols[2].selectbox(
            "Correct PMBOK category",
            PMBOK_CATEGORY_OPTIONS,
            index=option_index(PMBOK_CATEGORY_OPTIONS, old_pmbok_category, "Communication Risk"),
        )
        phrase_text = st.text_area("Phrase to learn", placeholder="unable to move ahead\nFinance reverts")
        notes = st.text_input("Notes")
        submitted = st.form_submit_button("Save correction")

    if not submitted:
        return

    phrases = [phrase.strip() for phrase in phrase_text.splitlines() if phrase.strip()]
    if not phrases:
        st.warning("Enter at least one phrase for the app to learn.")
        return

    for phrase in phrases:
        save_user_feedback(
            update_text=update_text,
            old_type=old_type,
            old_severity=old_severity,
            old_pmbok_category=old_pmbok_category,
            new_type=new_type,
            new_severity=new_severity,
            new_pmbok_category=new_pmbok_category,
            user_phrase=phrase,
            notes=notes,
        )

    st.success("Correction saved. Feedback, phrase memory, and learned taxonomy were updated.")


if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

st.title("Project Risk Monitor")

if st.button("Clear current data"):
    for key in ["manual_updates", "latest_findings"]:
        st.session_state.pop(key, None)
    st.session_state["uploader_key"] += 1
    st.rerun()

st.subheader("Project Updates")
uploaded_files = st.file_uploader(
    "Upload files",
    type=sorted(extension.lstrip(".") for extension in SUPPORTED_EXTENSIONS),
    accept_multiple_files=True,
    key=f"uploaded_files_{st.session_state['uploader_key']}",
)
manual_text = st.text_area("Paste a manual project update")

all_updates: list[dict] = []

for uploaded_file in uploaded_files:
    try:
        parsed = parse_uploaded_file(uploaded_file)
        all_updates.extend(parsed.to_dict("records"))
    except ValueError as exc:
        st.error(str(exc))

if st.button("Add Manual Update") and manual_text.strip():
    all_updates.append({
        "update_id": "manual-1",
        "source_file": "manual_input",
        "source_type": "manual",
        "source_location": "Manual text box",
        "project": "Manual Project",
        "workstream": "General",
        "update_text": manual_text,
        "owner": "Owner unclear",
    })
    st.session_state["manual_updates"] = st.session_state.get("manual_updates", []) + [all_updates[-1]]

all_updates.extend(st.session_state.get("manual_updates", []))

if all_updates:
    source_df = pd.DataFrame(all_updates)
else:
    source_df = pd.DataFrame(columns=SOURCE_COLUMNS)

st.caption(f"Loaded {len(source_df)} updates.")
st.dataframe(source_df, use_container_width=True, hide_index=True)

current_findings = pd.DataFrame()
updates_to_classify = all_updates
findings = []

if st.button("Classify Updates"):
    if not updates_to_classify:
        st.warning("Upload a file or add a manual update before classifying.")
        st.stop()

    for update in updates_to_classify:
        finding = classify_update(update)
        findings.append(finding)

    findings_df = pd.DataFrame([f.model_dump() for f in findings])
    findings_df["update_text"] = [update.get("update_text", "") for update in updates_to_classify]
    st.dataframe(findings_df)

    for finding in findings:
        append_update_log(finding.model_dump(), source=finding.source_type)

    st.session_state["latest_findings"] = findings_df
    current_findings = findings_df
    st.success("Updates classified and appended to the update log.")

st.divider()

latest_findings = st.session_state.get("latest_findings", pd.DataFrame())
register = latest_findings if not latest_findings.empty else current_findings

show_metrics(register)
render_register(register)

export_frame = register.copy()
if not export_frame.empty:
    for column in EXPORT_COLUMNS:
        if column not in export_frame.columns:
            export_frame[column] = ""
    st.download_button(
        "Export findings CSV",
        data=export_frame[EXPORT_COLUMNS].to_csv(index=False),
        file_name="project_risk_findings.csv",
        mime="text/csv",
    )

st.divider()
render_teach_app(register)

st.divider()
st.subheader("Project Memory")
memory_text = st.text_area("Edit memory/PROJECT_MEMORY.md", value=read_project_memory(), height=360)
if st.button("Save project memory"):
    save_project_memory(memory_text)
    st.success("Project memory saved.")
