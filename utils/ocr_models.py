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


def extract_text_from_img(jpg_path:str) -> str:
    OCRLoader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=os.getenv("AZURE_COGNITIVE_API_ENDPOINT"), 
        api_key=os.getenv("AZURE_COGNITIVE_API_KEY"),  
        api_model="prebuilt-layout",
        file_path=jpg_path,
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
