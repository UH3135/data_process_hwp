from bs4 import BeautifulSoup
from PIL import Image
import html2text
import subprocess
import os
import win32com.client as win32

from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')

def hwp_to_pdf(hwp_path:str, pdf_path:str):
    
    try:
        hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
        logger.info('Hancom Office activate')

        hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")

        hwp.Open(hwp_path)
        logger.info('HWP file open success')

        hwp.SaveAs(pdf_path, "PDF")
        logger.info('hwp2pdf success')
    except Exception as e:
        logger.error(f'hwp2pdf failed {str(e)}')
    finally:
        hwp.Quit()

def hwp_to_md(hwp_path: str):
    filename = os.path.basename(os.path.splitext(hwp_path)[0])
    logger.info(f'filename: {filename}')
    output_dir = os.path.abspath(f'assets/output/{filename}')
    md_path = os.path.join(output_dir, f'{filename}.md')
    logger.info(f'output_dir: {output_dir} \n md_path: {md_path}')

    os.makedirs(output_dir, exist_ok=True)
    hwp_to_html(output_dir, hwp_path)

    html_content = load_html_content(output_dir)
    logger.info(f'html 파일을 성공적으로 로드했습니다.')

    html_to_md(html_content, md_path)
        
def hwp_to_html(hwp_path:str, output_dir:str):
    try:
        command = f"hwp5html --output {output_dir} {hwp_path}"
        subprocess.run(command, shell=True, check=True)
        logger.info(f"HWP to HTML 변환에 성공했습니다. {output_dir}")
    except FileNotFoundError as fe:
        logger.error(f"hwp5html 실행 파일을 찾을 수 없습니다. pyhwp가 정상적으로 설치되었는지 확인하세요. {str(fe)}")
    except Exception as e:
        logger.error(f"hwp5html에서 에러가 발생했습니다. {str(e)}")


def html_to_md(html_content, md_path: str):
    md_converter = html2text.HTML2Text()
    md_converter.ignore_links = False   
    md_content = md_converter.handle(html_content)

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
    logger.info(f"Markdown 파일이 생성되었습니다: {md_path}")


def load_html_content(file_dir: str):
    """html 파일 로드 및 JPG 변환"""
    xhtml_path = os.path.join(file_dir, 'index.xhtml')
    with open(xhtml_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "xml")

    for img_tag in soup.find_all("img"):
        img_src = img_tag["src"]
        img_path = os.path.join(file_dir, img_src)

        if os.path.exists(img_path):
            img = Image.open(img_path)
            new_img_path = os.path.splitext(img_path)[0] + ".jpg"

            img.convert("RGB").save(new_img_path, "JPEG")
            img_tag["src"] = os.path.join('bindata', os.path.basename(new_img_path))
    
    with open(xhtml_path, "w+", encoding="utf-8") as file:
        file.write(str(soup))
        file.seek(0)
        html_content = file.read()
    return html_content


