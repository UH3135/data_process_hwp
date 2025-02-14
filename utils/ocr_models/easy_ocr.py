import easyocr
import os

from utils.finder import get_jpg_filenames
from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')


def get_easy_ocr(data_path:str):
    reader = easyocr.Reader(["ko", "en"])
    text_results = reader.readtext(data_path)
    result = []
    for _, text, _ in text_results:
        result.append(str(text))

    return "\n".join(result)


def get_all_easy_ocr(data_dir:str):
    for jpg_path in get_jpg_filenames(data_dir):
        
        dir_path = os.path.abspath(os.path.join(jpg_path, "..", ".."))
        filename = os.path.splitext(os.path.basename(jpg_path))[0]
        txt_path = dir_path+f'/{filename}.txt'
        
        text = get_easy_ocr(jpg_path)

        logger.info(dir_path)
        logger.info(filename)

        with open(txt_path, 'w', encoding='utf-8') as file:
            file.write(text)
            file.write('\n\n')
        