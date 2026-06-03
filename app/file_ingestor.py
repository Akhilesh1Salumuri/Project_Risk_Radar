from __future__ import annotations

from pathlib import Path
from typing import Any
import io
import re

import pandas as pd
from docx import Document
from pptx import Presentation


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xlsm", ".docx", ".pptx", ".txt", ".md"}


def normalize_text(text: Any) -> str:
    text = "" if text is None else str(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def make_update_record(
    update_id: str,
    source_file: str,
    source_type: str,
    update_text: str,
    project: str = "Unknown Project",
    workstream: str = "General",
    owner: str = "Owner unclear",
    location: str = "",
) -> dict:
    return {
        "update_id": update_id,
        "source_file": source_file,
        "source_type": source_type,
        "source_location": location,
        "project": project or "Unknown Project",
        "workstream": workstream or "General",
        "update_text": normalize_text(update_text),
        "owner": owner or "Owner unclear",
    }


def parse_uploaded_file(uploaded_file) -> pd.DataFrame:
    filename = uploaded_file.name
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    if extension == ".csv":
        return parse_csv(uploaded_file, filename)

    if extension in [".xlsx", ".xlsm"]:
        return parse_excel(uploaded_file, filename)

    if extension == ".docx":
        return parse_docx(uploaded_file, filename)

    if extension == ".pptx":
        return parse_pptx(uploaded_file, filename)

    if extension in [".txt", ".md"]:
        return parse_notes(uploaded_file, filename)

    raise ValueError(f"Unsupported file type: {extension}")


def parse_csv(uploaded_file, filename: str) -> pd.DataFrame:
    df = pd.read_csv(uploaded_file)
    return normalize_dataframe(df, filename, "csv")


def parse_excel(uploaded_file, filename: str) -> pd.DataFrame:
    excel_file = pd.ExcelFile(uploaded_file)
    records = []

    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        normalized = normalize_dataframe(df, filename, "excel", sheet_name=sheet_name)
        records.extend(normalized.to_dict("records"))

    return pd.DataFrame(records)


def normalize_dataframe(
    df: pd.DataFrame,
    filename: str,
    source_type: str,
    sheet_name: str = "",
) -> pd.DataFrame:
    records = []

    lower_cols = {str(col).lower().strip(): col for col in df.columns}

    text_col = (
        lower_cols.get("update_text")
        or lower_cols.get("update")
        or lower_cols.get("status")
        or lower_cols.get("comments")
        or lower_cols.get("notes")
        or lower_cols.get("description")
    )

    project_col = lower_cols.get("project")
    workstream_col = lower_cols.get("workstream")
    owner_col = lower_cols.get("owner") or lower_cols.get("assignee")

    for idx, row in df.iterrows():
        if text_col:
            update_text = normalize_text(row.get(text_col, ""))
        else:
            values = [normalize_text(v) for v in row.values if normalize_text(v)]
            update_text = " | ".join(values)

        if not update_text:
            continue

        project = normalize_text(row.get(project_col, "")) if project_col else "Unknown Project"
        workstream = normalize_text(row.get(workstream_col, "")) if workstream_col else "General"
        owner = normalize_text(row.get(owner_col, "")) if owner_col else "Owner unclear"

        location = f"Sheet: {sheet_name}, Row: {idx + 2}" if sheet_name else f"Row: {idx + 2}"

        records.append(
            make_update_record(
                update_id=f"{source_type}-{len(records) + 1}",
                source_file=filename,
                source_type=source_type,
                update_text=update_text,
                project=project,
                workstream=workstream,
                owner=owner,
                location=location,
            )
        )

    return pd.DataFrame(records)


def parse_docx(uploaded_file, filename: str) -> pd.DataFrame:
    document = Document(uploaded_file)
    records = []

    for idx, paragraph in enumerate(document.paragraphs, start=1):
        text = normalize_text(paragraph.text)
        if len(text) < 10:
            continue

        records.append(
            make_update_record(
                update_id=f"docx-p{idx}",
                source_file=filename,
                source_type="docx",
                update_text=text,
                location=f"Paragraph {idx}",
            )
        )

    table_counter = 0
    for table in document.tables:
        table_counter += 1
        for row_idx, row in enumerate(table.rows, start=1):
            cells = [normalize_text(cell.text) for cell in row.cells if normalize_text(cell.text)]
            text = " | ".join(cells)
            if len(text) < 10:
                continue

            records.append(
                make_update_record(
                    update_id=f"docx-t{table_counter}-r{row_idx}",
                    source_file=filename,
                    source_type="docx_table",
                    update_text=text,
                    location=f"Table {table_counter}, Row {row_idx}",
                )
            )

    return pd.DataFrame(records)


def parse_pptx(uploaded_file, filename: str) -> pd.DataFrame:
    presentation = Presentation(uploaded_file)
    records = []

    for slide_idx, slide in enumerate(presentation.slides, start=1):
        slide_text_parts = []

        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text = normalize_text(shape.text)
                if text:
                    slide_text_parts.append(text)

        slide_text = " | ".join(slide_text_parts)

        if len(slide_text) < 10:
            continue

        records.append(
            make_update_record(
                update_id=f"pptx-s{slide_idx}",
                source_file=filename,
                source_type="pptx",
                update_text=slide_text,
                location=f"Slide {slide_idx}",
            )
        )

    return pd.DataFrame(records)


def parse_notes(uploaded_file, filename: str) -> pd.DataFrame:
    raw = uploaded_file.read()

    if isinstance(raw, bytes):
        text = raw.decode("utf-8", errors="ignore")
    else:
        text = str(raw)

    chunks = chunk_notes_text(text)
    records = []

    for idx, chunk in enumerate(chunks, start=1):
        records.append(
            make_update_record(
                update_id=f"note-{idx}",
                source_file=filename,
                source_type="notes",
                update_text=chunk,
                location=f"Chunk {idx}",
            )
        )

    return pd.DataFrame(records)


def chunk_notes_text(text: str) -> list[str]:
    lines = [normalize_text(line) for line in text.splitlines()]
    lines = [line for line in lines if line]

    chunks = []
    buffer = []

    for line in lines:
        starts_new_item = line.startswith("- ") or line.startswith("* ") or re.match(r"^\d+[\.\)]\s+", line)

        if starts_new_item and buffer:
            chunks.append(" ".join(buffer))
            buffer = [line]
        else:
            buffer.append(line)

    if buffer:
        chunks.append(" ".join(buffer))

    final_chunks = []
    for chunk in chunks:
        if len(chunk) > 800:
            final_chunks.extend(split_long_text(chunk, max_chars=800))
        else:
            final_chunks.append(chunk)

    return [chunk for chunk in final_chunks if len(chunk) >= 10]


def split_long_text(text: str, max_chars: int = 800) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) <= max_chars:
            current = f"{current} {sentence}".strip()
        else:
            if current:
                chunks.append(current)
            current = sentence

    if current:
        chunks.append(current)

    return chunks
