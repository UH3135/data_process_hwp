from utils.converter import convert_all_hwp2md, convert_all_hwp2pdf, hwp_to_md
from utils.ocr_models import easy_ocr
import os


data_path = os.path.abspath('assets/')
img_path = os.path.abspath("assets/output/acadj_10/bindata/BIN0001.jpg")
hwp_path = os.path.abspath("assets/OneDrive_2025-02-14/acadj_1.hwp")
pdf_path = os.path.abspath("assets/output/acadj_1/acadj_1.pdf")


hwp_to_md(hwp_path)
# convert_all_hwp2md(data_path)
# convert_all_hwp2pdf(data_path)
# easy_ocr(img_path)