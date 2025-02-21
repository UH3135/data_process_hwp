from bs4 import BeautifulSoup
from PIL import Image
from typing import List
import html2text
import subprocess
import os

from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')

def hwp_to_xhtml(hwp_path: str, output_path: str):

    # HWP to HTML 변환
    try:
        command = f"hwp5html --output {output_path} {hwp_path}"
        subprocess.run(command, shell=True, check=True)
        logger.info(f"HWP to HTML 변환에 성공했습니다. {output_path}")
    except FileNotFoundError as fe:
        logger.error(f"hwp5html 실행 파일을 찾을 수 없습니다. pyhwp가 정상적으로 설치되었는지 확인하세요. {str(fe)}")
    except Exception as e:
        logger.error(f"파일 변환에 실패했습니다. Error code: {str(e)}")


def convert_to_jpg(image_dir:str, image_path:str):
    """모든 이미지를 JPG로 변환하는 함수"""
    filename, _ = os.path.splitext(os.path.basename(image_path))
    new_filename = f"{filename}.jpg"

    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output_path = os.path.join(image_dir, new_filename)
            img.save(output_path, "JPEG", quality=90)

            logger.info(f"[변환 완료] {output_path}")
    except Exception as e:
        logger.error(f"[변환 실패] {image_path}: {str(e)}")


def convert_all_images_in_folder(image_dir:str):
    """폴더 내 모든 이미지를 JPG로 변환"""
    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(("png", "bmp", "gif", "webp")):
                image_path = os.path.join(root, file)
                convert_to_jpg(image_dir, image_path)


# def hwp_to_md(hwp_path: str):

    
#     # html 로드 및 bmp등의 이미지 jpg 변환
#     xhtml_path = os.path.join(output_dir, 'index.xhtml')
#     with open(xhtml_path, "r", encoding="utf-8") as html_file:
#         soup = BeautifulSoup(html_file, "xml")

#     for img_tag in soup.find_all("img"):
#         img_src = img_tag["src"]
#         img_path = os.path.join(output_dir, img_src)

#         if os.path.exists(img_path):
#             img = Image.open(img_path)
#             new_img_path = os.path.splitext(img_path)[0] + ".jpg"

#             img.convert("RGB").save(new_img_path, "JPEG")
#             img_tag["src"] = os.path.join('bindata', os.path.basename(new_img_path))
    
#     with open(xhtml_path, "w+", encoding="utf-8") as file:
#         file.write(str(soup))
#         file.seek(0)
#         html_content = file.read()

#     logger.info(f'html 파일을 성공적으로 로드했습니다.')

#     # html to markdown
#     md_converter = html2text.HTML2Text()
#     md_converter.ignore_links = False   
#     md_content = md_converter.handle(html_content)

#     with open(md_path, 'w', encoding='utf-8') as md_file:
#         md_file.write(md_content)
#     logger.info(f"Markdown 파일이 생성되었습니다: {md_path}")

