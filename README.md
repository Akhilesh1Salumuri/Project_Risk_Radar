# Project Risk Radar

Project Risk Radar is a local Streamlit MVP for classifying project updates into delivery risks, blockers, dependencies, pending decisions, overdue actions, scope changes, data issues, compliance risks, adoption risks, and general updates.

## What it does

- Upload multiple files at once.
- Supports `.csv`, `.xlsx`, `.xlsm`, `.docx`, `.pptx`, `.txt`, and `.md`.
- Normalizes every extracted update into a common schema.
- Classifies updates with deterministic local rules.
- Maps findings to PMBOK-style risk categories.
- Lets users teach the app corrected phrases.
- Stores local memory in CSV and Markdown files.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Then open:

```text
http://localhost:8501
```

## MVP boundaries

This MVP does not include Gmail, Jira, OAuth, databases, OCR, external AI APIs, or cloud-specific integrations.
