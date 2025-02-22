from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_core.documents import Document
from dotenv import load_dotenv
from typing import List
from datetime import datetime
import easyocr
import json
import os

from etc.logger import init_logger
from utils.converter import hwp_to_xhtml, convert_image_to_txt
from utils.parser import parsing_xhtml, extract_tables_from_xhtml, extract_clean_tables_from_markdown
from utils.llm import extract_tables_from_text
from utils.data_process import preprocess_markdown


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
    result = {
        "documents": []
    }

    for hwp_path in get_filenames_with_type(data_dir, 'hwp'):
        filename = os.path.basename(os.path.splitext(hwp_path)[0])

        output_dir = os.path.abspath(f'assets/output/{filename}')
        md_path = os.path.join(output_dir, f'{filename}.md')    
        html_path = os.path.join(output_dir, 'index.xhtml')
        img_dir = os.path.join(output_dir, "bindata")
        
        logger.info(f"현재 변환중인 파일: {output_dir}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            hwp_to_xhtml(hwp_path, output_dir)
        parsing_xhtml(html_path, md_path)

        # convert_all_images_in_folder(img_dir)
        with open(md_path, 'r', encoding="utf-8") as f:
            md_text = f.read()
        logger.info(f'Markdown 텍스트를 읽었습니다')

        md_text = convert_image_to_txt(output_dir, md_path, md_text)

        table_data = extract_clean_tables_from_markdown(md_text)
        text_data = preprocess_markdown(md_text)

        now = datetime.now()
        formatted_time = now.strftime("%Y%m%dT%H:%M:%SZ")

        docs_json = {
            "id": filename,
            "content": text_data,
            "table": table_data,
            "metadata": {
                "timestamp": formatted_time
            },

        }
        result["documents"].append(docs_json)
    return json.dumps(result, ensure_ascii=False, indent=4)


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