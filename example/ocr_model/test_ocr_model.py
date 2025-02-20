import os
from dotenv import load_dotenv

from utils.ocr_models import all_md2txt_with_ocr

load_dotenv()

TEST_DATA_PATH = os.path.abspath("assets/output/acadj_10/")

all_md2txt_with_ocr(TEST_DATA_PATH)