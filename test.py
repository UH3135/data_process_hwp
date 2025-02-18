from utils.parser import parser_pdf_with_pymupdf, parser_pdf_with_pylumber
from ai_model import get_answer_llm
from utils.ocr_models.openai_ocr import extract_text_from_document_ai
from utils.ocr_models.easy_ocr import get_easy_ocr
from utils.parser.pdf_parser import extract_table_as_image
import os


data_dir = os.path.abspath('assets')
hwp_path = os.path.abspath("assets/OneDrive_2025-02-14/acadj_10.hwp")
mp4_path = os.path.join('assets/OneDrive_2025-02-14/acadj_1.mp4')
pdf_path = os.path.abspath('assets/test/과업지시서_v1.0.pdf')
pdf_dir = os.path.abspath(os.path.join(pdf_path, '..'))

test_dir = os.path.abspath("assets/output/acadj_10/")
jpg_path = os.path.abspath('assets/output/acadj_10/bindata/BIN0001.jpg')
table_path = os.path.abspath('assets/test/table_page_6.png')
md_path = os.path.join(test_dir, 'acadj_10.md')

# for doc in extract_text_from_document_ai(table_path):
#     print(doc.page_content)

for doc in parser_pdf_with_pymupdf(pdf_path):
    print(doc.page_content)
# print(get_easy_ocr(jpg_path))
# print(get_answer_llm('세부 과업에는 뭐가 있나요?', parser_pdf_with_pymupdf(pdf_path)))
