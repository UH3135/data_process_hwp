import os

from utils.converter import convert_all_hwp2md
from utils.ocr_models import all_md2txt_with_ocr

# basic setting
DATA_PATH = os.path.abspath('assets')

# convert_all_hwp2md(DATA_PATH)
all_md2txt_with_ocr(DATA_PATH)