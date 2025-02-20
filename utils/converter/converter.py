from bs4 import BeautifulSoup
from PIL import Image
import html2text
import subprocess
import os

from utils.finder import get_filenames_with_type
from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')

def hwp_to_md(hwp_path: str):
    filename = os.path.basename(os.path.splitext(hwp_path)[0])

    output_dir = os.path.abspath(f'assets/output/{filename}')
    md_path = os.path.join(output_dir, f'{filename}.md')    
    html_path = os.path.join(output_dir, 'index.xhtml')

    if os.path.exists(output_dir):
        logger.info(f"{output_dir}이 이미 존재합니다.")
        return 
    os.makedirs(output_dir, exist_ok=True)

    # HWP to HTML 변환
    try:
        command = f"hwp5html --output {output_dir} {hwp_path}"
        subprocess.run(command, shell=True, check=True)
        logger.info(f"HWP to HTML 변환에 성공했습니다. {html_path}")
    except FileNotFoundError as fe:
        logger.error(f"hwp5html 실행 파일을 찾을 수 없습니다. pyhwp가 정상적으로 설치되었는지 확인하세요. {str(fe)}")
    
    # html 로드 및 bmp등의 이미지 jpg 변환
    xhtml_path = os.path.join(output_dir, 'index.xhtml')
    with open(xhtml_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "xml")

    for img_tag in soup.find_all("img"):
        img_src = img_tag["src"]
        img_path = os.path.join(output_dir, img_src)

        if os.path.exists(img_path):
            img = Image.open(img_path)
            new_img_path = os.path.splitext(img_path)[0] + ".jpg"

            img.convert("RGB").save(new_img_path, "JPEG")
            img_tag["src"] = os.path.join('bindata', os.path.basename(new_img_path))
    
    with open(xhtml_path, "w+", encoding="utf-8") as file:
        file.write(str(soup))
        file.seek(0)
        html_content = file.read()

    logger.info(f'html 파일을 성공적으로 로드했습니다.')

    # html to markdown
    md_converter = html2text.HTML2Text()
    md_converter.ignore_links = False   
    md_content = md_converter.handle(html_content)

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
    logger.info(f"Markdown 파일이 생성되었습니다: {md_path}")

def convert_all_hwp2md(data_path:str):
    for file_path in get_filenames_with_type(data_path, 'hwp'):
        hwp_to_md(file_path)
