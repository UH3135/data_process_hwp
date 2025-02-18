from utils.converter import convert_all_hwp2md
from utils.ocr_models import extract_text_with_ocr
import os


data_dir = os.path.abspath('assets')

convert_all_hwp2md(data_dir)
extract_text_with_ocr(data_dir)
