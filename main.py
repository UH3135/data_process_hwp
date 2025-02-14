from utils.converter import convert_all_hwp2md, convert_all_hwp2pdf, convert_all_mp4_to_wav
from utils.ocr_models import extract_text_with_ocr
from utils.parser import extract_table_pymupdf, extract_text_images_tables
from etc.logger import init_logger
import os

logger = init_logger(__file__, 'DEBUG')

data_dir = os.path.abspath('assets')
hwp_path = os.path.abspath("assets/OneDrive_2025-02-14/acadj_10.hwp")
mp4_path = os.path.join('assets/OneDrive_2025-02-14/acadj_1.mp4')
pdf_path = os.path.abspath('assets/test/과업지시서_v1.0/과업지시서_v1.0.pdf')

test_dir = os.path.abspath("assets/output/acadj_10/")
jpg_path = os.path.abspath('assets/output/acadj_10/bindata/BIN0001.jpg')
md_path = os.path.join(test_dir, 'acadj_10.md')

# convert_all_hwp2md(data_dir)
# convert_all_hwp2pdf(data_dir)
# convert_all_mp4_to_wav(data_dir)
# print(get_jpg_filenames(data_dir))
# get_all_easy_ocr(data_dir)

data = extract_table_pymupdf(pdf_path)

for row in data:
    print(row)