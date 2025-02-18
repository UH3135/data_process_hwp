from utils.converter import convert_all_hwp2md, convert_all_hwp2pdf, convert_all_mp4_to_wav
from utils.ocr_models import extract_text_with_ocr
import os


data_dir = os.path.abspath('assets')

convert_all_hwp2md(data_dir)
convert_all_hwp2pdf(data_dir)
convert_all_mp4_to_wav(data_dir)
extract_text_with_ocr(data_dir)
