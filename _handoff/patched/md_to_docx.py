#!/usr/bin/env python3
"""Convert a markdown file to .docx with reasonable formatting.

Handles:
- # / ## / ### / #### headings
- bullet lists (- and *)
- numbered lists (1. 2. ...)
- inline **bold**, *italic*, `code`
- code blocks (``` … ```)
- markdown tables (| col | col |)
- horizontal rules (---)
- regular paragraphs

Not exhaustive but enough for our SOP/manual output.
"""
import re
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_runs_with_inline(p, text):
    """Parse inline **bold**, *italic*, `code` and add as runs to paragraph p."""
    # Tokenize on **bold**, *italic*, `code`
    # Simple approach: scan
    pattern = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            p.add_run(text[pos:m.start()])
        tok = m.group(0)
        if tok.startswith("**") and tok.endswith("**"):
            r = p.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("*") and tok.endswith("*"):
            r = p.add_run(tok[1:-1]); r.italic = True
        elif tok.startswith("`") and tok.endswith("`"):
            r = p.add_run(tok[1:-1])
            r.font.name = "Menlo"
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0x88, 0x44, 0x00)
        pos = m.end()
    if pos < len(text):
        p.add_run(text[pos:])


def convert(md_path, docx_path):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    doc = Document()
    # Set default style to a sane size
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        # First row is header; second row is the |---|---| separator (skip)
        header = table_rows[0]
        body = table_rows[2:] if len(table_rows) > 1 and re.match(r"^[\s|:-]+$", "|".join(table_rows[1])) else table_rows[1:]
        # Add table
        cols = len(header)
        t = doc.add_table(rows=1 + len(body), cols=cols)
        t.style = "Light Grid Accent 1"
        for c, h in enumerate(header):
            cell = t.rows[0].cells[c]
            cell.text = ""
            p = cell.paragraphs[0]
            r = p.add_run(h.strip())
            r.bold = True
        for r_i, row in enumerate(body, start=1):
            for c_i, val in enumerate(row[:cols]):
                cell = t.rows[r_i].cells[c_i]
                cell.text = ""
                add_runs_with_inline(cell.paragraphs[0], val.strip())
        doc.add_paragraph()  # spacer
        table_rows = []

    while i < len(lines):
        line = lines[i]

        # Code block fence
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                # End code block
                in_code = False
                p = doc.add_paragraph()
                r = p.add_run("\n".join(code_buf))
                r.font.name = "Menlo"
                r.font.size = Pt(9)
                p.paragraph_format.left_indent = Inches(0.3)
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Markdown table detection
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            in_table = True
            i += 1
            continue
        elif in_table:
            flush_table()
            in_table = False

        # Headings
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            # Strip trailing inline formatting markers from headers
            doc.add_heading(text, level=level)
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            r = p.add_run("─" * 40)
            r.font.color.rgb = RGBColor(0xC0, 0xC0, 0xC0)
            i += 1
            continue

        # Bullet list
        m = re.match(r"^(\s*)[-*]\s+(.+)$", line)
        if m:
            text = m.group(2).strip()
            p = doc.add_paragraph(style="List Bullet")
            add_runs_with_inline(p, text)
            i += 1
            continue

        # Numbered list
        m = re.match(r"^(\s*)\d+\.\s+(.+)$", line)
        if m:
            text = m.group(2).strip()
            p = doc.add_paragraph(style="List Number")
            add_runs_with_inline(p, text)
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            r = p.add_run(line.lstrip("> ").strip())
            r.italic = True
            i += 1
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Regular paragraph
        p = doc.add_paragraph()
        add_runs_with_inline(p, line)
        i += 1

    if in_table:
        flush_table()

    doc.save(docx_path)
    print(f"Wrote {docx_path}")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
