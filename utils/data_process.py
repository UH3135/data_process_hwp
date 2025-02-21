from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_core.documents import Document
from dotenv import load_dotenv
from typing import List
import easyocr
import os
import re

from etc.logger import init_logger
from utils.converter import hwp_to_xhtml, convert_all_images_in_folder
from utils.parser import parsing_xhtml

load_dotenv()
logger = init_logger(__file__, 'DEBUG')

reader = easyocr.Reader(["en", "ko"])

def main(data_dir: str) -> None:
    """
    data directory 내의 모든 hwp 파일 탐색
    hwp을 xhtml로 변환
    xhtml을 bs4로 parsing
    markdown 데이터에서 table, img 파싱 -> table은 json으로 img는 Text로 변환해서 markdown에 합치기
    결과로 나온 markdown 분석해서 json으로 변환
    """
    for hwp_path in get_filenames_with_type(data_dir, 'hwp'):
        filename = os.path.basename(os.path.splitext(hwp_path)[0])

        output_dir = os.path.abspath(f'assets/output/{filename}')
        md_path = os.path.join(output_dir, f'{filename}.md')    
        html_path = os.path.join(output_dir, 'index.xhtml')
        img_dir = os.path.join(output_dir, "bindata")
        
        if os.path.exists(output_dir):
            logger.info(f"xhtml 파일이 이미 존재합니다.: {output_dir}")
        else:
            os.makedirs(output_dir, exist_ok=True)
            hwp_to_xhtml(hwp_path, output_dir)
        parsing_xhtml(html_path, md_path)

        convert_all_images_in_folder(img_dir)

        with open(md_path, 'r', encoding="utf-8") as f:
            markdown_text = f.read()
        logger.info(f'Markdown 텍스트를 읽었습니다: {md_path}')
        
#         # 이미지 태그 추출 및 OCR 처리
#         img_matches = extract_image_tags(markdown_content)
#         tables = extract_tables(markdown_content)

#         replacements = {}
#         for match in img_matches:
#             img_path = os.path.join(dir_path, match.group(1))
#             ocr_text = "".join(reader.readtext(img_path, detail=0))
#             logger.info(f"이미지 경로: {match.group()}, 추출된 텍스트: {ocr_text}")
#             replacements[match.group()] = ocr_text
        
#         # 이미지를 텍스트로 대체
#         for img_tag, ocr_result in replacements.items():
#             markdown_content = markdown_content.replace(img_tag, ocr_result)

#         # 처리된 내용 저장
#         with open(md_path, "w", encoding="utf-8") as f:
#             f.write(markdown_content)
#         logger.info(f'{md_path}: 이미지를 텍스트로 변환하여 저장했습니다')

# def extract_text_from_document_ai(file_path:str) -> str:
#     OCRLoader = AzureAIDocumentIntelligenceLoader(
#         api_endpoint=os.getenv("AZURE_COGNITIVE_API_ENDPOINT"), 
#         api_key=os.getenv("AZURE_COGNITIVE_API_KEY"),  
#         api_model="prebuilt-layout",
#         file_path=file_path,
#         mode="page"
#     )
#     logger.info(f"{file_path}: 모델 로드가 완료되었습니다")
#     documents = OCRLoader.load()
#     texts = [doc.page_content for doc in documents]
#     return "".join(texts)

# def extract_image_tags(markdown_text:str):
#     """Markdown에서 <img> 태그 찾고 경로 추출"""
#     pattern = r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>'
#     return re.finditer(pattern, markdown_text)


def get_filenames_with_type(directory: str, type: str) -> List[str]:
    if not os.path.exists(directory):
        logger.error(f"Error:'{directory}'가 존재하지 않습니다.")
        return []

    found_files = []
    for root, _, files in os.walk(directory):
        found_files.extend([os.path.join(root, f) for f in files if f.lower().endswith(f".{type}")])

    if not found_files:
        logger.error(f"해당 {directory}에 {type} 파일이 없습니다.")
        return []

    logger.info(f"{len(found_files)}개의 {type} 파일을 찾았습니다.")

    return found_files