from utils.converter import convert_all_hwp2md, convert_all_hwp2pdf
from utils.ocr_models import extract_text_with_ocr
from etc.logger import init_logger
import os

logger = init_logger(__file__, 'DEBUG')

hwp_path = os.path.abspath("assets/OneDrive_2025-02-14/acadj_10.hwp")
data_dir = os.path.abspath('assets')
md_path = os.path.abspath('assets/output/acadj_1/acadj_1.md')
jpg_path = os.path.abspath('assets/output/acadj_10/bindata/BIN0001.jpg')


# hwp_to_pdf(hwp_path)
convert_all_hwp2md(data_dir)
# convert_all_hwp2pdf(data_dir)
# print(get_jpg_filenames(data_dir))
# get_all_easy_ocr(data_dir)