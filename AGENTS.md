---
name: project-risk-monitor
description: Guide coding agents to build and maintain the MVP-only project risk monitor with local memory, multi-file ingestion, and deterministic classification.
---

# Project Risk Monitor

## Project

### Scope
- MVP only

### Stack
- Python
- Streamlit
- Pandas
- Pydantic

### Run command
```bash
streamlit run app/streamlit_app.py
```

## Exclusions
- Gmail
- Jira
- OAuth
- database
- OCR
- external AI APIs
- cloud deployment

## Memory

### Files
- Read and update: `memory/PROJECT_MEMORY.md`
- Update log: `memory/UPDATE_LOG.csv`
- Learned phrases: `memory/PHRASE_MEMORY.csv`
- Feedback: `memory/CLASSIFICATION_FEEDBACK.csv`
- Learned taxonomy: `memory/LEARNED_TAXONOMY.md`

## Multi-file ingestion

### Supported file types
- `.csv`
- `.xlsx`
- `.xlsm`
- `.docx`
- `.pptx`
- `.txt`
- `.md`

### Normalized update fields
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

### Ingestion rules
- CSV and Excel rows become project update records.
- Word paragraphs and table rows become project update records.
- PowerPoint slide text becomes project update records.
- Text and Markdown bullets or paragraphs become project update records.
- The risk classifier consumes only normalized records.

## Classification and learning

### Order
1. Learned phrase memory first
2. NLP/context parsing
3. PMBOK mapping
4. Base rules
5. Teach the App correction
6. Update phrase memory, feedback, and learned taxonomy files

### Finding source metadata
- `source_file`
- `source_type`
- `source_location`
