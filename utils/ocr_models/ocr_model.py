from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_core.documents import Document
from dotenv import load_dotenv
from typing import List
import easyocr
import os
import re

from etc.logger import init_logger
from utils.finder import get_filenames_with_type


load_dotenv()
logger = init_logger(__file__, 'DEBUG')

reader = easyocr.Reader(["en", "ko"])

def all_md2txt_with_ocr(data_dir: str) -> None:
    """OCR 모델을 이용하여 markdown을 TXT 파일로 변환하여 저장"""
    pattern = r"!\[.*?\]\((.*?)\)"
    for md_path in get_filenames_with_type(data_dir, 'md'):
        dir_path = os.path.abspath(os.path.join(md_path, ".."))
        
        with open(md_path, 'r', encoding="utf-8") as f:
            markdown_content = f.read()
        logger.info(f'{md_path}: Markdown Text Read')
        img_matches = extract_image_tags(markdown_content)

        replacements = {}
        for match in img_matches:
            img_path = os.path.join(dir_path, match.group(1))
            #TODO 로고 부분은 여기서 검출해서 제거하도록
            # ocr_text = " ".join(extract_text_from_document_ai(img_path))
            ocr_text = "".join(reader.readtext(img_path, detail=0))  # Test용 코드
            logger.info(f"JPG PATH: {match.group()}, Text: {ocr_text}")
            replacements[match.group()] = ocr_text
        
        for img_tag, ocr_result in replacements.items():
            markdown_content = markdown_content.replace(img_tag, ocr_result)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        logger.info(f'{md_path}Img를 Text로 변경 후 입력')


def extract_text_from_document_ai(file_path:str) -> str:
    OCRLoader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=os.getenv("AZURE_COGNITIVE_API_ENDPOINT"), 
        api_key=os.getenv("AZURE_COGNITIVE_API_KEY"),  
        api_model="prebuilt-layout",
        file_path=file_path,
        mode="page"
    )
    logger.info(f"{file_path}: Model Load 완료했습니다")
    documents = OCRLoader.load()
    texts = [doc.page_content for doc in documents]
    return "".join(texts)


def extract_image_tags(markdown_text:str):
    """Markdown에서 <img> 태그 찾고 경로 추출"""
    pattern = r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>'
    return re.finditer(pattern, markdown_text)
