import fitz
import os

def extract_table_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    tables = []
    for page_num in range(len(doc)):
        page = doc[page_num]

        table_data = []

        blocks = page.get_text("blocks")
        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            if len(text.split("\n")) > 2:
                table_data.append(text)
        tables.append(table_data)
    doc.close()
    return tables
