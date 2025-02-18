from langchain_community.document_loaders import PyMuPDFLoader, PDFPlumberLoader
from langchain_core.documents import Document
from typing import List
import fitz

from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')

def parser_pdf_with_pymupdf(pdf_path:str) -> List[Document]:
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load() 
    return docs


def parser_pdf_with_pylumber(pdf_path:str) -> List[Document]:
    loader = PDFPlumberLoader(pdf_path)
    docs = loader.load() 
    return docs

def extract_table_as_image(pdf_path:str, output_path:str):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        pix = page.get_pixmap()
        image_path = f"{output_path}/table_page_{page_num + 1}.png"
        pix.save(image_path)

        logger.info(f"페이지 {page_num + 1}의 표가 이미지로 저장됨: {image_path}")
