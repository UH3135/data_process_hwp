import os

from etc.logger import init_logger
from utils.finder import get_jpg_filenames
from utils.ocr_models.easy_ocr import get_easy_ocr
from utils.ocr_models.openai_ocr import extract_text_from_document_ai

logger = init_logger(__file__, 'DEBUG')

def extract_text_with_ocr(data_dir:str):
    """OCR 모델을 이용하여 JPG를 TXT 파일로 변환하여 저장"""
    for jpg_path in get_jpg_filenames(data_dir):
        
        dir_path = os.path.abspath(os.path.join(jpg_path, "..", ".."))
        filename = os.path.splitext(os.path.basename(jpg_path))[0]
        txt_path = dir_path+f'/{filename}.txt'
        
        # OCR 모델 선정
        text = get_easy_ocr(jpg_path)
        logger.info('OCR 모델 호출')

        try:
            with open(txt_path, 'w', encoding='utf-8') as file:
                file.write(text)
                file.write('\n\n')

            logger.info(f'{txt_path} 파일 생성')
        except Exception as e:
            logger.error(f'{txt_path} 파일 생성 실패 {str(e)}')