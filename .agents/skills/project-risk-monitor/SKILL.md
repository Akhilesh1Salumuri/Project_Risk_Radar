---
name: project-risk-monitor
description: Build or improve a lightweight project risk monitoring MVP with local multi-file artefact ingestion, PMBOK-aligned classification, and user learning.
---

# Project Risk Monitor

## Purpose
- Monitor project updates for delivery risk.
- Normalize updates from files and manual text into one source schema.
- Classify updates using local deterministic rules and learned phrases.
- Preserve learning and memory locally.

## MVP scope

### Included
- Streamlit interface
- Multi-file upload
- Manual update entry
- CSV and Excel row ingestion
- Word paragraph and table ingestion
- PowerPoint slide text ingestion
- Text and Markdown bullet or paragraph ingestion
- PMBOK-style risk category mapping
- Teach the App user correction loop
- Local CSV and Markdown memory files

### Excluded
- Gmail
- Jira
- OAuth
- database
- OCR
- external AI APIs
- cloud deployment

## Supported file types
- `.csv`
- `.xlsx`
- `.xlsm`
- `.docx`
- `.pptx`
- `.txt`
- `.md`

## Normalized update schema

### Fields
- `update_id`
- `source_file`
- `source_type`
- `source_location`
- `project`
- `workstream`
- `update_text`
- `owner`

### Defaults
- Project: `Unknown Project`
- Workstream: `General`
- Owner: `Owner unclear`

## Risk taxonomy
- Risk
- Blocker
- Dependency
- Pending Decision
- Overdue Action
- Scope Change
- Data Issue
- Compliance Risk
- Adoption Risk
- General Update

## Classification order
1. Learned phrase memory first
2. NLP/context parsing
3. PMBOK mapping
4. Base rules
5. Teach the App correction
6. Update `PHRASE_MEMORY.csv`, `CLASSIFICATION_FEEDBACK.csv`, and `LEARNED_TAXONOMY.md`

## Memory behavior
- Project memory: `memory/PROJECT_MEMORY.md`
- Update log: `memory/UPDATE_LOG.csv`
- Phrase memory: `memory/PHRASE_MEMORY.csv`
- Feedback log: `memory/CLASSIFICATION_FEEDBACK.csv`
- Learned taxonomy: `memory/LEARNED_TAXONOMY.md`

## Done criteria
- App runs with `streamlit run app/streamlit_app.py`.
- Users can upload multiple supported files at once.
- All extracted records are normalized before classification.
- Findings include `source_file`, `source_type`, and `source_location`.
- `UPDATE_LOG.csv` includes `source_file`, `source_type`, and `source_location`.
- Teach the App updates local learning files.
