# Instructions: Run Project Risk Radar Locally

## 1. Prerequisites

Install Python 3.11 or newer. On Windows, confirm Python is available:

```powershell
py --version
```

## 2. Get the project

Clone the repository:

```powershell
git clone https://github.com/Akhilesh1Salumuri/Project_Risk_Radar.git
cd Project_Risk_Radar
```

## 3. Create a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Start the app

```powershell
streamlit run app/streamlit_app.py
```

Open the browser URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## 6. Use the app

1. Upload one or more supported files: `.csv`, `.xlsx`, `.xlsm`, `.docx`, `.pptx`, `.txt`, or `.md`.
2. Optionally paste a manual project update and click **Add Manual Update**.
3. Click **Classify Updates**.
4. Review the Risk Register.
5. Use **Teach the app** to correct type, severity, PMBOK category, and phrase memory.
6. Export findings if needed.

## 7. Local memory files

The app writes local memory under `memory/`:

- `UPDATE_LOG.csv`
- `PHRASE_MEMORY.csv`
- `CLASSIFICATION_FEEDBACK.csv`
- `LEARNED_TAXONOMY.md`
- `PROJECT_MEMORY.md`

These files are local runtime memory. Review before committing any real project data.

## 8. MVP limitations

This MVP is intentionally local and simple. It does not include Gmail, Jira, OAuth, databases, OCR, external AI APIs, or cloud deployment automation.
