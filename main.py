from utils.converter import convert_all_hwp2md
from utils.ocr_models import get_all_easy_ocr
from utils.finder import get_hwp_filenames, get_jpg_filenames
from etc.logger import init_logger
import os

logger = init_logger(__file__, 'DEBUG')

data_path = os.path.abspath("assets/output/acadj_10/bindata/BIN0001.jpg")
data_dir = os.path.abspath('assets')

# convert_all_hwp2md()
# print(get_jpg_filenames(data_dir))
get_all_easy_ocr(data_dir)