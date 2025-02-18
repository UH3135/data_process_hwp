from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_core.documents import Document
from dotenv import load_dotenv
from typing import List
import os

from etc.logger import init_logger
from utils.finder import get_filenames_with_type


load_dotenv()
logger = init_logger(__file__, 'DEBUG')

def extract_text_with_ocr(data_dir:str) -> None:
    """OCR 모델을 이용하여 JPG를 TXT 파일로 변환하여 저장"""
    for jpg_path in get_filenames_with_type(data_dir, 'jpg'):
        
        dir_path = os.path.abspath(os.path.join(jpg_path, "..", ".."))
        filename = os.path.splitext(os.path.basename(jpg_path))[0]
        txt_path = dir_path+f'/{filename}.txt'
        
        text = extract_text_from_document_ai(jpg_path)
        logger.info('OCR 모델 호출')

        try:
            if not os.path.exists(txt_path):
                with open(txt_path, 'w', encoding='utf-8') as file:
                    file.write(text)
                    file.write('\n\n')
                logger.info(f'{txt_path} 파일 생성')
            else:
                logger.info(f'{txt_path} 파일이 이미 존재합니다.')
        except Exception as e:
            logger.error(f'{txt_path} 파일 생성 실패 {str(e)}')


def extract_text_from_document_ai(file_path:str) -> str:
    OCRLoader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=os.getenv("AZURE_COGNITIVE_API_ENDPOINT"), 
        api_key=os.getenv("AZURE_COGNITIVE_API_KEY"),  
        api_model="prebuilt-layout",
        file_path=file_path,
        mode="page"
    )

    documents = OCRLoader.load()
    texts = [doc.page_content for doc in documents]
    return "".join(texts)