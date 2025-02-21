from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_core.documents import Document
from dotenv import load_dotenv
from PIL import Image
from typing import List
import hashlib
import subprocess
import os
import easyocr
import re

from etc.logger import init_logger

load_dotenv()

reader = easyocr.Reader(["en", "ko"])
logger = init_logger(__file__, 'DEBUG')

def hwp_to_xhtml(hwp_path: str, output_path: str):

    # HWP to HTML 변환
    try:
        command = f"hwp5html --output {output_path} {hwp_path}"
        subprocess.run(command, shell=True, check=True)
        logger.info(f"HWP to HTML 변환에 성공했습니다.")
    except FileNotFoundError as fe:
        logger.error(f"hwp5html 실행 파일을 찾을 수 없습니다. pyhwp가 정상적으로 설치되었는지 확인하세요. {str(fe)}")
    except Exception as e:
        logger.error(f"파일 변환에 실패했습니다. Error code: {str(e)}")


def convert_to_jpg(image_dir:str, image_path:str):
    """모든 이미지를 PNG로 변환하는 함수"""
    filename, _ = os.path.splitext(os.path.basename(image_path))
    new_filename = f"{filename}.png"

    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")

            output_path = os.path.join(image_dir, new_filename)
            img.save(output_path, "PNG", compress_level=9)

            logger.info(f"[변환 완료] {output_path}")
    except Exception as e:
        logger.error(f"[변환 실패] {image_path}: {str(e)}")


def convert_all_images_in_folder(image_dir:str):
    """폴더 내 모든 이미지를 PNG 변환"""
    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(("jpg", "jpeg", "bmp", "webp")):
                image_path = os.path.join(root, file)
                convert_to_jpg(image_dir, image_path)


def convert_image_to_txt(dir_path:str, markdown_path:str, markdown_text:str) -> str:
    """Markdown에서 <img> 태그 찾고 경로 추출"""
    pattern = r"!\[.*?\]\((.*?)\)" 
    img_matches = re.finditer(pattern, markdown_text)

    if not img_matches:
        logger.info("찾은 <img> 태그가 없습니다.")
        return

    replacements = {}
    for match in img_matches:
        img_path = os.path.join(dir_path, match.group(1))
        # TODO: OCR 모델 선정
        # ocr_text = extract_text_from_img(img_path)
        ocr_text = "".join(reader.readtext(img_path, detail=0))
        if is_right_text(ocr_text):
            logger.info(f"이미지 경로: {match.group()}")
            replacements[match.group()] = ocr_text
    
    # 이미지를 텍스트로 대체
    for img_tag, ocr_result in replacements.items():
        markdown_text = markdown_text.replace(img_tag, ocr_result)

    # 처리된 내용 저장
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    logger.info('이미지를 텍스트로 변환하여 저장했습니다')
    return markdown_text


def extract_text_from_img(jpg_path:str) -> str:
    OCRLoader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=os.getenv("AZURE_COGNITIVE_API_ENDPOINT"), 
        api_key=os.getenv("AZURE_COGNITIVE_API_KEY"),  
        api_model="prebuilt-layout",
        file_path=jpg_path,
        mode="page"
    )
    documents = OCRLoader.load()
    texts = [doc.page_content for doc in documents]
    return "".join(texts)


def is_right_text(text:str):
    return True

